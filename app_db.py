import sqlite3
from datetime import date, timedelta


def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS command_center (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_hours INTEGER NOT NULL,
            mission TEXT NOT NULL,
            streaks INTEGER DEFAULT 0,
            focus_score INTEGER DEFAULT 0,
            energy_score INTEGER DEFAULT 0,
            warnings TEXT DEFAULT '',
            daily_advice TEXT DEFAULT ''
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS mission_control (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_mission TEXT NOT NULL,
            weekly_missions TEXT NOT NULL,
            long_term_goals TEXT NOT NULL,
            XP_points INTEGER DEFAULT 0,
            streaks INTEGER DEFAULT 0,
            failed_missions TEXT DEFAULT ''
        )
    ''')

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
    cursor.execute('SELECT * FROM mission_control')

    legacy_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM missions WHERE status = 'active'")
    active_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM missions WHERE status = 'failed'")
    failed_rows = cursor.fetchall()

    conn.close()

    daily_missions = []
    weekly_missions = []
    long_term_goals = []
    failed_missions = []
    XP_points = 0
    streaks = 0

    for row in legacy_rows:
        if row['daily_mission']:
            daily_missions.append(row['daily_mission'])
        if row['weekly_missions']:
            weekly_missions.append(row['weekly_missions'])
        if row['long_term_goals']:
            long_term_goals.append(row['long_term_goals'])
        if row['failed_missions']:
            failed_missions.append(row['failed_missions'])
        XP_points += row['XP_points']
        streaks += row['streaks']

    for row in active_rows:
        if row['mission_type'] == 'daily':
            daily_missions.append(row['title'])
        elif row['mission_type'] == 'weekly':
            weekly_missions.append(row['title'])
        elif row['mission_type'] == 'long_term':
            long_term_goals.append(row['title'])

    for row in failed_rows:
        failed_missions.append(row['title'])

    return {
        'daily_missions': daily_missions,
        'weekly_missions': weekly_missions,
        'long_term_goals': long_term_goals,
        'XP_points': XP_points,
        'streaks': streaks,
        'failed_missions': failed_missions,
        'failed_count': len(failed_missions),
    }


def get_mission_data():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM command_center')

    rows = cursor.fetchall()
    conn.close()

    missions = []
    warnings = []
    daily_advice = []
    total_code_hours = 0
    focus_score = 0
    energy_score = 0
    streaks = 0

    

    for row in rows:
        total_code_hours += row['code_hours']
        focus_score += row['focus_score']
        energy_score += row['energy_score']
        streaks += row['streaks']
        missions.append(row['mission'])
        warnings.append(row['warnings'])
        daily_advice.append(row['daily_advice'])
        
    
    if len(rows) > 0:
        focus_score = focus_score // len(rows)
        energy_score = energy_score // len(rows)

    return {
        'code_hours': total_code_hours,
        'missions': missions,
        'streaks': streaks,
        'focus_score': focus_score,
        'energy_score': energy_score,
        'warnings': warnings,
        'daily_advice': daily_advice,
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
