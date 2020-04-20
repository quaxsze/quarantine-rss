import os
import time

import feedparser
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup


app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

FEEDS = [
    {
        'id': 1,
        'title': 'Numerama',
        'url': 'https://www.numerama.com/feed/'
    },
    {
        'id': 2,
        'title': 'Journal du hacker',
        'url': 'https://www.journalduhacker.net/rss'
    },
    {
        'id': 3,
        'title': 'Sam & Max',
        'url': 'http://sametmax.com/feed/rss/'
    },
    {
        'id': 4,
        'title': 'Hacker News',
        'url': 'https://hnrss.org/frontpage'
    },
    {
        'id': 5,
        'title': 'sebsauvage',
        'url': 'http://sebsauvage.net/links/index.php?do=rss'
    },
    {
        'id': 6,
        'title': 'korben',
        'url': 'https://korben.info/feed'
    },
    {
        'id': 7,
        'title': 'journaldugeek',
        'url': 'https://www.journaldugeek.com/feed/rss/'
    }
]


@app.route("/api/feeds", methods=['GET'])
def get_feeds():
    return jsonify(FEEDS)


@app.route("/api/feeds/<feed_id>", methods=['GET'])
def get_specific_feed(feed_id):
    res = list()

    for f in FEEDS:
        if f['id'] == int(feed_id):
            feed_url = f['url']

    parsed = feedparser.parse(feed_url)
    for entry in parsed['entries']:
        res_dict = {
            'title': entry['title'],
            'link': entry['link'],
        }

        parsed_date = entry['published_parsed']
        format_date = time.strftime('%d %B, %Y', parsed_date)
        res_dict.update({
                'publish_date': format_date
            })

        try:
            soup = BeautifulSoup(entry['content'][0]['value'])
            img_html = soup.find('img')
            if img_html:
                res_dict.update({
                    'img_src': img_html.get("src")
                })
        except KeyError:
            pass

        res.append(res_dict)
    return jsonify(res)


@app.route("/", defaults={"path": ""})
# allows routing in vuejs
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")
