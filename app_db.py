import sqlite3
from datetime import date, timedelta


def init_db():

    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            mission_type TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            due_date TEXT,
            created_at TEXT DEFAULT CURRENT_DATE
        )
    ''')

    conn.commit()
    conn.close()


def fail_overdue_missions():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    today = date.today().isoformat()

    cursor.execute("""
        UPDATE missions
        SET status = 'failed'
        WHERE status = 'active'
        AND due_date IS NOT NULL
        AND due_date < ?
    """, (today,))

    conn.commit()
    conn.close()


def get_mission_control_data():
    fail_overdue_missions()

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    legacy_rows = []

    cursor.execute("SELECT * FROM missions WHERE status = 'active' ORDER BY due_date, id")
    active_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM missions WHERE status = 'failed' ORDER BY id DESC")
    failed_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM missions WHERE status = 'completed'")
    completed_rows = cursor.fetchall()

    conn.close()

    daily_missions = []
    weekly_missions = []
    long_term_goals = []
    failed_missions = []
    legacy_daily_missions = []
    legacy_weekly_missions = []
    legacy_long_term_goals = []
    daily_mission_items = []
    weekly_mission_items = []
    long_term_goal_items = []
    failed_mission_items = []
    XP_points = 0
    streaks = 0

    for row in legacy_rows:
        if row['daily_mission']:
            daily_missions.append(row['daily_mission'])
            legacy_daily_missions.append(row['daily_mission'])
        if row['weekly_missions']:
            weekly_missions.append(row['weekly_missions'])
            legacy_weekly_missions.append(row['weekly_missions'])
        if row['long_term_goals']:
            long_term_goals.append(row['long_term_goals'])
            legacy_long_term_goals.append(row['long_term_goals'])
        if row['failed_missions']:
            failed_missions.append(row['failed_missions'])
        XP_points += row['XP_points']
        streaks += row['streaks']

    for row in active_rows:
        mission_item = {
            'id': row['id'],
            'title': row['title'],
            'mission_type': row['mission_type'],
            'status': row['status'],
            'due_date': row['due_date'],
        }

        if row['mission_type'] == 'daily':
            daily_missions.append(row['title'])
            daily_mission_items.append(mission_item)
        elif row['mission_type'] == 'weekly':
            weekly_missions.append(row['title'])
            weekly_mission_items.append(mission_item)
        elif row['mission_type'] == 'long_term':
            long_term_goals.append(row['title'])
            long_term_goal_items.append(mission_item)

    for row in failed_rows:
        failed_missions.append(row['title'])
        failed_mission_items.append({
            'id': row['id'],
            'title': row['title'],
            'mission_type': row['mission_type'],
            'status': row['status'],
            'due_date': row['due_date'],
        })

    for row in completed_rows:
        if row['mission_type'] == 'daily':
            XP_points += 20
        elif row['mission_type'] == 'weekly':
            XP_points += 50
        elif row['mission_type'] == 'long_term':
            XP_points += 120

    XP_points = max(XP_points - (len(failed_rows) * 25), 0)

    return {
        'daily_missions': daily_missions,
        'weekly_missions': weekly_missions,
        'long_term_goals': long_term_goals,
        'legacy_daily_missions': legacy_daily_missions,
        'legacy_weekly_missions': legacy_weekly_missions,
        'legacy_long_term_goals': legacy_long_term_goals,
        'daily_mission_items': daily_mission_items,
        'weekly_mission_items': weekly_mission_items,
        'long_term_goal_items': long_term_goal_items,
        'XP_points': XP_points,
        'streaks': streaks,
        'failed_missions': failed_missions,
        'failed_mission_items': failed_mission_items,
        'failed_count': len(failed_missions),
        'completed_count': len(completed_rows),
    }


def get_mission_data():
    return {
        'code_hours': 0,
        'missions': [],
        'streaks': 0,
        'focus_score': 0,
        'energy_score': 0,
        'warnings': [],
        'daily_advice': [
        "Take a real break and drink some water. Your brain will thank you.",
        "Pick one task and give it your full attention for a little while.",
        "You don't need a perfect day. Showing up consistently is enough.",
        "Even a small step moves you forward. Keep it going.",
        "Check in with yourself today. Rest is part of doing good work.",
        "You did something hard? Count it. Small wins still count.",
        "Make the big thing smaller: choose the next step, not the whole mountain.",
        "Rest isn't falling behind. It's how you come back with energy.",
        "You can handle more than this moment makes it feel like.",
        "Choose what matters before the day chooses for you.",
        "A focused hour beats a busy day full of half-finished tasks.",
        "Learn one small thing today. That still adds up.",
        "The work you do today makes tomorrow a little easier.",
        "You're on your own timeline. Compare less, build more.",
        "A mistake is useful information. Use it and keep moving.",
        "You've handled hard days before. This one won't last forever.",
        "Pause for a second and notice how far you've already come.",
        "Small efforts stack up faster than you think.",
        "Don't let perfect stop you from making progress.",
        "Trust the routine, even on the days it feels slow.",
        "Everyone starts somewhere. Your first version is allowed to be rough.",
        "Drink some water, move around, then come back to the next step.",
        "The limit today might be your energy, not your ability. Work with it.",
        "Finished is valuable. You can polish it later.",
        "Choose the work that matters most, even when the easy thing is tempting.",
        "Your excuses are loud, but they don't get to make the decision.",
        "Keep choosing progress over perfection.",
        "Stay focused on your path. You don't need to copy anyone else's.",
        "You can start now. That's better than waiting for the perfect time.",
        "What you do today is building the person you'll be later.",
        "Be patient with yourself. Growth takes more than one good day.",
        "You don't have to do everything today. Just take the next step.",
    ]
    
    }

def add_mission_control_data(daily, weekly, long_term):
    if daily:
        add_daily_mission(daily)
    if weekly:
        add_weekly_mission(weekly)
    if long_term:
        add_long_term_goal(long_term)


def add_mission(title, mission_type, days_until_due):
    if not title:
        return

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    due_date = (date.today() + timedelta(days=days_until_due)).isoformat()

    cursor.execute("""
        INSERT INTO missions (title, mission_type, status, due_date)
        VALUES (?, ?, 'active', ?)
    """, (title, mission_type, due_date))

    conn.commit()
    conn.close()


def add_daily_mission(mission):
    add_mission(mission, 'daily', 0)

def add_weekly_mission(mission):
    add_mission(mission, 'weekly', 7)

def add_long_term_goal(goal):
    add_mission(goal, 'long_term', 90)


def update_mission_status(mission_id, status):
    allowed_statuses = {'active', 'completed', 'failed', 'deleted'}

    if status not in allowed_statuses:
        return False

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE missions
        SET status = ?
        WHERE id = ?
    """, (status, mission_id))

    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return changed


def recover_mission(mission_id):
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT mission_type FROM missions WHERE id = ?", (mission_id,))
    mission = cursor.fetchone()

    if not mission:
        conn.close()
        return False

    days_by_type = {
        'daily': 1,
        'weekly': 7,
        'long_term': 90,
    }

    due_date = (date.today() + timedelta(days=days_by_type.get(mission['mission_type'], 1))).isoformat()

    cursor.execute("""
        UPDATE missions
        SET status = 'active',
            due_date = ?
        WHERE id = ?
    """, (due_date, mission_id))

    conn.commit()
    conn.close()

    return True
