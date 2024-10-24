from correlations import compute_and_plot_correlation, create_top_correlated_df
from data_extraction import create_base_df, plot_kpi_evolution, pivot_on_city
from model import run_synthetic_control
from glovo_synthetic_control_experiments.synthetic_control import SyntheticControl
import pandas as pd

query_names = ['pl_city_orders']
base_df = create_base_df(query_names, reload_data=False, transform_func=pivot_on_city)
column_name = 'WAW'
correlation_result = compute_and_plot_correlation(base_df, column_name, 30)
top_correlation_df = create_top_correlated_df(base_df, 'WAW', correlation_result)
top_correlation_df['date'] = pd.to_datetime(top_correlation_df['date'])
#plot_kpi_evolution(top_correlation_df, rolling_mean_value=14, start_date='2024-09-01', end_date='2024-09-30', plot_type='rolling')

run_synthetic_control(top_correlation_df, '2024-01-01', '2024-09-01', '2024-09-30', 'WAW')

sc = SyntheticControl(
    target_column='WAW',
    predictors=['GDN'],
    date_column='date',
    model_name="causal_impact",
)
intervention_dates = sc.intervention_dates_from_periods(
    top_correlation_df.query("date < '2024-09-01' & date >= '2024-01-01'"), periods_train=90, periods_test=30, frequency="W"
)
backtest_result = sc.backtest(
    data=top_correlation_df.query("date < '2024-09-01' & date >= '2024-01-01'"),
    number_periods_train=[20, 30, 60, 90],
    number_periods_test=[10, 20, 30],
    intervention_dates=intervention_dates,
    candidate_predictors=[
        ["POZ", "GDN"],
        ["GDN"],
        ["GDN", "POZ", "BZG"],
        ["GDN", "POZ", "SZY"],
        ["GDN", "POZ", "LOD"],
        ["GDN", "POZ", "KRA"],
        ["POZ"],
        ["BZG"],
        ["LOD"],
        ["KRA", "LOD", "SZY", "BZG", "GDN", "POZ"],
        ["KRA", "LOD", "SZY", "BZG"],
        ["SZY", "BZG"],
        ["KRA"],
        ["KRA", "LOD"],
    ]
)
print(backtest_result.to_string())
print('The backtest is done.')
aggregated_backtest = backtest_result.groupby(['predictors', 'test_period_duration', 'train_period_duration']).mean().reset_index()
aggregated_backtest.sort_values(['mae'], ascending=[False]).head(10)
print(aggregated_backtest.to_string())