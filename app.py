from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
import requests
from datetime import date, timedelta, datetime
from app_db import get_mission_data, init_db, get_mission_control_data, add_mission_control_data, add_daily_mission, add_weekly_mission, add_long_term_goal, update_mission_status, recover_mission
from openai import OpenAI
import os
import json

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
        data['daily_missions'] = ["Your day is clear - add a mission when you're ready."]

    weekly_missions = data['weekly_missions']
    if not weekly_missions:
        data['weekly_missions'] = ["Nothing planned this week yet - add something when you're ready."]

    ltg = data['long_term_goals']

    if not ltg:
        data['long_term_goals'] = ["No big goals yet - add one when you know what you're aiming for."]

    failed_missions = data["failed_missions"]
    if not failed_missions:
        data["failed_missions"] = ["Nothing missed. Nice work!"]
    
    return jsonify(data)

def generate_recovery_advice(failed_missions, daily_tasks, weekly_tasks):

    try:
        api = os.getenv("OPENAI_API_KEY")
    except KeyError:
        return jsonify({"message": failed_missions})
    
    prompt = """
    You are a calm, helpful teammate in a personal mission app.
    Write one short recovery message using the user's actual missed missions.
    Give one specific, realistic next step instead of generic motivation.
    Sound warm and human, not like a system notification or a life coach.
    Do not ask questions or add filler. Return only the message.
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
        return jsonify({"message": "Nothing missed. Nice work! You're all clear."})

    try: 
        advice = generate_recovery_advice(failed_missions, data['daily_missions'], data['weekly_missions'])
        return jsonify({"message": advice})
    except Exception as e:
        return jsonify({"messages": failed_missions})
    
def generate_warnings(active_missions):
    try:
        api = os.getenv('OPENAI_API_KEY')
    except KeyError:
        return jsonify({"message": "I can't create warnings right now. Check that your OpenAI key is connected."})
    
    prompt = """
    You are a helpful teammate in a personal productivity app.
    Write one short warning for each active mission, using the actual mission as context.
    Keep each warning specific, practical, and easy to act on.
    Sound human and calm, not corporate or dramatic.
    Return only a JSON list of warning strings.
    Do not ask questions, add numbering, or include filler.
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
        return jsonify({"message": "No warnings today - you're clear to focus."})

    try:
        warnings = generate_warnings(active_missions)
        return jsonify({"message": warnings})
    except Exception as e:
        return jsonify({"message": "I couldn't load your warnings this time. Try again in a moment."})
    

