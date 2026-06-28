from flask import Flask, jsonify
from app_db import get_mission_data, init_db, get_mission_control_data
from openai import OpenAI
import os

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

def generate_recovery_advice(failed_missions):

    try:
        api = os.getenv("OPENAI_API_KEY")
    except KeyError:
        return jsonify({"message": failed_missions})
    
    prompt = "The user will ask you for an advice on how to recover from his failed missions. Give a detailed yet concise advice and make sure to quote often from the failed missions." 
    "Your expected input will be a list of failed missions. Your output should be a single string with the advice. It will be used in a web applications to help users recover from their failed missions. DONT be too generic, and DONT ask questions. Make sure to give a plan with quotes from the failed missions and NO comments such 'tell me when you are done' or 'Ask me anything you need '."
    client = OpenAI(api_key=api)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Failed missions: {failed_missions}"}
            
        ]
    )
    return response.choices[0].message.content

@app.route('/api/recovery-assistant') #tells how to recover failed tasks
def recovery_assistant():
    data = get_mission_control_data()
    failed_missions = data['failed_missions']
    
    if not failed_missions:
        return jsonify({"message": "Yaey, no failed missions! Keep up the good work!"})

    try:
        advice = generate_recovery_advice(failed_missions)
        return jsonify({"message": advice})
    except Exception as e:
        return jsonify({"messages": failed_missions})

if __name__ == "__main__":
    app.run(debug=True)
