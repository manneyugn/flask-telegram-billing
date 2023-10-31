from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import telegram

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return "About"


@app.route("/billing", methods=["GET", "POST"])
async def billing():
    if request.method == "GET":
        return jsonify(isError=False, message="Success", statusCode=200, data="Billing")
    if request.method == "POST":
        body = request.json
        message = body.message
        if message is not None:
            text = message.text
            if text is not None:
                bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))

                token = text.split()
                if len(token) > 0:
                    if token[0] == "/start":
                        print("/start")
                        await bot.send_message(chat_id=-4012657625, text="/start")
                    elif token[0] == "/buy":
                        print("/buy")
                        await bot.send_message(chat_id=-4012657625, text="/buy")
                    elif token[0] == "/link":
                        print("/link")
                        await bot.send_message(chat_id=-4012657625, text="/link")
                    else:
                        print("Câu lệnh chưa được hỗ trợ")
                        await bot.send_message(
                            chat_id=-4012657625, text="Câu lệnh chưa được hỗ trợ"
                        )
        return jsonify(isError=False, message="Success", statusCode=200, data="POST")
