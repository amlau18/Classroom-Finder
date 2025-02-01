import json
import requests
import sqlite3

request = requests.get("https://sis.rutgers.edu/oldsoc/init.json")

info = request.json()

coursecodes = []

for subject in info["subjects"]:
    coursecodes.append(subject["code"])

conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS busch  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS livi  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS ca  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS cd  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
conn.commit()

for cc in coursecodes:
    url1 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=UG"
    url2 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=G"

conn.close()

