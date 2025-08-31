import sqlite3

# Creating the table
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
        date TEXT,
        time TEXT
    )
    """)
    connection.commit()
    connection.close()

# Delete the table
def delete_table():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS WEATHER")
    connection.commit()
    connection.close()
    print("Table dropped successfully.")

# Delete the data in the table
def delete_weather_data():
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM WEATHER")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='WEATHER'")
    connection.commit()
    connection.close()

# Insert the data into the table
def insert_weather_data(temperature, feelslike, rain, humidity, condition, date, time):
    connection = sqlite3.connect("weather_data.db")
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO WEATHER (temperature, feels, rain, humidity, condition, date, time)
    VALUES (?, ?, ?, ?, ?, ?, ?)""", (temperature, feelslike, rain, humidity, condition, date, time))
    connection.commit()
    connection.close()

# Showing the data from the table
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


