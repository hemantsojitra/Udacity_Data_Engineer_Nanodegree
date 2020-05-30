# Project Data Warehouse

## Project Description
Sparkify is a music streaming startup with a growing user base and song database.

Their user activity and songs metadata data resides in json files in S3. The goal of the current project is to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

## Project Datasets
|Dataset Name      |       S3 Bucket Name          
|-------------------|-------------------------------
|Song Data Path     |`s3://udacity-dend/song_data`            
|Log Data Path      |`s3://udacity-dend/log_data`            
|Log Data JSON Path |`s3://udacity-dend/log_json_path.json`

## Project structure
Below is description of each file content :

##### create_cluster.py : 
This script will spin up cluster programmatically using infrastructure as code methodology. It would also create IAM role linked to cluster having access to S3 Bucket for copying data from.
##### sql_queries.py
Script define syntaxes drop table, create table, copy table and delete table. This script is being called by create_table.py and etl.py
##### create_table.py 
Script is having drop tables if exist and recreate new fact and dimension tables for the star schema in Redshift.
##### etl.py 
Script loads data from S3 bucket in to staging tables on Redshift and then transformed data.
##### README.md
Providing details about project description, structure, implementation and execution steps.

## Database schema design
State and justify your database schema design and ETL pipeline.

#### Staging Tables
- staging_events
- staging_songs

#### Fact Table
- songplays - records in event data associated with song plays i.e. records with page NextSong 
- Columns: songplay_id, start_time, - user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables
- users - users in the app 
users columns: user_id, first_name, last_name, gender, level

- songs - songs in music database 
songs columns: song_id, title, artist_id, year, duration

- artists - artists in music database 
artists columns: artist_id, name, location, lattitude, longitude

- time - timestamps of records in songplays broken down into specific units 
time columns: start_time, hour, day, week, month, year, weekday

## Steps followed on this project

#### Create Table Schemas
 - Design schemas for your fact and dimension tables
- Write SQL DROP statements to drop tables in the beginning of - create_tables.py if the tables already exist. This way, when create_tables.py get executed it reset database first.
- Write a SQL CREATE statement for each of these tables in sql_queries.py
- Complete the logic in create_tables.py to connect to the database and create these tables
- Launch a redshift cluster and create an IAM role that has read access to S3.
- Add redshift database and IAM role info to dwh.cfg.
- Test by running create_tables.py and checking the table schemas in your redshift database. 

#### Build ETL Pipeline
- Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
- Test by running etl.py after running create_tables.py on Redshift database.
- Delete redshift cluster when finished.

#### Document Process Do the following steps in your README.md file.
- Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
- State and justify your database schema design and ETL pipeline

## Step taken to execute project
#####  1. Update dwh.cfg file to read properties of various variable.
#####  2. Run the create_cluster script to set up the needed infrastructure for this project.
$ python create_cluster.py
#####  3. Run the create_tables script to set up the database staging and analytical tables
$ python create_tables.py
#####  4. Finally, run the etl script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables.
$ python etl.py