from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

campuses = {"BUS": "busch",
            "CAC": "ca",
            "C/D": "cd",
            "LIV": "livi"}

def conv_to_24hour(time, code):
    t = []
    if ':' in time: t = [int(str) for str in time.split(':')]
    else: t = [time[:2], time[2:]]

    if code == 'PM':
        t[0] += 12

    return time

def query_database(campus, building, start_time, M_value, duration, weekday):
    conn = sqlite3.connect('schedule.db')
    cur = conn.cursor()

    s = conv_to_24hour(start_time, M_value)
    e = [s[0] + ((s[1] + duration) / 60), (s[1] + duration) % 60]

    start = str(s[0]) + '' + str(s[1])
    end = str(e[0]) + '' + str(e[1])

    query = "SELECT abbcampus, abbr, room, building FROM abbrroom WHERE campus like '?' AND building like '?'"
    rooms = cur.execute(query, (campus, building))

    emptyroom = []
    for room in rooms:
        roomIsEmpty = True
        query = "SELECT start, end, pmCode FROM '?' WHERE room = '?' AND \
            campus = '?' AND day = '?' AND building = '?'"
        class_time = cur.execute(query, (campuses[room[0]], room[2], room[0], weekday, room[1]))

        for class_start, class_end, class_m in class_time:
            cs = conv_to_24hour(class_start, class_m)
            ce = conv_to_24hour(class_end, class_m)
            cstart = str(cs[0]) + '' + str(cs[1])
            cend = str(ce[0]) + '' + str(ce[1])

            if int(end) >= int(cstart) and int(start) <= int(cend):
                roomIsEmpty = False
                break
            else:
                emptyroom.append(room[3] + " - Room " + str(room[2]))

    conn.close()
    return emptyroom

@app.route('/submit', methods=['POST'])
def submit():
    campus = request.form.get('CampusDropdown')
    building = request.form.get('BuildingDropdown')
    start_time = request.form.get('StartTimeDropdown')
    M_value = request.form.get('AMorPMDropdown')
    duration = request.form.get('DurationDropdown')
    weekday = request.form.get('WeekdayDropdown')

    query = query_database(campus, '%' if building == 'Any' else building, start_time, M_value, duration, weekday)
    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)