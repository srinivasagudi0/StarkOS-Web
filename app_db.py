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
        "Remember to take breaks and stay hydrated!",
        "Focus on one task at a time to maximize productivity.",
        "Your consistency matters more than perfection.",
        "Small progress is still progress. Keep going!",
        "Take care of your mental health today.",
        "Celebrate your wins, no matter how small.",
        "Break large goals into manageable chunks.",
        "Rest is part of the process, not laziness.",
        "You're capable of more than you think.",
        "Start your day with intention, not just reaction.",
        "Quality over quantity in your work.",
        "Learn something new today, even if it's tiny.",
        "Your future self will thank you for your effort today.",
        "Don't compare your chapter 1 to someone else's chapter 20.",
        "Mistakes are feedback, not failure.",
        "You've overcome challenges before. You'll do it again.",
        "Take time to appreciate how far you've come.",
        "Your effort compounds over time.",
        "Perfectionism is the enemy of progress.",
        "Believe in the process, trust the journey.",
        "Every expert was once a beginner.",
        "Stay hydrated, stay focused, stay moving.",
        "Your limits are mostly mental. Push through.",
        "Done is better than perfect.",
        "Discipline is choosing what you want most over what you want now.",
        "You are stronger than your excuses.",
        "Progress over perfection, always.",
        "Keep your eyes on your own paper.",
        "The best time to start was yesterday. The second best is now.",
        "Your dedication today shapes your tomorrow.",
        "Stay patient with yourself. Growth takes time.",
        "You've got this. One step at a time.",
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
