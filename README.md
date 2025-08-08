# 🌦️ Weather Outlet Recommender

A Python app that fetches 3-hour weather forecasts using the OpenWeatherMap API and recommends outfits and precautions based on **temperature**, **rain**, and **humidity** levels.

---

## 🧠 What It Does

- Connects to OpenWeatherMap API every 3 hours
- Analyzes upcoming temperature, rain, and humidity
- Prints helpful suggestions like:
  - How to dress (e.g., heavy coat or T-shirt)
  - Whether to bring an umbrella
  - When to stay indoors due to high heat or humidity

---

## 🛠️ Tech Stack

- Python
- `requests` – for fetching data from API
- `schedule` – to run the app every 3 hours
- `json` – for logging raw weather data
- OpenWeatherMap API

---

## 🚀 How to Run

##1 Clone the repo.

```bash
git clone https://github.com/stevenmicevski/Weather-Outfit-Recommender.git
cd Weather-Outfit-Recommender
```

##2 Replace the api_key value in the script with your own OpenWeatherMap API key.

```python
api_key = "YOUR_API_KEY_HERE"
```

##3 Run 

```bash
python weather_outfit.py
```
