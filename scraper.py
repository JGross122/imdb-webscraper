import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def scraper_IMDB():
    database_path_imdb = "resources/imdb_data.db"
    web_url = "https://www.imdb.com/chart/tvmeter"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/117.0.0.0 Safari/537.36"
    }

    print("Fetching data from IMDB...")
    response = requests.get(web_url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to fetch page: ", response.status_code)
        print("Exiting the script...")
        exit()


    soup = BeautifulSoup(html_content, "html.parser")

    rows = soup.select(".ipc-metadata-list-summary-item")

    print("Connecting to " + database_path_imdb + "...")
    con = sqlite3.connect(database_path_imdb)
    cur = con.cursor()
    print("Creating table if not exists...")
    cur.execute("CREATE TABLE IF NOT EXISTS movie(id INTEGER PRIMARY KEY AUTOINCREMENT, title, ranking, date)")

    for row in rows:
        movie_title = row.select_one(".ipc-title-link-wrapper .ipc-title__text")
        movie_rating = row.select_one(".ipc-rating-star--rating")
        movie_data = movie_title.text + ", " + movie_rating.text

        title = movie_title.text if movie_title else "N/A"
        rating = movie_rating.text if movie_rating else "N/A"
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        
        cur.execute("INSERT INTO movie (title, ranking, date) VALUES (?, ?, ?)", 
                (title, rating, date))
    
    print("Comitting to " + database_path_imdb + "...")
    con.commit()
    print("Closing " + database_path_imdb + "...")
    #con.close()

    print("Database:")
    cur.execute("SELECT * FROM movie")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    con.close()

scraper_IMDB()

# todo:
# switch from txt files to sqlite3