# News_archive
News-database that is regularly updated

## What does it do
 - Crawl url: https://www.spiegel.de/international/
 - Extract News-Entries from HTML
    * Title
    * Sub-Title
    * Abstract
    * Download-time 
 -  Store these entries in a Postgresql database
 -  The crawler is triggered to run automatically every 15 minutes
 -  During re-runs, existing entries are detected and not stored as duplicates, but an additional timestamp is stored: update-time

News page example:
![example](https://sun9-61.userapi.com/c853428/v853428060/13502b/K22N4RGYelQ.jpg)

Database screenshot:
![database look](https://sun9-29.userapi.com/c853428/v853428960/131b65/hcetUa5gGI4.jpg)

## How to run

1. Install Python 3.6

 - Ubuntu (17.10 and above): installed by defaullt
  
 - Ubuntu (16.10 and lower):
  ```
$ sudo apt-get update
$ sudo apt-get install python3.6
  ```
 - Windows: navigate to [Download page](https://www.python.org/downloads/windows/) and run installer

2. Install necessary libraries
  ```
$ pip install psycopg2
$ pip install psycopg2.extras
$ pip install requests
$ pip install datetime
$ pip install timeloop
$ pip install bs4
  ```

3. Install pgAdmin4
 - Ubuntu: 
  ``` 
$ sudo apt-get install pgadmin4
  ```
 - Windows: navigate to [Download page](https://www.pgadmin.org/download/)
 
 Note: port = "5433", user="postgres", password="12345"
 
 4. Create database:
  - open the SQL Shell
  - write the command
  
    ``` 
    $ CREATE DATABASE news_archive
    ```
  -connect to a Database using the command
      ``` 
    $ \c news_archive
    ```
   
   5. Run the script 
 - go to the folder with crawler.py using command line
    ``` 
    $ cd folder_path
    ```
    
  - run the script
    
    ``` 
    $ python crawler.py
    ```
  - look throw the database using SQL Shell
     ``` 
    $ show tables
    $ select news_archive
    ```
