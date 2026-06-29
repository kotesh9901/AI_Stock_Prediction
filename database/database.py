import sqlite3

connection = sqlite3.connect("database/stock.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    password TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    stock TEXT,

    predicted_price REAL,

    prediction_date TEXT,

    user_email TEXT

)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    stock TEXT
);
""");

connection.commit()

connection.close()

print("Database Created Successfully!")