import sqlite3
import requests
import time
from selenium import webdriver

conn = sqlite3.connect("~/Termux-TiviMate/config/system_data.db", check_same_thread=False)
cursor = conn.cursor()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

def check_streams():
    cursor.execute("SELECT id, page_url, stream_url FROM iptv_links WHERE status='Actif'")
    streams = cursor.fetchall()

    for stream_id, page_url, stream_url in streams:
        try:
            response = requests.get(stream_url, timeout=5)
            if response.status_code in [403, 401]:
                replace_stream(stream_id, page_url)
        except requests.exceptions.RequestException:
            replace_stream(stream_id, page_url)

def replace_stream(stream_id, page_url):
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    time.sleep(5)

    new_streams = driver.execute_script("return performance.getEntries().map(e => e.name).filter(n => n.includes('.m3u8'));")
    driver.quit()

    if new_streams:
        new_url = new_streams[0]
        cursor.execute("UPDATE iptv_links SET stream_url=?, status='Remplacé' WHERE id=?", (new_url, stream_id))
        conn.commit()
        print(f"✅ Flux IPTV remplacé : {new_url}")
    else:
        print("🚨 Aucun flux alternatif détecté.")

while True:
    check_streams()
    time.sleep(1800)
