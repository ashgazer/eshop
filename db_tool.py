import psycopg2


def db_connection():
    conn_string = "host='localhost' dbname='dvdrental' user='ashik'"
    conn = psycopg2.connect(conn_string)
    return conn


def copy_to_db(table, file):
    sql = """copy eshop.prices_raw
    from '/Users/ashik.pirmohamed/PycharmProjects/eshop/bucket/eshop_prices.csv'
    DELIMITER ',' CSV;
    commit;
    """

    return sql
