import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

rms = requests.get("https://dcs.rutgers.edu/classrooms/find-a-classroom?items_per_page=All")
rms = BeautifulSoup(rms.text, 'html.parser').find_all(class_=["campus-header-text","accordion-row"])

badrooms = []
for element in rms:
    if element.a != element.next_element:
        badrooms.append(element.next_element)
    else:
        badrooms.append(element.next_element.next_element)

rooms = [[0 for x in range(106)] for y in range(4)] 
counter = 0
i = 0
j = -1
for room in badrooms:
    if room == "Busch" or room == "College Avenue" or room == "Cook / Douglass" or room == "Livingston":
        i = 0
        j += 1
        counter += 1
        continue

    ind = badrooms[counter].find(' - ')
    if ind == -1: rooms[j][i] = (badrooms[counter][:25], badrooms[counter][26:])
    else: rooms[j][i] = [badrooms[counter][:ind], badrooms[counter][ind+3:].replace('Room ', '').replace('Auditorium', 'AUD').replace('EDR-204', 'EDR').replace('MPR-205', 'MPR')]

    i += 1
    counter += 1

campus = []
buildings = []
brooms = []
cps = ["Busch", "Colleve Avenue", "Cook / Douglass", "Livingston"]
prev = ""
for i in range(4):
    for room in rooms[i]:
        if room == 0: break
        if room[0] == "Science & Engineering Resource Center": room[0] = "Science & Engineering Resource Center (T. Alexander Pond)"
        if room[0] == "Cook / Douglass Lecture Hall": room[0] = "Cook Douglass Lecture Hall"
        if room[0] == "Food Sciences": room[0] = "Food Science Building"
        if room[0] == "Graduate School Education": room[0] = "Graduate School of Education"
        if room[0] == "Pharmacy": room[0] = "Pharmacy Building (William Levin Hall)"
        if room[0] == "Wright Labs": room[0] = "Wright Rieman Laboratories"

        campus.append(cps[i])
        buildings.append(room[0])
        brooms.append(room[1])


campus.insert(207, "Cook / Douglass")
campus.insert(207, "Cook / Douglass")
campus.insert(207, "Cook / Douglass")
campus.insert(207, "Cook / Douglass")
campus.insert(207, "Cook / Douglass")
campus.insert(207, "Cook / Douglass")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
buildings.insert(207, "Kathleen W Ludwig Global Village Learning Center")
brooms.insert(207, "002")
brooms.insert(208, "008")
brooms.insert(209, "010")
brooms.insert(210, "011")
brooms.insert(211, "013")
brooms.insert(212, "017")

conn = sqlite3.connect("schedule.db")
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS rooms""")
cur.execute("""DROP TABLE IF EXISTS abbrroom""")

cur.execute("""CREATE TABLE rooms  (id INTEGER PRIMARY KEY AUTOINCREMENT, campus TEXT, building TEXT, room TEXT)""")
cur.executemany('INSERT INTO rooms(campus, building, room) VALUES(?, ?, ?)', list(zip(campus, buildings, brooms)))

cur.execute("""CREATE TABLE abbrroom AS \
            SELECT rooms.id, abbrs.abbcampus, rooms.campus, abbrs.abbr, rooms.building, rooms.room \
            FROM rooms \
            INNER JOIN abbrs ON rooms.building=abbrs.buildingname""")

# query = f"SELECT start, end, pmCode FROM cd WHERE room like ? AND campus = ? AND day = ? AND building = ?"
# class_time = cur.execute(query, (f'127', f'C/D', f'M', f'HCK'))

# for row in class_time: print (row)

conn.commit()
conn.close()