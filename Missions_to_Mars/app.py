from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_costa

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

@app.route("/")
def home():

    destination_data = mongo.db.collection.find_one()

    return render_template("index.html", vacation=destination_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    costa_data = scrape_costa.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, costa_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
