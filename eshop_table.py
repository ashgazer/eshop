import datetime
import psycopg2
import csv

import pandas as pd
from request_object import get_html
from db_tool import db_connection, copy_to_db


def clean_eshop_dataframe(data):
    df_prices = data[0]
    df_prices.rename(columns={df_prices.columns[0]: "Name"}, inplace=True)
    df2 = df_prices.fillna('10000')

    for x in df2:

        if x != 'Name':
            df2[x] = df2[x].apply(lambda x: float(x.replace('£', '')))

    min_price = df2.loc[:, 'ARG':].min(axis=1)
    min_col = df2.loc[:, 'ARG':].idxmin(axis=1)

    min_df = pd.merge(min_col.to_frame(), min_price.to_frame(), left_index=True, right_index=True)
    end_df = pd.merge(df2, min_df, left_index=True, right_index=True)
    end_df = end_df[['Name', '0_x', '0_y']]
    end_df.columns = ['Name', 'Country', 'Price']
    end_df['currency'] = 'GBP'
    end_df['etl_tstamp'] = datetime.datetime.now()

    return end_df


def main():
    url = "https://eshop-prices.com/?currency=GBP"
    bucket_location = "./bucket/"

    r_object = get_html(url)
    eshop_data = pd.read_html(r_object.text)

    final_df = clean_eshop_dataframe(eshop_data)

    final_df.to_csv("".join([bucket_location, 'eshop_prices.csv']), index=False, header=False,
                    quoting=csv.QUOTE_NONNUMERIC)

    conn = db_connection()

    cursor = conn.cursor()
    cursor.execute(copy_to_db("", ""))
    conn.close()


if __name__ == '__main__':
    main()
