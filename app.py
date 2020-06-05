from flask import Flask, jsonify, make_response, render_template
from sReddit import RedditScraper
import json

app = Flask(__name__)


@app.route('/<int:check>', methods=['GET'])
def index(check):
    redditScraper = RedditScraper(check)
    redditData = redditScraper.scrape()
    return render_template("pennystock.htm", data=redditData, length=check)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
