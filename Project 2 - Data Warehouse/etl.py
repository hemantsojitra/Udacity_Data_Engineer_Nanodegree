import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    
    """
    Load data from file stored in S3 to staging table using sql_quries
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    
    """
    Tranform data from staging tables and load it in different table
    """
    
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    
    """
    - Read dwh configuration files for getting database property
    - Make database connection
    - Load data to staging table by calling load_staging_tables function
    - Transform data from staging table and insert in to another table by calling insert_tables function
    """    
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
        
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
        
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()