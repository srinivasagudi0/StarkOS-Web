import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS command_center (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission TEXT NOT NULL,
            streaks INTEGER DEFAULT 0,
            xp_points INTEGER DEFAULT 0,
            focus_score INTEGER DEFAULT 0,
            energy_score INTEGER DEFAULT 0,
            )
    ''')
    conn.commit()
    conn.close()


def get_mission_data():

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row # This allows us to access columns by name

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM command_center')

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
