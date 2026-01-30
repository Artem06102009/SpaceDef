import sqlite3
import datetime


def init_database():
    conn = sqlite3.connect('space_defender_scoress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            killed INTEGER NOT NULL,
            level INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_score(player_name, killed, level):
    conn = sqlite3.connect('space_defender_scoress.db')
    cursor = conn.cursor()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(player_name) > 20:
        player_name = player_name[:20]
    cursor.execute('''
        INSERT INTO scores (player_name, killed, level, date)
        VALUES (?, ?, ?, ?)
    ''', (player_name, killed, level, current_date))
    conn.commit()
    conn.close()
    print(f"Сохранено в БД: {player_name}")
