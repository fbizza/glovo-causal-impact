from correlations import compute_and_plot_correlation
from data_extraction import create_base_df, plot_kpi_evolution, pivot_on_city

query_names = ['pl_city_orders']
base_df = create_base_df(query_names, reload_data=False, transform_func=pivot_on_city)
print(base_df)
# plot_kpi_evolution(base_df, rolling_mean_value=14, start_date='2024-09-01', end_date='2024-09-30', plot_type='rolling')
column_name = 'WAW'
correlation_result = compute_and_plot_correlation(base_df, column_name, 20)
print(correlation_result)
