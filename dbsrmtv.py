import sqlite3

conn = sqlite3.connect("~/Termux-TiviMate/config/system_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS iptv_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url TEXT,
    stream_url TEXT,
    status TEXT DEFAULT 'Actif'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_access (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE,
    code TEXT UNIQUE,
    status TEXT DEFAULT 'Actif',
    expiry_time INTEGER
)
""")

conn.commit()
conn.close()
