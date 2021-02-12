import sqlite3  
  
con = sqlite3.connect("fitness360.db")  
print("Database opened successfully")  
con.execute("create table calorie_count (id INTEGER PRIMARY KEY AUTOINCREMENT, food TEXT NOT NULL, grams INTEGER NOT NULL, calories INTEGER NOT NULL)")
con.execute("create table exercise_count (id INTEGER PRIMARY KEY AUTOINCREMENT, exercise TEXT NOT NULL, minutes INTEGER NOT NULL, calories INTEGER NOT NULL)")
con.execute("create table health_monitor (id INTEGER PRIMARY KEY AUTOINCREMENT, heartrate INTEGER NOT NULL, sleeptime INTEGER NOT NULL, caloriesate INTEGER NOT NULL, caloriesspent INTEGER)")
print("Tables created successfully") 
con.close()   
