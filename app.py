from flask import Flask, jsonify
from app_db import get_mission_data, init_db, get_mission_control_data

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

if __name__ == "__main__":
    app.run(debug=True)

