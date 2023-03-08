import os
import sys
from datetime import datetime
import requests
import psycopg2 as pg2
import pyshorteners as pysh
from bs4 import BeautifulSoup
from pyshorteners.exceptions import ShorteningErrorException

SEZNAM_URL = "https://seznam.cz/"
DEFAULT_PATH = "digest.txt"


def get_response_text():
    """Connect with the website."""
    response = requests.get(SEZNAM_URL)
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching: {response.status_code},"
                           f" check the website and try again")
    return response.text


def prepare_data(text):
    """Create a dictionary from the raw data
    to be the source for the following functions."""
    raw_data = BeautifulSoup(text, "html.parser")
    enhanced_data = raw_data.select(".article__title")
    final_data = {}
    for index, item in enumerate(enhanced_data):
        title = enhanced_data[index].getText()
        link = enhanced_data[index].get("href", None)
        final_data.update({title: link})
    return final_data


def gather_env_var():
    """Gather environment variables needed to connect with a local database."""
    db_name = os.environ.get("PGDATABASE")
    username = os.environ.get("PGUSER")
    userpass = os.environ.get("PGPASSWORD")
    if not all((db_name, username, userpass)):
        raise RuntimeError(
            """
            Enter the command with PGDATABASE, PGUSER, 
            and PGPASSWORD included and try again.
            """
        )
    return db_name, username, userpass


def create_table():
    return ("""CREATE TABLE IF NOT EXISTS titles (
            line_id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            url VARCHAR UNIQUE NOT NULL,
            request_time TIMESTAMP NOT NULL
            )""")


def titles_database(final_data):
    """Add information into the PostgreSQL database, ignore duplicates."""
    db_name, username, userpass = gather_env_var()
    conn = pg2.connect(database=db_name, user=username, password=userpass)
    curs = conn.cursor()
    curs.execute(create_table())
    for title, link in final_data.items():
        insert = """INSERT INTO titles(title, url, request_time)
                    VALUES (%s, %s, %s)
                    ON CONFLICT(url) DO NOTHING;"""
        values = (title, link, datetime.now())
        curs.execute(insert, values)
    conn.commit()
    curs.close()
    conn.close()


def titles_digest(final_data, path):
    """Create a digest of the current articles on the main page of seznam.cz.
    Shorten the urls for the better readability."""
    count_lines = 0
    count_errors = 0
    with open(path, "w") as file:
        for title, link in final_data.items():
            count_lines += 1
            try:
                link = pysh.Shortener().tinyurl.short(link)
            except ShorteningErrorException:
                count_errors += 1
            file.write(title + ": " + link + "\n")

    print(f"The digest contains {count_lines} current news titles.")
    if count_errors:
        print(f"{count_errors} url(s) cannot be shortened.")
    else:
        print("All urls have been shortened.")


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        path = DEFAULT_PATH

    text = get_response_text()
    final_data = prepare_data(text)
    gather_env_var()
    titles_database(final_data)
    titles_digest(final_data, path)


if __name__ == '__main__':
    main()
