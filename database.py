import sqlite3


def create_table():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WEATHER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        feels REAL,
        rain INT DEFAULT 0,
        humidity INT,
        condition TEXT,
        date TEXT
    )
    """)
    connection.commit()
    connection.close()

def delete_weather_data():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM WEATHER")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='WEATHER'")
    connection.commit()
    connection.close()

def insert_weather_data(temperature, feelslike, rain, humidity, condition, datetime):
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO WEATHER (temperature, feels, rain, humidity, condition, date)
    VALUES (?, ?, ?, ?, ?, ?)""", (temperature, feelslike, rain, humidity, condition, datetime))
    connection.commit()
    connection.close()

def show_weather_data():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM WEATHER 
        ORDER BY date ASC 
        LIMIT 1""")
    rows = cursor.fetchall()
    connection.close()
    return rows[0]


