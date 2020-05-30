# Project: Data Lake

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description

In this project, you'll apply what you've learned on Spark and data lakes to build an ETL pipeline for a data lake hosted on S3. To complete the project, you will need to load data from S3, process the data into analytics tables using Spark, and load them back into S3. You'll deploy this Spark process on a cluster using AWS.

### How to run

- To run this project in local mode, create a file  `dl.cfg`  in the root of this project with the following data:

```
KEY=YOUR_AWS_ACCESS_KEY
SECRET=YOUR_AWS_SECRET_KEY
```

Create an S3 Bucket in AWS account for reading input data and writing back output data.

Finally, run the following command:
`python etl.py`

- To run on an Jupyter Notebook powered by an EMR cluster, import the notebook found in this project.

## Project structure

The files found at this project are the following:

-   dl.cfg:  File storing AWS accesskey and secret access keys. 
-   etl.py: Program that extracts songs and log data from S3, transforms it using Spark, and loads the dimensional tables created in parquet format back to S3.
-   README.md: Contains detailed information about the project.

## ETL pipeline

1.  Load credentials    
2.  Read data from S3    
    -   Song data:  `s3://udacity-dend/song_data`
    -   Log data:  `s3://udacity-dend/log_data`
    
    The script reads song_data and log_data from S3.    
3.  Process data using spark
    
    Transforms them to create five different tables listed under  `Dimension Tables and Fact Table`. Each table includes the right columns and data types. Duplicates are addressed where appropriate.
    
4.  Load it back to S3    
    Writes them to partitioned parquet files in table directories on S3.
    
    Each of the five tables are written to parquet files in a separate analytics directory on S3. Each table has its own folder within the directory. Songs table files are partitioned by year and then artist. 
    Time table files are partitioned by year and month. 
    Songplays table files are partitioned by year and month.
    

## Source Data

-   **Song datasets**: all json files are nested in subdirectories under  _s3a://udacity-dend/song_data_. A sample of this files is:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

-   **Log datasets**: all json files are nested in subdirectories under  _s3a://udacity-dend/log_data_. A sample of a single row of each files is
```
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}
```

### Dimension Tables and Fact Table

**songplays**  - Fact table - records in log data associated with song plays i.e. records with page NextSong

-   songplay_id (int) PRIMARY KEY: ID of each user song play
-   start_time (date) NOT NULL: Timestamp of beginning of user activity
-   user_id (int) NOT NULL: ID of user
-   level (text): User level {free | paid}
-   song_id (text) NOT NULL: ID of Song played
-   artist_id (text) NOT NULL: ID of Artist of the song played
-   session_id (int): ID of the user Session
-   location (text): User location
-   user_agent (text): Agent used by user to access Sparkify platform

**users**  - users in the app

-   user_id (int) PRIMARY KEY: ID of user
-   first_name (text) NOT NULL: Name of user
-   last_name (text) NOT NULL: Last Name of user
-   gender (text): Gender of user {M | F}
-   level (text): User level {free | paid}

**songs**  - songs in music database

-   song_id (text) PRIMARY KEY: ID of Song
-   title (text) NOT NULL: Title of Song
-   artist_id (text) NOT NULL: ID of song Artist
-   year (int): Year of song release
-   duration (float) NOT NULL: Song duration in milliseconds

**artists**  - artists in music database

-   artist_id (text) PRIMARY KEY: ID of Artist
-   name (text) NOT NULL: Name of Artist
-   location (text): Name of Artist city
-   latitude (float): Latitude location of artist
-   longitude (float): Longitude location of artist

**time**  - timestamps of records in songplays broken down into specific units

-   start_time (date) PRIMARY KEY: Timestamp of row
-   hour (int): Hour associated to start_time
-   day (int): Day associated to start_time
-   week (int): Week of year associated to start_time
-   month (int): Month associated to start_time
-   year (int): Year associated to start_time
-   weekday (text): Name of week day associated to start_time