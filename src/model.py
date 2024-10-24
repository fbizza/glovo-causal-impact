from glovo_synthetic_control_experiments.synthetic_control import SyntheticControl
import pandas as pd

def run_synthetic_control(df, start_date, intervention_date, end_date, target_column, date_column='date'):
    # Extract predictors by excluding the target and date columns
    predictors = [col for col in df.columns if col not in [target_column, date_column]]

    # Initialize the SyntheticControl object
    sc = SyntheticControl(
        target_column=target_column,
        predictors=predictors,
        date_column=date_column,
        model_name="causal_impact",
        alpha=0.1,
    )

    # Train the model
    sc.train(df, start_date=start_date, intervention_date=intervention_date, end_date=end_date)

    # Get the underlying model
    model = sc.get_underlying_model()

    # Print the model summary
    print(model.summary())

    # Plot the model
    model.plot()

# Example usage
# df = pd.read_csv('your_data.csv')  # Load your data into a DataFrame
# run_synthetic_control(df, '2024-01-01', '2024-09-01', '2024-09-30', 'WAW')