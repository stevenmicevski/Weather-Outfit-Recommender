from socket import timeout
import requests
import json
import database
from plyer import notification
import time

city = "your_city"
unit = "metric"
api_key = "your_API_key"
url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={api_key}"

# Fetch weather forecast from OpenWeatherMap API and store it in 'weather_data.json'.
def fetch_data_from_api():
    response = requests.get(url)
    data = response.json()
    with open("weather_data.json", "w") as file:
        json.dump(data, file, indent=4)
    return data

# Read weather data from 'weather_data.json' and store it in the database.
def store_data_in_db():
    with open("weather_data.json", "r") as file:
        data = json.load(file)

    database.create_table()
    database.delete_weather_data()

    for entry in data["list"]:
        temperature = entry["main"]["temp"]
        feelslike = entry["main"]["feels_like"]
        rain = entry.get("rain", {}).get("3h", 0)
        humidity = entry["main"]["humidity"]
        condition = entry["weather"][0]["main"]
        date, time_str = entry["dt_txt"].split()
        database.insert_weather_data(temperature, feelslike, rain, humidity, condition, date, time_str)


def get_data_from_db():
    return database.show_weather_data()


def get_values_from_data():
    rows = get_data_from_db()
    all_daily_values = []

    for r in rows:
        values = {
            "temp": str(round(r[1])),
            "feels": str(round(r[2])) + "°C",
            "humidity": f"{r[4]} %",
            "condition": str(r[5]),
            "date": r[6],
            "time": r[7] if r[7] < '12:00:00' else r[7] + "PM",
        }

        rain = r[3]
        if rain == 0:
            values["rain"] = '0%'
        elif rain < 1:
            values["rain"] = '20%'
        elif rain < 2:
            values["rain"] = '40%'
        elif rain < 5:
            values["rain"] = '60%'
        elif rain < 10:
            values["rain"] = '80%'
        else:
            values["rain"] = '100%'

        all_daily_values.append(values)

    return all_daily_values


def get_temperature_suggestions(temp, feels):
    if temp < 0:
        return f"<span class='text-badge freezing'>❄️ It’s freezing outside — Feels like {feels}°C.</span>"
    elif temp < 10:
        return f"<span class='text-badge cold'>🧥 Quite chilly — Feels like {feels}°C.</span>"
    elif temp < 20:
        return f"<span class='text-badge mild'>🌤️ Mild weather — Feels like {feels}°C.</span>"
    elif temp < 30:
        return f"<span class='text-badge warm'>😊 Comfortable and warm — Feels like {feels}°C.</span>"
    elif temp < 40:
        return f"<span class='text-badge hot'>☀️ It’s hot outside — Feels like {feels}°C.</span>"
    else:
        return f"<span class='text-badge heat'>🔥 Extreme heat alert — Feels like {feels}°C. Stay safe!</span>"


def get_rain_suggestions(rain):
    if rain > 0:
        if rain < 0.1:
            return "<span class='text-badge rain-none'>🌤️ Almost no rain expected. You’re good to go!</span>"
        elif rain < 1.0:
            return "<span class='text-badge rain-light'>🌦️ Light rain possible. Bring a small umbrella — just in case.</span>"
        elif rain < 3.0:
            return "<span class='text-badge rain-moderate'>🌧️ Moderate rain ahead. Don’t forget your umbrella or raincoat!</span>"
        elif rain < 10.0:
            return "<span class='text-badge rain-heavy'>🌧️🌧️ Heavy rain expected! Waterproof gear recommended.</span>"
        else:
            return "<span class='text-badge rain-extreme'>⛈️ Torrential rain alert! Stay safe and dry — avoid unnecessary trips outdoors.</span>"
    return "<span class='text-badge rain-none'>☀️ No rain in the forecast — enjoy the sunshine!</span>"


def get_humidity_suggestions(humidity):
    if humidity < 30:
        return "<span class='text-badge humidity-low'>🌵 Very dry air — stay hydrated.</span>"
    elif humidity < 50:
        return "<span class='text-badge humidity-comfort'>🌤️ Comfortable humidity — enjoy the fresh air!</span>"
    elif humidity < 70:
        return "<span class='text-badge humidity-slight'>🌫️ Slightly humid — dress in breathable clothes.</span>"
    elif humidity < 85:
        return "<span class='text-badge humidity-humid'>💦 It's humid today — feels warmer than it is.</span>"
    else:
        return "<span class='text-badge humidity-extreme'>🥵 Very high humidity! Stay indoors if possible.</span>"


