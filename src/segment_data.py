import pandas as pd
from datetime import timedelta

def segment_customers(df):
    """
    This function creates customer segmentation based on customer recency, frequency, and monetary value scores.
    """

    # Create a hypothetical snapshot date
    print("-" * 80)
    print('Creating hypothetical snapshot date...')
    snapshot_date = df['date'].max() + timedelta(days=1)
    print(f'Hypothetical snapshot date of {snapshot_date} created')

    # Calculate RFM metrics
    print("-" * 80)
    print('Calculating RFM metrics...')
    rfm = df.groupby(['customer_id']).agg({
        'date': lambda x: (snapshot_date - x.max()).days,
        'invoice': 'nunique',
        'total_order_value': 'sum'})

    # Rename columns
    rfm.rename(columns={
        'date': 'recency',
        'invoice': 'frequency',
        'total_order_value': 'monetary_value'}, inplace=True)
    print('RFM metrics calculated')

    # Group the customers into tertiles based on each of the RFM metrics and assign labels
    print("-" * 80)
    print('Grouping customers into tertiles for each RFM metric...')
    recency_tertiles = pd.qcut(rfm['recency'], q=3, labels=range(3, 0, -1))
    rfm['R'] = recency_tertiles

    frequency_tertiles = pd.qcut(rfm['frequency'], q=3, labels=range(1, 4))
    rfm['F'] = frequency_tertiles

    monetary_tertiles = pd.qcut(rfm['monetary_value'], q=3, labels=range(1, 4))
    rfm['M'] = monetary_tertiles
    print('Grouping customers into tertiles completed')

    # Build RFM segments and calculate RFM scores
    print("-" * 80)
    print('Building RFM segments and calculating RFM scores...')
    cols = ['R', 'F', 'M']
    rfm['rfm_segment'] = rfm[cols].astype(str).apply(''.join, axis=1)
    rfm['rfm_score'] = rfm[cols].sum(axis=1)
    print('RFM segments created and RFM scores calculated')

    # segment customers based on RFM scores
    print("-" * 80)
    print('Segmenting customers into named segments based on RFM scores...')
    rfm.loc[rfm['rfm_score'] == 3, 'customer_segment'] = 'Inactive customers'
    rfm.loc[rfm['rfm_score'] == 4, 'customer_segment'] = 'Customers at risk'
    rfm.loc[rfm['rfm_score'].between(5, 6, inclusive='both'), 'customer_segment'] = 'Unsteady customers'
    rfm.loc[rfm['rfm_score'].between(7, 8, inclusive='both'), 'customer_segment'] = 'Active customers'
    rfm.loc[rfm['rfm_score'] == 9, 'customer_segment'] = 'Top-performing customers'
    print('Segmenting customers into named segments completed')

    # create marketing campaign strategies based on customer segments
    print("-" * 80)
    print('Creating campaign strategies based on customer segments...')
    rfm.loc[rfm['customer_segment'] == 'Top-performing customers', 'campaign_strategy'] = 'Send birthday and anniversary cards\
        with discount vouchers. Create a referral program where customers can get discounts on the first purchase of their \
        referrals.'
    rfm.loc[rfm['customer_segment'] == 'Active customers', 'campaign_strategy'] = 'Create loyalty rewards program where \
        customers can earn points for every purchase and convert these points into discount or voucher.'
    rfm.loc[rfm['customer_segment'] == 'Unsteady customers', 'campaign_strategy'] = "Send emails with discounted or \
        promotional items for every occasion, including birthdays, Mother's Day, Father's Day, and Christmas."
    rfm.loc[rfm['customer_segment'] == 'Customers at risk', 'campaign_strategy'] = 'Send personalized emails containing \
        promotional items or free samples to encourage them to be more active.'
    rfm.loc[rfm['customer_segment'] == 'Inactive customers', 'campaign_strategy'] = 'Send personalized emails containing special offers\
        with discounted or free items to encourage them to order and be active.'
    print('Campaign strategies based on customer segments created')

    # reset index
    rfm = rfm.reset_index()

    # Create a customer_segment dataframe to only include customer id, customer segment, and campaign strategy columns
    print("-" * 80)
    print('Creating a customer_segments dataframe to only include customer id, customer segment, and campaign strategy columns...')
    customer_segments = rfm[['customer_id', 'customer_segment', 'campaign_strategy']]
    print('customer_segments dataframe created')
    print("Shape of customer_segments dataframe:", customer_segments.shape)
    print("-" * 80)

    #  Load the rfm dataframe as a csv file to local folder
    print("Loading rfm dataframe as csv file to local folder...")
    path = "data\customer_rfm.csv"
    rfm.to_csv(path, index=False)
    print(f"rfm dataframe loaded to {path}")
    print("-" * 80)

    # load customer segmentation data as a csv file to local folder
    print("Loading customer_segments data as csv file to local folder...")
    path = 'data\customer_segments.csv'
    customer_segments.to_csv(path, index=False)
    print(f"customer_segments dataframe loaded to {path}")
    print("-" * 80)
