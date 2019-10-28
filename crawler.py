import psycopg2
import psycopg2.extras
import requests
import datetime
from datetime import timedelta
from timeloop import Timeloop
from bs4 import BeautifulSoup

#connecting to database
try:
    conn = psycopg2.connect(port="5433", dbname="news_archive", user="postgres", password="12345")
except:
    print("Cannot connect")
#cursor creating
cursor = conn.cursor()

#define Time Loop
tl = Timeloop()
WAIT_MINUTES = 15

#set url
url = 'https://www.spiegel.de/international/'
#connect to url
response = requests.get(url)
# parse HTML and save to BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")


#create DB
def create_table():
    try:
        # SELECT call to DB
        sql = """CREATE TABLE IF NOT EXISTS news_archive 
            (
             id            serial not null primary key,
             title         varchar(255),
             subtitle      varchar(255),
             abstract      varchar,
             download_time timestamp,
             update_time   timestamp
            );"""
        cursor.execute(sql)
    except:
        print("Error: unable to create")
    conn.commit()

@tl.job(interval=timedelta(minutes = WAIT_MINUTES))
#create valies list
def find_values():
    #look throw teasers
    teasers = soup.findAll('div', attrs={'class': 'teaser'})
    for teaser in teasers:
        #extract values from each teaser
        headline = teaser.find('span', attrs={'class': 'headline'}).text.strip()
        headline = headline.strip("''")
        result = []
        #check if headline already exists at DB
        id = check(headline)
        if id > 0:
            #if exists write update time
            update_table(id)
        else:
            #if not exists make new record
            headline_intro = teaser.find('span', attrs={'class': 'headline-intro'}).text.strip()
            headline_intro = headline_intro.strip("''")

            article_intro = teaser.find('p', attrs={'class': 'article-intro'}).text.strip()
            article_intro = article_intro.strip("''")

            #write values to the list
            result.append(
                {
                    'title': headline,
                    'subtitle': headline_intro,
                    'abstract': article_intro,
                    'download_time': datetime.datetime.utcnow()
                }
            )
        insert_to_table(result)
    print ("DB updated")
    return result

#check if value already exists at DB
def check (value):
    if not value:
        return
    try:
        #SELECT call to DB
        sql = "SELECT COUNT (*) FROM news_archive WHERE title = %s "
        cursor.execute(sql, (value,))
        data = cursor.fetchone()
        if data == (0,):
            #if no records found
            return 0
        else:
            #if some record found get id
            #SELECT call to DB
            sql = "SELECT id FROM news_archive WHERE title = %s "
            cursor.execute(sql, (value,))
            data = cursor.fetchone()[0]
            #return id of record
            return data
    except:
        print("Error: unable to check")

#upate DB
def update_table (value):
    if not value:
        return
    try:
        #UPDATE call to DB
        sql = "UPDATE news_archive SET update_time = %s WHERE id = %s"
        cursor.execute(sql, (datetime.datetime.utcnow(), value))
    except:
        print("Error: unable to update")
    else:
        # save transaction
        conn.commit()

#insert to DB
def insert_to_table(values):
    if not values:
        return
    try:
        # INSERT call to DB
        sql = "INSERT INTO {} ({}) VALUES %s".format('news_archive', ','.join(values[0].keys()))
        #temlate of list
        template = '(' + ', '.join('%({})s'.format(field) for field in values[0].keys()) + ')'
        psycopg2.extras.execute_values(cursor, sql, values, template)
    except:
        print("Error: unable to insert")
    else:
        # save transaction
        conn.commit()

#create new table if not exists
create_table()
#start timer
tl.start(block=True)

#close connection
conn.close()