from socket import timeout
import requests
import json
import database
from plyer import notification
import time

city = "YOUR_CITY_HERE"
unit = "metric"
api_key = "YOUR_API_KEY_HERE"
url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={api_key}"

def fetch_data():
    response = requests.get(url)
    data = response.json()
    with open("weather_data.json", "w") as file:
        json.dump(data, file, indent=4)


def store_data():
    with open("weather_data.json", "r") as file:
        data = json.load(file)

    database.create_table()
    database.delete_weather_data()

    for entry in data["list"]:
        temperature = entry["main"]["temp"]
        feelslike = entry["main"]["feels_like"]
        rain = 0
        if "rain" in entry:
            rain = entry["rain"]["3h"]
        humidity = entry["main"]["humidity"]
        condition = entry["weather"][0]["main"]
        datetime = entry["dt_txt"]
        database.insert_weather_data(temperature, feelslike, rain, humidity, condition, datetime)

def get_data():
    rows = database.show_weather_data()
    return rows

def give_suggestions():
    row = get_data()
    temp = row[1]
    feels = row[2]
    rain = row[3]
    humidity = row[4]
    condition = str(row[5])

    message = ""
    if temp < 0:
        message += f"\n❄️ It’s freezing outside! Temp: {temp}°C, feels like {feels}°C. Wear a heavy winter coat, gloves, and a hat 🧥🧤🧣."
    elif 0 <= temp < 10:
        message += f"\n🧥 Quite chilly. Temp: {temp}°C, feels like {feels}°C. A warm jacket and layers are recommended 🧣🧦."
    elif 10 <= temp < 20:
        message += f"\n🌤️ Mild weather. Temp: {temp}°C, feels like {feels}°C. A light jacket or sweater should be enough 🧥."
    elif 20 <= temp < 30:
        message += f"\n😊 Comfortable and warm. Temp: {temp}°C, feels like {feels}°C. Short sleeves or a T-shirt are perfect 👕."
    elif 30 <= temp < 40:
        message += f"\n☀️ It’s hot outside! Temp: {temp}°C, feels like {feels}°C. Wear breathable clothes, stay hydrated 💧🧢."
    else:
        message += f"\n🔥 Extreme heat alert! Temp: {temp}°C, feels like {feels}°C. Stay indoors if possible, wear lightweight clothes, drink plenty of water 💦, and avoid strenuous activities 🛑."

    if rain > 0:
        if rain < 0.1:
            message += f"\n🌤️ Almost no rain expected ({rain:.1f} mm). You’re good to go!"
        elif 0.1 <= rain < 1.0:
            message += f"\n🌦️ Light rain possible ({rain:.1f} mm). Bring a small umbrella — just in case."
        elif 1.0 <= rain < 3.0:
            message += f"\n🌧️ Moderate rain ahead ({rain:.1f} mm). Don’t forget your umbrella or raincoat!"
        elif 3.0 <= rain < 10.0:
            message += f"\n🌧️🌧️ Heavy rain expected ({rain:.1f} mm)! Waterproof gear recommended."
        else:
            message += f"\n⛈️ Torrential rain alert ({rain:.1f} mm)! Stay safe and dry — avoid unnecessary trips outdoors."
    else:
        message += "\n☀️ No rain in the forecast — enjoy the sunshine!"

    if humidity < 30:
        message += f"\n🌵 Very dry air today ({humidity}%) — stay hydrated, use lip balm, and maybe a humidifier indoors."
    elif 30 <= humidity < 50:
        message += f"\n🌤️ Comfortable humidity at ({humidity}%) — enjoy the fresh air!"
    elif 50 <= humidity < 70:
        message += f"\n🌫️ Slightly humid today ({humidity}%) — you might feel a little sticky, so dress in breathable clothes."
    elif 70 <= humidity < 85:
        message += f"\n💦 It's humid today ({humidity}%) — feels warmer than it is. Stay cool, wear light clothes, and drink plenty of water."
    else:
        message += f"\n🥵 Very high humidity! ({humidity}%) — the air is thick and heavy. Stay indoors if possible, avoid intense activity, and keep hydrated."


    if condition in ["Clear", "Sunny"]:
        message += "\n☀️ Clear skies today — perfect for outdoor activities!"
    elif condition in ["Clouds", "Cloudy", "Overcast"]:
        message += "\n☁️ Cloudy skies — might be a bit gloomy but still fine for outdoor activities."
    elif condition in ["Rain", "Drizzle"]:
        message += "\n🌧️ Rainy weather — bring an umbrella or wear a raincoat!"
    elif condition in ["Thunderstorm"]:
        message += "\n⛈️ Thunderstorm alert — stay indoors if possible and stay safe!"
    elif condition in ["Snow"]:
        message += "\n❄️ Snowy conditions — dress warmly and be careful on the roads."
    else:
        message += f"\n🌤️ Current condition: {condition} — dress appropriately."


    wear_advice = "\n\n👕 Recommendation: "
    if feels < 0:
        wear_advice += "Heavy winter coat 🧥, layers 🧣, gloves 🧤, hat 🧢"
    elif 0 <= feels < 10:
        wear_advice += "Warm jacket 🧥, sweater layers 🧣, scarf 🧤"
    elif 10 <= feels < 20:
        wear_advice += "Light jacket 🧥 or long-sleeve shirt 👕"
    elif 20 <= feels < 30:
        wear_advice += "T-shirt 👕, breathable top 👚"
    else:
        wear_advice += "Light, airy top 👕, stay hydrated 💧"

    if feels < 0:
        wear_advice += "; thick pants ❄️, thermal leggings 🩳"
    elif 0 <= feels < 10:
        wear_advice += "; warm pants 👖, maybe jeans 🩳"
    elif 10 <= feels < 20:
        wear_advice += "; pants 👖 or skirt 👗 with tights"
    elif 20 <= feels < 30:
        wear_advice += "; light pants 👖, shorts 🩳 optional"
    else:
        wear_advice += "; shorts 🩳, skirt 👗, or breathable trousers 👖"

    if rain >= 0.1:
        wear_advice += ", and take an umbrella ☂️ or raincoat 🌂"

    if humidity >= 70 and feels >= 20:
        wear_advice += " — light fabrics recommended due to humidity 💦"

    if condition in ["Snow"]:
        wear_advice += ", plus waterproof boots 🥾 and warm layers ❄️"

    if condition in ["Clear", "Sunny"] and feels >= 30:
        wear_advice += ", plus sunscreen 🧴, hat 🧢, and sunglasses 🕶️"

    message += wear_advice
    return message

def send_notification_on_desktop():
    notification.notify(
        title="🌤️ Weather & Outfit Advice",
        message=give_suggestions()
    )

fetch_data()
while True:
    send_notification_on_desktop()
    time.sleep(3 * 60 * 60)
