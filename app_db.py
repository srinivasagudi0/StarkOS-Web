import sqlite3


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

    conn.commit()
    conn.close()


def get_mission_control_data():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mission_control')

    rows = cursor.fetchall()
    conn.close()

    daily_missions = []
    weekly_missions = []
    long_term_goals = []
    failed_missions = []
    XP_points = 0
    streaks = 0

    for row in rows:
        daily_missions.append(row['daily_mission'])
        weekly_missions.append(row['weekly_missions'])
        long_term_goals.append(row['long_term_goals'])
        if row['failed_missions']:
            failed_missions.append(row['failed_missions'])
        XP_points += row['XP_points']
        streaks += row['streaks']

    return {
        'daily_missions': daily_missions,
        'weekly_missions': weekly_missions,
        'long_term_goals': long_term_goals,
        'XP_points': XP_points,
        'streaks': streaks,
        'failed_missions': failed_missions,
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
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO mission_control (daily_mission, weekly_missions, long_term_goals)
            VALUES (?, ?, ?)
        """, (daily, weekly, long_term))

    conn.commit()
    conn.close()

def add_daily_mission(mission):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mission_control (daily_mission, weekly_missions, long_term_goals)
        VALUES (?, '', '')
    """, (mission,))

    conn.commit()
    conn.close()

def add_weekly_mission(mission):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mission_control (daily_mission, weekly_missions, long_term_goals)
                   VALUES ('', ?, '')
    """, (mission,))

    conn.commit()
    conn.close()

def add_long_term_goal(goal):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mission_control (daily_mission, weekly_missions, long_term_goals)
        VALUES ('', '', ?)
    """, (goal,))

    conn.commit()
    conn.close()