from flask import Flask, jsonify, request, redirect, session
import requests
from datetime import date
from app_db import get_mission_data, init_db, get_mission_control_data, add_mission_control_data, add_daily_mission, add_weekly_mission, add_long_term_goal
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"

init_db()

@app.route('/api/command-center')
def command_center():
    data = get_mission_data()
    return jsonify(data)

@app.route('/api/mission-control')
def mission_control():
    data = get_mission_control_data()
    
    daily_missions = data['daily_missions']
    if not daily_missions:
        data['daily_missions'] = ["No daily missions at the moment. Enjoy or set new missions!"]

    weekly_missions = data['weekly_missions']
    if not weekly_missions:
        data['weekly_missions'] = ["No weekly missions at the moment. Enjoy or set new missions!"]

    ltg = data['long_term_goals']

    if not ltg:
        data['long_term_goals'] = ["No long term goals. Set a new long term goal, please."]

    failed_missions = data["failed_missions"]
    if not failed_missions:
        data["failed_missions"] = ["No failed missions. Keep up the good work!"] 
    
    return jsonify(data)

def generate_recovery_advice(failed_missions, daily_tasks, weekly_tasks):

    try:
        api = os.getenv("OPENAI_API_KEY")
    except KeyError:
        return jsonify({"message": failed_missions})
    
    prompt = """
    You help users recover from failed missions.
    Write a single short, actionable advice string.
    Use the failed missions as context and quote exact phrashes from them when useful.
    Be specific, concise, and practical.
    Do not be generic. Do not ask questions.
    Do not include filler like 'tell me when you are done' or 'let me know' or 'ask me anyhting'.
    Return only the advice text.
    Actually plan, dont just say 'If you missed your daily tasks, aim to catch up on them during the weekend to stay on track.'
    """
    client = OpenAI(api_key=api)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Failed missions: {failed_missions}\n\nDaily tasks: {daily_tasks}\n\nWeekly tasks: {weekly_tasks}\n\nIf a task cannot be completed during the day, suggest completing it on the weekend."}
            
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
        advice = generate_recovery_advice(failed_missions, data['daily_missions'], data['weekly_missions'])
        return jsonify({"message": advice})
    except Exception as e:
        return jsonify({"messages": failed_missions})
    
def generate_warnings(active_missions):
    try:
        api = os.getenv('OPENAI_API_KEY')
    except KeyError:
        return jsonify({"message": "Warnings cannot be generated at the moment. Please check your API key."})
    
    prompt = """
    You generate cocise warnings for a user's active missions.
    Return only json like list of short warnings strings, for example: ["warning 1", "warning 2", "warning 3"].

    Each watning must be:
    - specific to the mission provided
    - actionable
    - breif
    - not generic

    WARNINGS SHOULD NOT MORE NUMBER THAN THE NUMBER OF ACTIVE MISSIONS.

    Do not ask questions, numbering, or extra text. Do not include filler like 'tell me when you are done' or 'let me know' or 'ask me anyhting'.

    """

    client = OpenAI(api_key=api)
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Here are all the active missions: {active_missions}."}
        ]
    )
    return response.choices[0].message.content

@app.route('/api/warnings')
def warnings():

    data = get_mission_control_data()
    active_missions = data['daily_missions'] + data['weekly_missions'] + data['long_term_goals']

    if not active_missions:
        return jsonify({"message": "No active missions at the moment. Enjoy or set new missions!"}) # thss does the job of telling empty message

    try:
        warnings = generate_warnings(active_missions)
        return jsonify({"message": warnings})
    except Exception as e:
        return jsonify({"message": "Warnings are currently unavailable. Please try again later."})
    

@app.route('/api/advice')
def advice():
    data=get_mission_data()

    advice = data['daily_advice']

    if not advice:
        return jsonify({"message": "No advice available at the moment. Please check back later."})
    
    num = len(advice)

    if num == 1:
        return jsonify({"message": advice[0]})
    else:
        import random
        random_advice = random.choice(advice)
        return jsonify({"message": random_advice})
    

