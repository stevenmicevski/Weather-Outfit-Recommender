import sqlite3

#DATABSE

#creating the table with the needed values
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
        LIMIT 4
    )
    """)
    connection.commit()
    connection.close()

#deleting the data in the table before every new fetch/insertion
def delete_weather_data():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM WEATHER")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='WEATHER'")
    connection.commit()
    connection.close()

#inserting the fetched data into the table
def insert_weather_data(temperature, feelslike, rain, humidity, condition, datetime):
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO WEATHER (temperature, feels, rain, humidity, condition, date)
    VALUES (?, ?, ?, ?, ?, ?)""", (temperature, feelslike, rain, humidity, condition, datetime))
    connection.commit()
    connection.close()

#showing the data from the first 5 rows in the table
def show_weather_data():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM WEATHER 
        ORDER BY date ASC 
        LIMIT 5""")
    rows = cursor.fetchall()
    connection.close()
    return rows


