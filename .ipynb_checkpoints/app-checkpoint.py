# Import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create variable for our connection string
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():
    
    mars_data = mongo.db.mars_data.find_one()
    
    # Return template and data
#    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
