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

#cursor.execute("""CREATE TABLE IF NOT EXISTS busch  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS livi  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS ca  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

#cursor.execute("""CREATE TABLE IF NOT EXISTS cd  (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, pmCode TEXT, campus TEXT, day TEXT, building TEXT, start INTEGER, end INTEGER)""")
#conn.commit()

for cc in coursecodes:
    url1 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=UG"
    url2 = "https://sis.rutgers.edu/oldsoc/courses.json?subject="+cc+"&semester=12025&campus=NB&level=G"

    requestug = requests.get(url1)
    requestg = requests.get(url2)

    ugsched = requestug.json()
    gsched = requestg.json()



course1 = ugsched[3]
if course1["campusCode"] == "NB":
    for section in course1["sections"]:
        if section["printed"] == "Y":
            classblocks = section["meetingTimes"]
            
            for block in classblocks:
                if(block["campusLocation"]== "O"):
                    next
                campus = block["campusAbbrev"]
                room = block["roomNumber"]
                pmCode = block["pmCode"]
                day = block["meetingDay"]
                building = block["buildingCode"]
                start = block["startTime"]
                end = block["endTime"]
                
                if(campus == "BUS"):
                    conn.execute("""INSERT INTO busch (room, pmCode, campus, day, building, start, end)""",(room,pmCode,campus,day,building,start,end))
                    conn.commit()
                if(campus == "LIV"):
                    conn.execute("""INSERT INTO livi (room, pmCode, campus, day, building, start, end)""",(room,pmCode,campus,day,building,start,end))
                    conn.commit()
                if(campus == "CAC"):
                    conn.execute("""INSERT INTO ca (room, pmCode, campus, day, building, start, end)""",(room,pmCode,campus,day,building,start,end))
                    conn.commit()
                if(campus == "D/C"):
                    conn.execute("""INSERT INTO cd (room, pmCode, campus, day, building, start, end)""",(room,pmCode,campus,day,building,start,end))
                    conn.commit()


                
    
    

    #for course in ugsched:
    #    if 

conn.close()    