@app.route('/api/advice')
def advice():
    data=get_mission_data()

    advice = data['daily_advice']

    if not advice:
        return jsonify({"message": "No advice is ready right now. Check back in a little while."})
    
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
        return "AI planning isn't connected yet. Add your OpenAI key to turn ideas into missions."
    
    client = OpenAI(api_key=api)

    prompt = '''
    You help a person turn an idea into a realistic mission plan.
    Divide the plan into daily, weekly, and long-term goals and ONLY RETURN a valid JSON object with this shape:
    {
        "daily": ["task 1", "task 2", ...],
        "weekly": ["task 1", "task 2", ...],
        "long_term": ["goal 1", "goal 2", ...]
    }
    Keep the user's wording where possible. Make each mission clear and realistic.
    Do not assume personal details, ask questions, add explanations, markdown, or filler.
    Return only the JSON object.
    '''

    response = client.chat.completions.create(
        model="gpt-4o",
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
        return jsonify({"message": "Tell me what you want to accomplish first."})

    try:
        plan = plan_with_ai(input_text)
        if isinstance(plan, str):
            plan = json.loads(plan)
        ufm = "Here's a mission plan built around your idea:\n"

        daily = plan.get("daily", [])
        if daily:
            ufm += "Today's missions:\n"
            for i, task in enumerate(daily, start=1):
                ufm += f"{i}. {task}\n"
            ufm += "\n"

        weekly = plan.get("weekly", [])
        if weekly:
            ufm += "This week's missions:\n"
            for i, task in enumerate(weekly, start=1):
                ufm += f"{i}. {task}\n"
            ufm += "\n"

        long_term = plan.get("long_term", [])
        if long_term:
            ufm += "Long-term goals:\n"
            for i, goal in enumerate(long_term, start=1):
                ufm += f"{i}. {goal}\n"

        return jsonify({"plan": plan, "message": ufm})
    except Exception as e:
        return jsonify({"message": "I couldn't build that plan this time. Check your connection and try again."})
    
@app.route('/api/apply_plan', methods=['POST'])
def apply_plan():
    data = request.get_json() or {}

    daily = data.get("daily", [])
    weekly = data.get("weekly", [])
    long_term = data.get("long_term", [])

    if isinstance(daily, str):
        daily = [daily]
    if isinstance(weekly, str):
        weekly = [weekly]
    if isinstance(long_term, str):
        long_term = [long_term]

    for mission in daily:
        if mission:
            add_daily_mission(mission)
    for mission in weekly:
        if mission:
            add_weekly_mission(mission)
    for goal in long_term:
        if goal:
            add_long_term_goal(goal)
        
    return jsonify({"message": "Your missions are ready 🚀"})

@app.route('/api/add_daily', methods=['POST'])
def add_daily():
    data = request.get_json() or {}
    daily = data.get("daily", "")
    if daily:
        add_daily_mission(daily)
        return jsonify({"message": "Your daily mission is on the board."})
    else:
        return jsonify({"message": "Tell me what you want to finish today."}), 400

@app.route('/api/add_weekly', methods=['POST'])
def add_weekly():
    data = request.get_json() or {}
    weekly = data.get("weekly", "")
    if weekly:
        add_weekly_mission(weekly)
        return jsonify({"message": "Your weekly mission is on the board."})
    else:
        return jsonify({"message": "Tell me what you want to work on this week."}), 400

@app.route('/api/add_long_term', methods=['POST'])
def add_long_term():
    data = request.get_json() or {}
    long_term = data.get("long_term", "")
    if long_term:
        add_long_term_goal(long_term)
        return jsonify({"message": "Your long-term goal is on the board."})
    else:
        return jsonify({"message": "Tell me what you're working toward."}), 400

@app.route('/api/missions/<int:mission_id>/<action>', methods=['POST'])
def update_mission(mission_id, action):
    if action == 'recover':
        recovered = recover_mission(mission_id)

        if not recovered:
            return jsonify({"message": "I couldn't find that mission anymore."}), 404

        return jsonify({"message": "Back on track. That mission is active again."})

    action_to_status = {
        'complete': 'completed',
        'fail': 'failed',
        'delete': 'deleted',
    }

    status = action_to_status.get(action)

    if not status:
        return jsonify({"message": "I couldn't do that with this mission."}), 400

    updated = update_mission_status(mission_id, status)

    if not updated:
        return jsonify({"message": "I couldn't find that mission anymore."}), 404

    messages = {
        'completed': "Mission complete. Nice work!",
        'failed': "That mission is marked as missed. You can recover it later.",
        'deleted': "That mission has been removed.",
    }
    return jsonify({"message": messages[status]})

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
        return jsonify({"message": "Hackatime couldn't connect. Check the connection settings and try again."}), 400

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
        return jsonify({"connected": False, "message": "Connect Hackatime to see your coding activity here.", "days": [] }), 401
    
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
            "message": "I couldn't load your coding heatmap. Try reconnecting Hackatime.",
            "days": []
        })

    return jsonify({"connected": True, "days": days})


@app.route('/api/pages/personalize')
def personalize():
    messages = [
        "Built by Srinivasa to make coding feel like a mission 🚀",
        "Keep building - you're closer than yesterday 💪",
        "Code with heart of an artist, for elegance lies in simplicity. 🎨",
        "Your code is a story waiting to unfold in the digital realm. 📖",
        "Programming is not about what you know, it's about what you can figure out. 🧠",
        "Code is like humor. When you have to explain it, it's bad. 😄",
        "Debugging is like being a detective in a crime movie where you are also the murderer. 🔍",
        "The best way to predict the future is to create it. ✨",
        "Simplicity is the soul of efficiency. ⚡",
        "Beauty is the ultimate goal of design. 🌟",
        "Good luck on the project you are working! 🍀",
        "Nothing here 🤷",
        "Be willing to be a beginner every single morning to keep learning! 📚",
        "Start anything with emotion! ❤️",
        "Momentum grows when the first step feels manageable.",
        "Focus isn't intensity. It's loyalty to one task.",
    ]
    import random
    message = random.choice(messages)
    return jsonify({"message": message})

@app.route('/api/mission-control/count')
def count():
    data = get_mission_control_data()
    daily_count = len(data["daily_missions"])

    if daily_count == 0:
        message = "Your daily missions are clear."
    else:
        mission_word = "mission" if daily_count == 1 else "missions"
        message = f"{daily_count} daily {mission_word} left to go."

    return jsonify({"count": daily_count, "message": message})


if __name__ == "__main__":
    app.run(debug=True)
