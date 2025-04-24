import pandas as pd

def clean_data(df):
    """
    This function performs the following cleaning tasks:
    1. Remove records where stock_code is C2, DOT, and PADS
    2. Remove records where price is 0.00
    3. Remove records that have pairs of original invoice and matching cancelled invoice
    """

    print("-" * 80)
    print("Shape of data before cleaning:", df.shape)

    # Remove records where stock_code is C2, DOT, and PADS
    print("-" * 80)
    print('Removing records with stock codes C2, DOT, and PADS...')
    alpha_stock_code = ['C2', 'DOT', 'PADS']
    num = len(df[df['stock_code'].isin(alpha_stock_code)])
    df_cleaned = df[~df['stock_code'].isin(alpha_stock_code)]
    print(f'Total of {num} records with stock codes C2, DOT, and PADS removed')

    # Remove records where price is 0.00
    print("-" * 80)
    print('Removing records where price is 0.00...')
    num2 = len(df_cleaned[df_cleaned['price'] == 0])
    df_cleaned = df_cleaned[df_cleaned['price'] != 0]
    print(f'Total of {num2} records where price is 0.00 removed')

    # Remove records with pairs of original invoice and matching cancelled invoice
    print("-" * 80)
    print('Removing records with pairs of original invoice and matching cancelled invoice...')
    idx = df_cleaned.groupby([df_cleaned.customer_id, df_cleaned.stock_code, df_cleaned.quantity.abs()]) \
        .filter(lambda x: (len(x.quantity.abs()) % 2 == 0) and (x.quantity.sum() == 0)).index
    num3 = len(idx)
    df_cleaned = df_cleaned.drop(idx)
    print(f'Total of {num3} records with pairs of original invoice and matching cancelled invoice removed')

    # Extract date, period, day, hour and create individual columns
    print("-" * 80)
    print('Extracting date, period, dow, and hour from invoice date...')
    df_cleaned['date'] = pd.to_datetime(df_cleaned['invoice_date']).dt.date
    df_cleaned['period'] = df_cleaned['invoice_date'].dt.to_period('M')
    df_cleaned['dow'] = df_cleaned['invoice_date'].dt.day_name()
    df_cleaned['hour'] = df_cleaned['invoice_date'].dt.hour
    print('Additional columns for date, period, dow, and hour created')
    print("-" * 80)

    print("Shape of data after cleaning:", df_cleaned.shape)
    print("-" * 80)

    return df_cleaned