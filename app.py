from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa_data"
mongo = PyMongo(app)


@app.route("/")
def home():
    scrap_data = mongo.db.nasaData.find_one()
    return render_template("index.html", listings=scrap_data)


# Set path to /scrape
@app.route("/scrape")
def scraper():
    nasatable = mongo.db.nasaData
    mongo.db.nasaData.drop()
    
    # update the listings with the data that is being scraped
    listings_data = scrape_mars.scrape()
    nasatable.update_one({}, {"$set": listings_data}, upsert=True)
    
    # return a message to our page so we know it was successful
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
