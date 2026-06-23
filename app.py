from flask import Flask, jsonify
from app_db import get_mission_data, init_db

app = Flask(__name__)

init_db()

def get_mission_data():
	data = get_mission_data()
    
@app.route('/api/command-center')
def index():
	data = get_mission_data()
	return jsonify(data)    

if __name__ == "__main__":
    app.run(debug=True)