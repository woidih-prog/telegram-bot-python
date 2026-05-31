import os
import anthropic
from telebot import TeleBot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CHAT_ID = "5411273910"

bot = TeleBot(TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "⚡ Trading Master V5\nEnvoie: /analyse EURUSD")

@bot.message_handler(commands=["analyse"])
def analyse(message):
    pair = message.text.replace("/analyse", "").strip() or "EUR/USD"
    bot.reply_to(message, f"🔍 Analyse {pair} en cours...")
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system="Expert SMC trading. Analyse la paire et donne un score 0-100 et une décision ATTENDRE/SIGNAL/EXECUTION. Réponds en français avec: Score, Décision, Biais, Entrée, SL, TP, RR, Raisonnement.",
            messages=[{"role": "user", "content": f"Analyse {pair} maintenant. Session actuelle, contexte macro, SMC. Score et signal."}]
        )
        result = response.content[0].text
        bot.send_message(CHAT_ID, f"⚡ ANALYSE {pair}\n\n{result}")
    except Exception as e:
        bot.reply_to(message, f"❌ Erreur: {str(e)}")

bot.infinity_polling()