def get_condition_suggestions(condition):
    if condition in ["Clear", "Sunny"]:
        return "<span class='text-badge clear'>☀️ Clear skies today — perfect for outdoor activities!</span>"
    elif condition in ["Clouds", "Cloudy", "Overcast"]:
        return "<span class='text-badge cloudy'>☁️ Cloudy skies — might be a bit gloomy but still fine for outdoor activities.</span>"
    elif condition in ["Rain", "Drizzle"]:
        return "<span class='text-badge rainy'>🌧️ Rainy weather — bring an umbrella or wear a raincoat!</span>"
    elif condition in ["Thunderstorm"]:
        return "<span class='text-badge thunder'>⛈️ Thunderstorm alert — stay indoors if possible and stay safe!</span>"
    elif condition in ["Snow"]:
        return "<span class='text-badge snow'>❄️ Snowy conditions — dress warmly and be careful on the roads.</span>"
    else:
        return f"<span class='text-badge other'>🌤️ Current condition: {condition} — dress appropriately.</span>"


def get_advice_suggestions(feels, rain, humidity, condition):
    advice = []

    # Tops
    if feels < 0:
        advice += ["🧥 Heavy winter coat", "🧣 Layers & scarf", "🧤 Gloves", "🧢 Hat"]
    elif feels < 10:
        advice += ["🧥 Warm jacket", "🧣 Sweater layers", "🧤 Scarf"]
    elif feels < 20:
        advice.append("👕 Light jacket or long-sleeve shirt")
    elif feels < 30:
        advice.append("👕 T-shirt, breathable top")
    else:
        advice.append("👕 Light airy top (stay hydrated 💧)")

    # Bottoms
    if feels < 0:
        advice += ["👖 Thick pants", "🩳 Thermal leggings"]
    elif feels < 10:
        advice.append("👖 Warm pants or jeans")
    elif feels < 20:
        advice.append("👖 Pants or skirt 👗 with tights")
    elif feels < 30:
        advice.append("👖 Light pants or shorts")
    else:
        advice.append("🩳 Shorts, skirt, or breathable trousers")

    # Rain
    if rain >= 0.1:
        advice.append("☂️ Umbrella or raincoat 🌂")

    # Humidity
    if humidity >= 70 and feels >= 20:
        advice.append("💦 Light fabrics for humid weather")

    # Condition
    if condition == "Snow":
        advice.append("🥾 Waterproof boots & warm layers ❄️")
    if condition in ["Clear", "Sunny"] and feels >= 30:
        advice.append("🧴 Sunscreen, hat 🧢, sunglasses 🕶️")

    # Wrap each item in a "badge" style for HTML
    return " ".join([f"<span class='text-badge'>{item}</span>" for item in advice])

# Combine all attribute suggestions into a list of dictionaries for each row.
def get_all_suggestions():
    """Combine all attribute suggestions into a list of dictionaries for each row."""
    rows = get_data_from_db()
    all_daily_suggestions = []

    for r in rows:
        temp = r[1] 
        feels = round(r[2]) 
        rain = r[3] 
        humidity = r[4] 
        condition = str(r[5])
        messages = {
            "temperature": get_temperature_suggestions(temp, feels),
            "rain": get_rain_suggestions(rain),
            "humidity": get_humidity_suggestions(humidity),
            "condition": get_condition_suggestions(condition),
            "advice": get_advice_suggestions(feels, rain, humidity, condition)
        }
        all_daily_suggestions.append(messages)

    return all_daily_suggestions


# Extra function for sending weather notifications on Desktop:
# def send_notification_on_desktop(): 
    # notification.notify(title="🌤️ Weather & Outfit Advice", message=give_suggestions()) 

# if __name__ == "__main__": 
    # while True: 
        # send_notification_on_desktop() 
        # time.sleep(3 * 60 * 60)