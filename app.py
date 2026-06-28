from flask import Flask, jsonify
from app_db import get_mission_data, init_db, get_mission_control_data
from openai import OpenAI

app = Flask(__name__)

init_db()

@app.route('/api/command-center')
def command_center():
    data = get_mission_data()
    return jsonify(data)

@app.route('/api/mission-control')
def mission_control():
    data = get_mission_control_data()
    return jsonify(data)

@app.route('/api/recovery-assistant') #tells how to recover failed tasks
def recovery_assistant():
    data = get_mission_control_data()
    failed_missions = data['failed_missions']
    
    if not failed_missions:
        return jsonify({"message": "Yaey, no failed missions! Keep up the good work!"})

    return jsonify({"failed_missions": failed_missions})

if __name__ == "__main__":
    app.run(debug=True)

