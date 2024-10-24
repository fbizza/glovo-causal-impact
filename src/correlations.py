import pandas as pd
import matplotlib.pyplot as plt

def compute_and_plot_correlation(df, column_name, top_n=10):
    """
    Computes the correlation of a specified column with all other columns in the DataFrame and plots the results.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column_name (str): The name of the column to compute the correlation against.
    top_n (int): The number of top correlations to consider.

    Returns:
    pd.Series: A Series containing the top n correlation values of the specified column with other columns.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

    # Drop the 'date' column if it exists
    if 'date' in df.columns:
        df = df.drop(columns=['date'])

    # Compute correlation
    correlation_series = df.corr()[column_name]

    # Drop the correlation of the column with itself
    correlation_series = correlation_series.drop(column_name)

    # Get the top n correlations
    top_n_correlation = correlation_series.abs().sort_values(ascending=False).head(top_n)

    # Plot correlation
    plt.figure(figsize=(10, 6))
    bars = top_n_correlation.plot(kind='bar', color='skyblue')
    plt.title(f'Top {top_n} Correlations of {column_name} with other columns')
    plt.xlabel('Columns')
    plt.ylabel('Correlation coefficient')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add correlation values on top of the bars
    for bar in bars.patches:
        plt.annotate(format(bar.get_height(), '.2f'),
                     (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     ha='center', va='center',
                     size=10, xytext=(0, 8),
                     textcoords='offset points')

    plt.show()
    return top_n_correlation


