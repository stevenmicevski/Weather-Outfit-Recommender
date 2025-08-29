from flask import Flask, render_template
import weather
from datetime import datetime

#creating a Flask app
app = Flask(__name__)

#making a route for the app on the home page (/)
@app.route("/")
def home():
    # weather.fetch_data()
    # weather.store_data()
    hourly_suggestions = weather.give_suggestions()
    daily_values = weather.get_values()

    # Combine hourly suggestions with the corresponding datetime
    combined = []
    for hour, value in zip(hourly_suggestions, daily_values):
        hour_copy = hour.copy()
        date_str = value.get("date")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            hour_copy["time"] = dt.strftime("%H:%M")
        else:
            hour_copy["time"] = "N/A"
        combined.append((hour_copy, value))

    return render_template("home.html", combined=combined)

if __name__ == "__main__":
    app.run(debug=True)
