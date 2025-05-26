#!/bin/bash
echo "🚀 Déploiement automatique du système IPTV..."

pkg update && pkg upgrade -y
pkg install python -y
pkg install termux-api -y
pkg install chromium -y
pkg install sqlite -y
pip install requests selenium telegram gspread pandas

mkdir -p ~/Termux-TiviMate/config
mkdir -p ~/Termux-TiviMate/reports

python3 setup_db.py
nohup python3 telegram_bot.py &
nohup python3 manage_iptv_streams.py &
cp ~/Termux-TiviMate/config/system_data.db /sdcard/TiviMate/IPTV_Users.db

echo "✅ Système IPTV opérationnel !"
