from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

campuses = {"BUS": "busch",
            "CAC": "ca",
            "C/D": "cd",
            "LIV": "livi"}

days = {"Monday": "M",
        "Tuesday": "T",
        "Wednesday": "W",
        "Thursday": "TH",
        "Friday": "F"}

def conv_to_24hour(time, code):
    t = []
    if ':' in time: t = [int(str) for str in time.split(':')]
    else: t = [int(time[:-2]), int(time[-2:])]

    if (code == 'P' or code == 'PM') and t[0] != 12:
        t[0] += 12

    return t

def query_database(campus, building, start_time, M_value, duration, weekday):
    conn = sqlite3.connect('schedule.db')
    cur = conn.cursor()
    print(start_time)
    
    s = conv_to_24hour(start_time, M_value)
    e = [s[0] + ((s[1] + duration) // 60), (s[1] + duration) % 60]

    start = str(s[0]) + '' + ('00' if s[1] == 0 else str(s[1]))
    end = str(e[0]) + '' + ('00' if e[1] == 0 else str(e[1]))

    query = "SELECT abbcampus, abbr, room, building FROM abbrroom WHERE campus like ? AND building like ?"
    rooms = cur.execute(query, (f'{campus}', f'{building}'))
    
    emptyroom = []
    for room in rooms:
        tempconn = sqlite3.connect('schedule.db')
        tempcur = tempconn.cursor()
        
        table_name = campuses[room[0]]
        queryt = f"SELECT start, end, pmCode FROM {table_name} WHERE room = ? AND campus = ? AND day = ? AND building = ?"
        class_time = tempcur.execute(queryt, (f'{room[2]}', f'{room[0]}', f'{days[weekday]}', f'{room[1]}'))
        
        bad = False
        for ctime in class_time:
            class_start, class_end, class_m = ctime
            
            cs = conv_to_24hour(str(class_start), class_m)
            ce = conv_to_24hour(str(class_end), class_m)
            cstart = str(cs[0]) + '' + ('00' if cs[1] == 0 else str(cs[1]))
            cend = str(ce[0]) + '' + ('00' if ce[1] == 0 else str(ce[1]))

            if (int(end) >= int(cstart) and int(start) <= int(cend)):
                bad = True
                break
            
        if (not bad): emptyroom.append(room[3] + " - Room " + str(room[2]))
        tempconn.close()

    conn.close()
    return emptyroom

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    campus = request.form.get('CampusDropdown')
    building = request.form.get('BuildingDropdown')
    start_time = request.form.get('StartTimeDropdown')
    M_value = request.form.get('AMorPMDropdown')
    duration = request.form.get('DurationDropdown')
    weekday = request.form.get('WeekdayDropdown')
    
    query = query_database(campus, '%' if building == 'Any' else building, start_time, M_value, int(duration), weekday)
    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)