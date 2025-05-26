import sqlite3
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = "7771692085:AAEyU45cduOSEZIa4we1d2kUTqD83ula4H4"
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def check_code(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text("Utilisation : /code <votre_code>")
        return

    user_code = context.args[0]
    user_id = update.message.chat_id

    conn = sqlite3.connect("~/Termux-TiviMate/config/system_data.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM user_access WHERE code=?", (user_code,))
    result = cursor.fetchone()

    if result and result[0] == "Actif":
        cursor.execute("UPDATE user_access SET status='Utilisé', user_id=? WHERE code=?", (user_id, user_code))
        conn.commit()
        update.message.reply_text("✅ Code validé ! Votre accès IPTV est activé.")
    else:
        update.message.reply_text("⛔ Code invalide ou déjà utilisé.")

    conn.close()

dispatcher.add_handler(CommandHandler("code", check_code))
updater.start_polling()
updater.idle()
