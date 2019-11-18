from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Creates a Mongo DB to hold the scraped data
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_app"

mongo = PyMongo(app)

# Drops collection if available to remove duplicates

@app.route("/")
def index():
    mars_data_web = mongo.db.mars_data_coll.find_one()
    return render_template("index.html", mars_data_web=mars_data_web)


@app.route("/scrape")
def scraper():
    mars_data_db = mongo.db.mars_data_coll
    mars_data_coll = scrape_mars.scrape()
    mars_data_db.update({}, mars_data_coll, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

