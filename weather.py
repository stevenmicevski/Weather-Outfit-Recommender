from socket import timeout
import requests
import json
import database
from plyer import notification
import time

city = ""
unit = "metric"
api_key = ""
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

def get_values():
    rows = get_data()
    daily_values = []
    for r in rows:
        values = {}
        values["temp"] = str(round(r[1])) + " °C"
        values["feels"] = str(round(r[2])) + " °C"
        values["rain"] = str(r[3]) + " mm"
        values["humidity"] = str(r[4]) + " %"
        values["condition"] = str(r[5])
        values["date"] = r[6]  # <-- Add this line to include the datetime
        daily_values.append(values)

    return daily_values

    

def give_suggestions():
    row = get_data()
    day_suggestions = []
    for r in row:
        temp = r[1]
        feels = round(r[2])
        rain = r[3]
        humidity = r[4]
        condition = str(r[5])
        
        messages = {}

        tempmessage = ""
        if temp < 0:
            tempmessage += f"\n❄️ It’s freezing outside! Feels like {feels}°C."
        elif 0 <= temp < 10:
            tempmessage += f"\n🧥 Quite chilly. Feels like {feels}°C."
        elif 10 <= temp < 20:
            tempmessage += f"\n🌤️ Mild weather. Feels like {feels}°C."
        elif 20 <= temp < 30:
            tempmessage += f"\n😊 Comfortable and warm. Feels like {feels}°C."
        elif 30 <= temp < 40:
            tempmessage += f"\n☀️ It’s hot outside! Feels like {feels}°C."
        else:
            tempmessage += f"\n🔥 Extreme heat alert! Stay indoors if possible, wear lightweight clothes, drink plenty of water 💦, and avoid strenuous activities 🛑. Feels like {feels}°C."
        messages ["temperature"] = tempmessage

        rainmessage = ""
        if rain > 0:
            if rain < 0.1:
                rainmessage += f"\n🌤️ Almost no rain expected. You’re good to go!"
            elif 0.1 <= rain < 1.0:
                rainmessage += f"\n🌦️ Light rain possible. Bring a small umbrella — just in case."
            elif 1.0 <= rain < 3.0:
                rainmessage += f"\n🌧️ Moderate rain ahead. Don’t forget your umbrella or raincoat!"
            elif 3.0 <= rain < 10.0:
                rainmessage += f"\n🌧️🌧️ Heavy rain expected! Waterproof gear recommended."
            else:
                rainmessage += f"\n⛈️ Torrential rain alert! Stay safe and dry — avoid unnecessary trips outdoors."
        else:
            rainmessage += "\n☀️ No rain in the forecast — enjoy the sunshine!"
        messages ["rain"] = rainmessage


        hummessage = ""
        if humidity < 30:
            hummessage += f"\n🌵 Very dry air today — stay hydrated, use lip balm, and maybe a humidifier indoors."
        elif 30 <= humidity < 50:
            hummessage += f"\n🌤️ Comfortable humidity — enjoy the fresh air!"
        elif 50 <= humidity < 70:
            hummessage += f"\n🌫️ Slightly humid today — you might feel a little sticky, so dress in breathable clothes."
        elif 70 <= humidity < 85:
            hummessage += f"\n💦 It's humid today — feels warmer than it is. Stay cool, wear light clothes, and drink plenty of water."
        else:
            hummessage += f"\n🥵 Very high humidity! — the air is thick and heavy. Stay indoors if possible, avoid intense activity, and keep hydrated."
        messages ["humidity"] = hummessage

        condmessage = ""
        if condition in ["Clear", "Sunny"]:
            condmessage += "\n☀️ Clear skies today — perfect for outdoor activities!"
        elif condition in ["Clouds", "Cloudy", "Overcast"]:
            condmessage += "\n☁️ Cloudy skies — might be a bit gloomy but still fine for outdoor activities."
        elif condition in ["Rain", "Drizzle"]:
            condmessage += "\n🌧️ Rainy weather — bring an umbrella or wear a raincoat!"
        elif condition in ["Thunderstorm"]:
            condmessage += "\n⛈️ Thunderstorm alert — stay indoors if possible and stay safe!"
        elif condition in ["Snow"]:
            condmessage += "\n❄️ Snowy conditions — dress warmly and be careful on the roads."
        else:
            condmessage += f"\n🌤️ Current condition: {condition} — dress appropriately."
        messages ["condition"] = condmessage

        wear_advice = ""
        if feels < 0:
            wear_advice += "Heavy winter coat 🧥, layers 🧣, gloves 🧤, hat 🧢 <br>"
        elif 0 <= feels < 10:
            wear_advice += "Warm jacket 🧥, sweater layers 🧣, scarf 🧤 <br>"
        elif 10 <= feels < 20:
            wear_advice += "Light jacket 🧥 or long-sleeve shirt 👕 <br>"
        elif 20 <= feels < 30:
            wear_advice += "T-shirt 👕, breathable top 👚 <br>"
        else:
            wear_advice += "Light, airy top 👕, stay hydrated 💧 <br>"

        if feels < 0:
            wear_advice += "Thick pants 👖, thermal leggings 🩳 <br>"
        elif 0 <= feels < 10:
            wear_advice += "Warm pants 👖, maybe jeans 🩳 <br>"
        elif 10 <= feels < 20:
            wear_advice += "Pants 👖 or skirt 👗 with tights <br>"
        elif 20 <= feels < 30:
            wear_advice += "Light pants 👖, shorts 🩳 optional <br>"
        else:
            wear_advice += "Shorts 🩳, skirt 👗, or breathable trousers 👖 <br>"

        if rain >= 0.1:
            wear_advice += " — and take an umbrella ☂️ or raincoat 🌂"

        if humidity >= 70 and feels >= 20:
            wear_advice += " — light fabrics recommended due to humidity 💦"

        if condition in ["Snow"]:
            wear_advice += " — plus waterproof boots 🥾 and warm layers ❄️"

        if condition in ["Clear", "Sunny"] and feels >= 30:
            wear_advice += " — plus sunscreen 🧴, hat 🧢, and sunglasses 🕶️"
        messages ["advice"] = wear_advice

        day_suggestions.append(messages)

    return day_suggestions



# def send_notification_on_desktop():
#     notification.notify(
#         title="🌤️ Weather & Outfit Advice",
#         message=give_suggestions()
#     )

# fetch_data()
# store_data()

# if __name__ == "__main__":
#     while True:
#         send_notification_on_desktop()
#         time.sleep(3 * 60 * 60)

print(get_data())
print(give_suggestions())
print(get_values())