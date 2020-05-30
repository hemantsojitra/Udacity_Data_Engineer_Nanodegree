import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

# Read Config File
config = configparser.ConfigParser()
config.read_file(open('dl.cfg'))

# Read config file properties for aws connection
os.environ['AWS_ACCESS_KEY_ID']=config.get('AWS','AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('AWS','AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    
    """
        Description: Create or retrieve a Spark Session and Import spark jar packages
    """    
    
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    
    return spark

def process_song_data(spark, input_data, output_data):
    
    """
        Description: Load song data from S3, Transform it and load it back to S3
        Parameters: 
            spark: Spark Session
            input_data: Location of json file in S3 bucket
            output_data: Location in S3 bucket where parquet format file will get store
    """
    
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)
    
    # created song view to write SQL Queries
    df.createOrReplaceTempView("song_data_table")

    # extract columns to create songs table
    songs_table = spark.sql("""
                            SELECT DISTINCT sdtn.song_id, 
                            sdtn.title,
                            sdtn.artist_id,
                            sdtn.year,
                            sdtn.duration
                            FROM song_data_table sdtn
                            WHERE song_id IS NOT NULL
                        """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(output_data + 'songs/')

    # extract columns to create artists table
    artists_table = spark.sql("""
                                SELECT DISTINCT arti.artist_id, 
                                arti.artist_name,
                                arti.artist_location,
                                arti.artist_latitude,
                                arti.artist_longitude
                                FROM song_data_table arti
                                WHERE arti.artist_id IS NOT NULL
                            """)    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data + 'artists/')

def process_log_data(spark, input_data, output_data):
    
    """
        Description: Load log data from S3, Transform it and load it back to S3
        Parameters: 
            spark: Spark Session
            input_data: Location of json file in S3 bucket
            output_data: Location in S3 bucket where parquet format file will get store
    """
    
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_data) 
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')
    
    # Create log table after filtering where page is equal to Nextsong
    df.createOrReplaceTempView("log_data_table")

    # extract columns for users table    
    users_table = spark.sql("""
                            SELECT DISTINCT userT.userId as user_id, 
                            userT.firstName as first_name,
                            userT.lastName as last_name,
                            userT.gender as gender,
                            userT.level as level
                            FROM log_data_table userT
                            WHERE userT.userId IS NOT NULL
                        """)
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + 'users/')

    # create timestamp column from original timestamp column
    time_table = spark.sql("""
                            SELECT DISTINCT
                            A.start_time_sub as start_time,
                            hour(A.start_time_sub) as hour,
                            dayofmonth(A.start_time_sub) as day,
                            weekofyear(A.start_time_sub) as week,
                            month(A.start_time_sub) as month,
                            year(A.start_time_sub) as year,
                            dayofweek(A.start_time_sub) as weekday
                            FROM
                            (SELECT to_timestamp(timeSt.ts/1000) as start_time_sub
                            FROM log_data_table timeSt
                            WHERE timeSt.ts IS NOT NULL
                            ) A
                        """)

    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'time/')
    
    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + 'songs/')

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
                                SELECT DISTINCT
                                monotonically_increasing_id() as songplay_id,
                                to_timestamp(log.ts/1000) as start_time,
                                month(to_timestamp(log.ts/1000)) as month,
                                year(to_timestamp(log.ts/1000)) as year,
                                log.userId as user_id,
                                log.level as level,
                                song.song_id as song_id,
                                song.artist_id as artist_id,
                                log.sessionId as session_id,
                                log.location as location,
                                log.userAgent as user_agent
                                FROM log_data_table log JOIN song_data_table song on log.artist = song.artist_name 
                                                                                   and log.song = song.title
                            """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'songplays_table/')

def main():
    
    """
    Description: Load song and log data from S3, Transform it and load it back to S3
    """             
                    
    spark = create_spark_session()
    input_data = "/home/workspace/data/"
    output_data = "/home/workspace/output/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()