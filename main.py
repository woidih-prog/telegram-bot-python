import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
from telebot import TeleBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = "5411273910"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "⚡ Trading Master V5 actif ! Tu recevras les signaux ici.")

@bot.message_handler(commands=["test"])
def test(message):
    bot.reply_to(message, "✅ Bot opérationnel !")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "⚡ " + message.text)

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            msg = data.get("message", "Signal reçu")
            bot.send_message(CHAT_ID, msg, parse_mode="HTML")
            self.send_response(200)
        except Exception as e:
            logger.error(e)
            self.send_response(500)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Master V5 - OK")

    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"Serveur webhook sur port {port}")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    logger.info("Bot démarré")
    bot.infinity_polling()
