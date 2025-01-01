from flask import Blueprint, render_template, jsonify
from src.scraper import TwitterScraper

main = Blueprint('main', __name__)
scraper = TwitterScraper()

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/scrape')
def scrape():
    trends = scraper.get_trends()
    return jsonify(trends)