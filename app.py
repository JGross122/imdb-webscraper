from flask import Flask, render_template, request
from scraper import scraper_IMDB
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_scraper", methods=["POST"])
def run_scraper():
    try:
        message = scraper_IMDB()
    except Exception as e:
        message = f"Failed to run scraper: {e}"
    return render_template("success.html", message=message)

@app.route("/history")
def history():
    con = sqlite3.connect("resources/imdb_data.db")
    try:
        cur = con.cursor()
        cur.execute("SELECT id, title, ranking, date FROM movie ORDER BY id DESC")
        rows = cur.fetchall()
    finally:
        con.close()
    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
