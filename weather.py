import requests
import json
import schedule
import time

city = "Skopje"
unit = "metric"
api_key = "09a3d48b5d9bbacf39092f134fde8f06"
url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={unit}&appid={api_key}"

def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    return data

def get_temp(data):
    forecast_list = data["list"]
    temp = forecast_list[0]["main"]["temp"]
    feelslike = forecast_list[0]["main"]["feels_like"]
    avg_temp = (float(temp)+float(feelslike))/2
    if avg_temp < 0:
        print("❄️ It’s freezing outside! Wear a heavy winter coat, gloves, and a hat 🧥🧤🧣.")
    elif avg_temp >= 0 and avg_temp < 10:
        print("🧥 Quite chilly. A warm jacket and layers are recommended 🧣🧦.")
    elif avg_temp >= 10 and avg_temp < 20:
        print("🌤️ Mild weather. A light jacket or sweater should be enough 🧥.")
    elif avg_temp >= 20 and avg_temp < 30:
        print("😊 Comfortable and warm. Short sleeves or a T-shirt are perfect 👕.")
    elif avg_temp >= 30 and avg_temp < 40:
        print("🔥 It’s hot outside! Wear breathable clothes, stay hydrated 💧🧢.")
    else:
        print("☀️ Extreme heat alert! Stay indoors if possible, wear lightweight and breathable clothing, drink plenty of water 💦, and avoid strenuous activities 🛑.")

def get_rain(data):
    forecast_list = data["list"]
    if "rain" in forecast_list[0]:
        rain = float(forecast_list[0]["rain"]["3h"])
        if rain < 0.1:
            print(f"🌤️ Almost no rain expected ({rain:.1f} mm). You’re good to go!")
        elif 0.1 <= rain < 1.0:
            print(f"🌦️ Light rain possible ({rain:.1f} mm). You *might* want to bring a small umbrella — just in case.")
        elif 1.0 <= rain < 3.0:
            print(f"🌧️ Moderate rain ahead ({rain:.1f} mm). Don’t forget your umbrella or raincoat!")
        elif 3.0 <= rain < 10.0:
            print(f"🌧️🌧️ Heavy rain expected ({rain:.1f} mm)! Waterproof gear recommended.")
        else:
            print(f"⛈️ Torrential rain alert ({rain:.1f} mm)! Stay safe and dry — avoid unnecessary trips outdoors.")
    else:
        print("☀️ No rain in the forecast — enjoy the sunshine!")

def get_humidity(data):
    forecast_list = data["list"]
    humidity = forecast_list[0]["main"]["humidity"]
    if humidity < 30:
        print(f"🌵 Very dry air today ({humidity}%) — stay hydrated, use lip balm, and maybe a humidifier indoors.")
    elif 30 <= humidity < 50:
        print(f"🌤️ Comfortable humidity at ({humidity}%) — enjoy the fresh air!")
    elif 50 <= humidity < 70:
        print(f"🌫️ Slightly humid today ({humidity}%) — you might feel a little sticky, so dress in breathable clothes.")
    elif 70 <= humidity < 85:
        print(f"💦 It's humid today ({humidity}%) — feels warmer than it is. Stay cool, wear light clothes, and drink plenty of water.")
    else:  # 85% and above
        print(f"🥵 Very high humidity! ({humidity}%) — the air is thick and heavy. Stay indoors if possible, avoid intense activity, and keep hydrated.")

def suggestions(url):
    data = fetch_data(url)
    with open("weather_data.json", "w") as file:
        json.dump(data, file, indent=4)

    get_temp(data)
    get_rain(data)
    get_humidity(data)


schedule.every(3).hours.do(suggestions, url)
while True:
    schedule.run_pending()
    time.sleep(1)
