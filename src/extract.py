import psycopg2
import pandas as pd


def connect_to_redshift(dbname, host, port, user, password):
    """Method that connects to redshift."""

    connect = psycopg2.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    )

    print("Connection to redshift made")

    return connect

def extract_data(dbname, host, port, user, password):
    """
    This function connects to redshift and extracts online_transactions_cleaned data
    """

    # connect to redshift
    connect = connect_to_redshift(dbname, host, port, user, password)

    # query to extract online_transactions_cleaned data

    query = """
    SELECT *
    FROM bootcamp.online_transactions_cleaned
    ORDER BY customer_id
    """

    online_trans = pd.read_sql(query, connect)

    print('The shape of online_transactions_cleaned data:', online_trans.shape)

    return online_trans