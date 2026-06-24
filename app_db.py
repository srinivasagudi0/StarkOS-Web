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

    conn.commit()
    conn.close()


def get_mission_data():

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row # This allows us to access columns by name

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
        missions.append(row['mission'])
        warnings.append(row['warnings'])
        daily_advice.append(row['daily_advice'])
        total_code_hours += row['code_hours']
        focus_score += row['focus_score']
        energy_score += row['energy_score']
        streaks += row['streaks']

    # average the focus and energy scores
    if len(rows) > 0:
        focus_score = focus_score // len(rows)
        energy_score = energy_score // len(rows)
        
    return {
        'code_hours': total_code_hours,  # wwhen you come with hackatime plugin thn, the today code hours will be fetched from hackatime plugin and will be showed so absically everyday start with 0 code hours and then it will be updated with hackatime plugin and when shoudl it, so we are going to do coded hours ystday
        'missions': missions,
        'streaks': streaks,
        'focus_score': focus_score,
        'energy_score': energy_score,
        'warnings': warnings,
        'daily_advice': daily_advice
    }