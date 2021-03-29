from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return  render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data_new = scrape_mars.scrape_mars_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data_new, upsert=True)

    # return "Scraping successful"

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

