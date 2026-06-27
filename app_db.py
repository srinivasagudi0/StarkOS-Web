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

    c.execute('PRAGMA table_info(mission_control)')
    mission_columns = [column[1] for column in c.fetchall()]

    if 'failed_misions' in mission_columns and 'failed_missions' not in mission_columns:
        c.execute('ALTER TABLE mission_control RENAME COLUMN failed_misions TO failed_missions')

    if 'streaks' not in mission_columns:
        c.execute('ALTER TABLE mission_control ADD COLUMN streaks INTEGER DEFAULT 0')

    c.execute('SELECT COUNT(*) FROM command_center')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO command_center
            (code_hours, mission, streaks, focus_score, energy_score, warnings, daily_advice)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            4,
            'Build Command Center page',
            3,
            80,
            70,
            'Do not code too late. Take breaks.',
            'Finish one small feature today.'
        ))

        c.execute('''
            INSERT INTO command_center
            (code_hours, mission, streaks, focus_score, energy_score, warnings, daily_advice)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            3,
            'Build Mission Control page',
            3,
            80,
            70,
            'Dont use AI too much.',
            'Reduce 1000 calories.'
        ))

    c.execute('SELECT COUNT(*) FROM mission_control')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO mission_control
            (daily_mission, weekly_missions, long_term_goals, XP_points, streaks, failed_missions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'Complete today coding session',
            'Finish Command Center and Mission Control pages',
            'Build StarkOS into a full personal dashboard',
            120,
            6,
            'Missed workout yesterday'
        ))

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