def plan_with_ai(input_text):
    api = os.getenv('OPENAI_API_KEY')
    if not api:
        return "AI planning is currently unavailable. Please add your OpenAI key to the environment variables."
    
    client = OpenAI(api_key=api)

    prompt = '''
    You help users plan out their mission(s)/task(s). Divide the plan into daily, weekly, and long-term goals and ONLY RETURN a valid JSON object with this shape:
    {
        "daily": ["task 1", "task 2", ...],
        "weekly": ["task 1", "task 2", ...],
        "long_term": ["goal 1", "goal 2", ...]
    }
    DO NOT ASSUME ANYTHING ABOUT THE USER OR TASKS. DO NOT INCLUDE ANY EXPLANATIONS OR FILLER. FOR EXAMPLE, if it says something like "finish homework", you say daily misssion to be finihsh homework
    Use arrays for every key. Do not ask questions, add explanations, markdown, or filler. Return only the JSON object.
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"User input: {input_text}"}
        ]
    )

    return response.choices[0].message.content

@app.route('/api/ai-forge', methods=['POST'])
def ai_forge():
    data = request.get_json() or {}
    input_text = data.get('input', '')

    if not input_text:
        return jsonify({"message": "Please enter a mission first."})

    try:
        plan = plan_with_ai(input_text)
        return jsonify({"message": plan})
    except Exception:
        return jsonify({"message": "AI planning is currently unavailable. Please try again later."})
    
@app.route('/api/apply_plan', methods=['POST'])
def apply_plan():
    data = request.get_json () or {}
    daily = data.get("daily", "")
    weekly = data.get("weekly", "")
    long_term = data.get("long_term", "")

    if long_term and daily and weekly:
        add_mission_control_data(daily, weekly, long_term)
    else:
        if daily:

            add_daily_mission(daily)
        if weekly:
            add_weekly_mission(weekly)
        if long_term:
            add_long_term_goal(long_term)
    return jsonify({"message": "Plan applied successfully."})

@app.route('/api/add_daily', methods=['POST'])
def add_daily():
    data = request.get_json() or {}
    daily = data.get("daily", "")
    if daily:
        add_daily_mission(daily)
        return jsonify({"message": "Daily mission added successfully."})
    else:
        return jsonify({"message": "Please provide a daily mission."}), 400

@app.route('/api/add_weekly', methods=['POST'])
def add_weekly():
    data = request.get_json() or {}
    weekly = data.get("weekly", "")
    if weekly:
        add_weekly_mission(weekly)
        return jsonify({"message": "Weekly mission added successfully."})
    else:
        return jsonify({"message": "Please provide a weekly mission."}), 400

@app.route('/api/add_long_term', methods=['POST'])
def add_long_term():
    data = request.get_json() or {}
    long_term = data.get("long_term", "")
    if long_term:
        add_long_term_goal(long_term)
        return jsonify({"message": "Long-term goal added successfully."})
    else:
        return jsonify({"message": "Please provide a long-term goal."}), 400

@app.route('/api/hackatime/login')
def hackatime_login():
    client_id = os.getenv("HACKATIME_CLIENT_ID")
    redirect_uri = "http://localhost:5000/api/hackatime/callback"

    return redirect(
        "https://hackatime.hackclub.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
        "&scope=profile+read"
    )

@app.route('/api/hackatime/callback')
def hackatime_callback():
    code = request.args.get("code")
    response = requests.post(
        "https://hackatime.hackclub.com/oauth/token",
        data={
            "client_id": os.getenv('HACKATIME_CLIENT_ID'),
            "client_secret": os.getenv('HACKATIME_CLIENT_SECRET'),
            "code": code,
            "redirect_uri": "http://localhost:5000/api/hackatime/callback",
            "grant_type": "authorization_code"
        },
    )
    data = response.json()
    session["hackatime_token"] = data.get("access_token")

    return redirect("http://localhost:5173/")

@app.route('/api/hackatime/hours')
def hackatime_hours():
    token = session.get("hackatime_token")

    if not token:
        return jsonify({"connected": False, "hours": 0})

    today = date.today().isoformat()

    response = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/hours",
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "start_date": today,
            "end_date": today
        }
    )

    data = response.json()
    seconds = data.get("total_seconds", 0)

    return jsonify({"connected": True, "hours": round(seconds / 3600, 2)})

@app.route('/api/hackatime/streak')
def hackatime_streak():
    token = session.get("hackatime_token")

    if not token:
        return jsonify({"connected": False, "streak": 0})
    
    response = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/streak",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    data = response.json()
    streak = data.get("streak_days", 0)

    return jsonify({"connected": True, "streak": streak})

@app.route('/api/command-center/focus-score')
def focus():
    hours = hackatime_hours().get_json().get("hours", 0)
    focus_score = min(hours * 20, 100)
    focus_score = round(focus_score)

    return jsonify({"connected": True, "focus_score": focus_score})


if __name__ == "__main__":
    app.run(debug=True)