import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()
import os
import telebot
from google import genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

SYSTEM_PROMPT = "You are MuslimFarouk Bot. FIRST language is HAUSA. Reply in Hausa unless user uses English, Arabic, French, Chinese. Help with Quran, Hadith, Duas. Be short, friendly, respectful. Advise to ask scholar for serious fatwa."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalamu Alaikum! Ni ne MuslimFarouk Bot. Ka tambaye ni komai a Hausa, Turanci, Larabci, Faransanci ko Chinese. Menene zan taimaka maka?")

@bot.message_handler(func=lambda message: True)
def answer(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=SYSTEM_PROMPT + "\n\nUser: " + message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(e)

bot.delete_webhook(drop_pending_updates=True)
print("MuslimFarouk Bot yana aiki...")
bot.polling(none_stop=True, interval=0, timeout=20)
