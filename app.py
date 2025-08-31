from flask import Flask, redirect, render_template, url_for
import weather
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Home page route
@app.route("/")
def home():

    data = weather.fetch_data_from_api()
    if not data or "list" not in data:
        return redirect("/error")

    weather.store_data_in_db()
    suggestions = weather.get_all_suggestions()
    values = weather.get_values_from_data()

    # Combine the suggestions and values so we can loop trough them at once and display them in the HTML
    combined = []
    for sug, val in zip(suggestions, values):
        combined.append((sug, val))

    return render_template("home.html", combined=combined)

# Error page route
@app.route("/error")
def error_page():
    message = "We couldn't fetch the weather data. Please try again later."
    return render_template("error.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
