### Recipe Scraper 

A CRUD web app made in Flask that allows a user to add and delete recipe URLs, store them in a SQLAlchemy (SQLite) database, update and view the ingredients list. The web app routes to a Python script that utilises BeautifulSoup and requests for web scraping the URLs.
The script uses the schema.org convention to extract a "recipeIngredient" list or dict from recipe websites.

This project uses uv to manage the Python version and dependencies, before running use

```
uv sync
source .venv/bin/activate
```
for macOS and Linux, and:


```
uv sync
.venv\Scripts\activate
```
for Windows.



*** Running just the scraper: ***
```
uv run script.py
```

*** Running the Flask app ***
```
uv run app.py
```