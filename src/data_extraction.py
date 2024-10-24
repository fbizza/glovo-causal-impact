import trino
import pandas as pd
from queries import sql_queries
import matplotlib.pyplot as plt
import os

# Set up DB connection
HOST = 'starburst.g8s-data-platform-prod.glovoint.com'
PORT = 443
conn_details = {
    'host': HOST,
    'port': PORT,
    'http_scheme': 'https',
    'auth': trino.auth.OAuth2Authentication()
}

DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data')
BASE_DF_FILE = os.path.join(DATA_FOLDER, 'base_df.csv')


def execute_query(sql_query):
    with trino.dbapi.connect(**conn_details) as conn:
        df = pd.read_sql_query(sql_query, conn)
    return df


def save_df(df, file_path):
    df.to_csv(file_path, index=False)


def load_df(file_path):
    return pd.read_csv(file_path)


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_base_df(query_names, reload_data=False):
    create_directory_if_not_exists(DATA_FOLDER)

    if not reload_data and os.path.exists(BASE_DF_FILE):
        print("Loading existing DataFrame from file.")
        return load_df(BASE_DF_FILE)

    print("Creating new DataFrame from queries.")
    dataframes = []
    for query_name in query_names:
        sql_query = getattr(sql_queries, query_name)
        df = execute_query(sql_query)
        dataframes.append(df)

    base_df = dataframes[0]
    for df in dataframes[1:]:
        base_df = pd.merge(base_df, df, on='date')

    save_df(base_df, BASE_DF_FILE)
    return base_df


def plot_orders_evolution(base_df, rolling_mean_value, start_date, end_date, plot_type='both'):
    base_df['date'] = pd.to_datetime(base_df['date'])
    base_df = base_df.sort_values(['date'])

    plt.figure(figsize=(14, 8))
    plt.rcParams.update({'font.size': 10})

    for column in base_df.columns:
        if column != 'date':
            base_df[f'{column}_rolling_mean'] = base_df[column].rolling(rolling_mean_value).mean()

            if plot_type in ['both', 'normal']:
                plt.plot(base_df['date'], base_df[column], linewidth=1.5, label=f'{column}')

            if plot_type in ['both', 'rolling']:
                plt.plot(base_df['date'], base_df[f'{column}_rolling_mean'], linewidth=2,
                         label=f'{rolling_mean_value}D rolling average for {column}')

    max_value = base_df.drop(columns=['date']).max().max()

    plt.axvline(x=pd.Timestamp(start_date), color='#F2CC38', linestyle='--', linewidth=2)
    plt.text(pd.Timestamp(start_date), max_value, 'Start', color='black', rotation=90, verticalalignment='bottom')

    plt.axvline(x=pd.Timestamp(end_date), color='red', linestyle='--', linewidth=2)
    plt.text(pd.Timestamp(end_date), max_value, 'End', color='black', rotation=90, verticalalignment='bottom')

    plt.legend()
    plt.title('KPI Evolution')
    plt.show()


# Example usage
query_names = ['waw_daily_orders', 'gdn_daily_orders']
base_df = create_base_df(query_names, reload_data=False)  # Set reload_data=True to reload and save new data
plot_orders_evolution(base_df, rolling_mean_value=14, start_date='2024-09-01', end_date='2024-09-30',
                      plot_type='normal')