import json
import requests
import sqlite3

request = requests.get("https://sis.rutgers.edu/oldsoc/init.json")

info = request.json()


coursecodes = []

for subject in info["subjects"]:
    coursecodes.append(subject["code"])

with open('courselist.txt','w') as file:
    file.write(str(coursecodes))



conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

#cursor.execute("""CREATE TABLE IF NOT EXISTS busch  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS livi  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS ca  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS cd  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

with open('courselist.txt','r') as file:
    data = file.read()
    data = data.replace("'", '"')
    coursecodes = json.loads(data)
    print(coursecodes)

conn.execute("""DELETE FROM livi""")
conn.execute("""DELETE FROM sqlite_sequence WHERE name='livi'""")
conn.execute("""DELETE FROM busch""")
conn.execute("""DELETE FROM sqlite_sequence WHERE name='busch'""")
conn.execute("""DELETE FROM cd""")
conn.execute("""DELETE FROM sqlite_sequence WHERE name='cd'""")
conn.execute("""DELETE FROM ca""")
conn.execute("""DELETE FROM sqlite_sequence WHERE name='ca'""")
conn.commit()

for cc in coursecodes:
    url1 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=UG"
    url2 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=G"

    requestug = requests.get(url1)
    requestg = requests.get(url2)

    ugsched = requestug.json()
    gsched = requestg.json()
    print("Looking at course code " + cc)

    for course in ugsched:
        if course["campusCode"] == "NB":
            for section in course["sections"]:
                if section["printed"] == "Y":
                    classblocks = section["meetingTimes"]
                    
                    for block in classblocks:
                        if(block["campusLocation"]== "O"):
                            continue
                        campus = block["campusAbbrev"]
                        if(campus == "D/C"):
                            campus = "C/D"
                        room = block["roomNumber"]
                        if(room is None):
                            continue
                        pmCode = block["pmCode"]
                        day = block["meetingDay"]
                        building = block["buildingCode"]
                        start = block["startTime"]
                        end = block["endTime"]
                        
                        if(campus == "BUS"):
                            conn.execute("""INSERT INTO busch (room, pmCode, campus, day, building, start, end)
                                        VALUES (?,?,?,?,?,?,?)""",(room,pmCode,campus,day,building,start,end))
                            conn.commit()
                        if(campus == "LIV"):
                            conn.execute("""INSERT INTO livi (room, pmCode, campus, day, building, start, end)
                                        VALUES (?,?,?,?,?,?,?)""",(room,pmCode,campus,day,building,start,end))
                            conn.commit()
                        if(campus == "CAC"):
                            conn.execute("""INSERT INTO ca (room, pmCode, campus, day, building, start, end)
                                        VALUES (?,?,?,?,?,?,?)""",(room,pmCode,campus,day,building,start,end))
                            conn.commit()
                        if(campus == "C/D"):
                            conn.execute("""INSERT INTO cd (room, pmCode, campus, day, building, start, end)
                                        VALUES (?,?,?,?,?,?,?)""",(room,pmCode,campus,day,building,start,end))
                            conn.commit()

conn.close()    


