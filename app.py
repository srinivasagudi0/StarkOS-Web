from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
import requests
from datetime import date, timedelta, datetime
from app_db import get_mission_data, init_db, get_mission_control_data, add_mission_control_data, add_daily_mission, add_weekly_mission, add_long_term_goal, update_mission_status, recover_mission
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key"

IS_PRODUCTION = os.getenv("RENDER") == "true"

if IS_PRODUCTION:
    FRONTEND_URL = "https://stark-os-web-eight.vercel.app"
    BACKEND_URL = FRONTEND_URL
else:
    FRONTEND_URL = "http://localhost:5173"
    BACKEND_URL = "http://localhost:5000"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = IS_PRODUCTION

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "https://stark-os-web-eight.vercel.app",
            ],
        }
    },
    supports_credentials=True,
)

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

@app.route('/api/missions/<int:mission_id>/<action>', methods=['POST'])
def update_mission(mission_id, action):
    if action == 'recover':
        recovered = recover_mission(mission_id)

        if not recovered:
            return jsonify({"message": "Mission not found."}), 404

        return jsonify({"message": "Mission recovered and moved back to active."})

    action_to_status = {
        'complete': 'completed',
        'fail': 'failed',
        'delete': 'deleted',
    }

    status = action_to_status.get(action)

    if not status:
        return jsonify({"message": "Invalid mission action."}), 400

    updated = update_mission_status(mission_id, status)

    if not updated:
        return jsonify({"message": "Mission not found."}), 404

    return jsonify({"message": f"Mission marked as {status}."})

@app.route('/api/hackatime/login')
def hackatime_login():
    client_id = os.getenv("HACKATIME_CLIENT_ID")
    redirect_uri = f"{BACKEND_URL}/api/hackatime/callback"

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
    redirect_uri = f"{BACKEND_URL}/api/hackatime/callback"
    response = requests.post(
        "https://hackatime.hackclub.com/oauth/token",
        data={
            "client_id": os.getenv('HACKATIME_CLIENT_ID'),
            "client_secret": os.getenv('HACKATIME_CLIENT_SECRET'),
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        },
    )
    data = response.json()
    token = data.get("access_token")

    if not token:
        return jsonify({"message": "Hackatime login failed. Check your OAuth app settings."}), 400

    session["hackatime_token"] = token

    return redirect(FRONTEND_URL)

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

@app.route('/api/command-center/energy-score')
def energy():
    hcq = hackatime_streak().get_json()
    st = hackatime_streak().get_json()
    mc = get_mission_control_data()

    hours = float(hcq.get("hours", 0))
    streak = int(st.get("streak", 0))

    daily = len(mc.get("daily_missions", []))  
    weekly = len(mc.get("weekly_missions", []))
    long = len(mc.get("long_term_goals", []))
    failed = len(mc.get("failed_missions", []))

    energy = 100
    if hours == 0:
        energy -= 20
    elif hours < 2:
        energy += 5
    elif hours < 4:
        energy += 2
    elif hours < 6:
        energy -= 8
    else:
        energy -=18
    
    if streak >= 7:
        energy += 10
    elif streak == 0:
        energy -= 5

    if daily and weekly and long:
        energy +=5
    
    energy = max(0, min(100, round(energy)))
    return jsonify({"connected": True, "energy_score": energy})

@app.route('/api/hackatime/goals')
def hackatime_goals():
    oauth_token = session.get("hackatime_token")

    if not oauth_token:
        return jsonify({"connected": False}), 401

    key_response = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/api_keys",
        headers={"Authorization": f"Bearer {oauth_token}"}
    )

    api_key = key_response.json().get("token")

    if not api_key:
        return jsonify({"connected": False}), 401

    response = requests.get(
        "https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"api_key": api_key}
    )

    data = response.json().get("data", {})

    return jsonify({
            "connected": True,
            "goal": data.get("goal", {}),
            "grand_total": data.get("grand_total", {})
        })


@app.route('/api/hackatime/projects')
def hackatime_projects():
    oauth_token = session.get("hackatime_token")

    if not oauth_token:
        return jsonify({"connected": False}), 401
    
    key_response = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/api_keys",
        headers={"Authorization": f"Bearer {oauth_token}"}
    )

    api_key = key_response.json().get("token")

    if not api_key:
        return jsonify({"connected": False}), 401
    
    response = requests.get(
        "https://hackatime.hackclub.com/api/hackatime/v1/users/current/stats/last_7_days",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        params={
            "api_key": f"{api_key}"
        }
    )

    data = response.json().get("data", {})

    return jsonify(
        {
            "connected": True,
            "data": data,
            "editors": data.get("editors", []),
            "languages": data.get("languages", []),
            "machines": data.get("machines", []),
            "projects": data.get("projects", []),
            "operating_systems": data.get("operating_systems", []),
            "categories": data.get("categories", []),
        }
    )

@app.route('/api/hackatime/heatmap')
def hackatime_heatmap():
    oauth_token = session.get("hackatime_token")

    if not oauth_token:
        return jsonify({"connected": False, "message": "No oAuth token", "days": [] }), 401
    
    days = []

    today = date.today()

    try:
        # new thing learnt offset is the distance from the staring point.
        for offset in range(6,-1,-1):
            delta = timedelta(days=offset)
            target_date = today - delta

            response = requests.get(
                "https://hackatime.hackclub.com/api/v1/authenticated/hours",
                headers={
                    "Authorization": f"Bearer {oauth_token}"
                },
                params={
                    "start_date": target_date.isoformat(),
                    "end_date": target_date.isoformat()
                },
                timeout=10
            )

            total_seconds = response.json().get("total_seconds", 0)
            hours = total_seconds / 3600
            hours = round(hours, 2)
            day = target_date

            days.append({
                "date": target_date.isoformat(),
                "day": day.strftime("%a"),
                "total_seconds": total_seconds,
                "hours": hours
            })
    except Exception as e:
        return jsonify({
            "connected": False,
            "message": f"Could not load hackatime heatmao because of {e}",
            "days": []
        })


    return jsonify({"connected": True, "days": days})

@app.route('/api/command-center/greeting')
def greeting():
    current_hour = datetime.now().hour
    text = ""

    if 5 <= current_hour < 12:
        text += "Good morning!"
    elif 12 <= current_hour < 17:
        text += "Good afternoon!"
    elif 17 <= current_hour < 21:
        text += "Good evening!"
    else:
        text += "Good night!"

    text += " sir. I am operating at full capacity and ready to assist you with your missions. Let's make today productive and successful."

    return jsonify({"message": text})

if __name__ == "__main__":
    app.run(debug=True)
