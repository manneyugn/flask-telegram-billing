from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import telegram
import requests
import json


app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SAMPLE_SPREADSHEET_ID = "1XqamczY56e232SfJv77yObfjC8sZiEet-yHUpgeHpbo"
SAMPLE_RANGE_NAME = "Class Data!A2:E"


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
        print("body", body)
        message = body["message"]
        if message is not None:
            if "text" in message:
                text = message["text"]
                sender = message["from"]
                if text is not None:
                    bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))
                    token = text.split()
                    if len(token) > 0:
                        if token[0] == "/start":
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"), text="/start"
                            )
                        elif token[0] == "/buy":
                            try:
                                res = requests.get(
                                    os.getenv("GOOGLE_APP_SCRIPT")
                                    + "?item="
                                    + " ".join(token[1 : len(token) - 1])
                                    + "&price="
                                    + token[len(token) - 1]
                                    + "&buyer="
                                    + sender["last_name"]
                                    + " "
                                    + sender["first_name"]
                                )
                                data = json.loads(res.text)
                                if data["result"] == "success":
                                    await bot.send_message(
                                        chat_id=os.getenv("CHAT_ID"),
                                        text="Mua hàng thành công "
                                        + " ".join(token[1 : len(token) - 1])
                                        + " với giá "
                                        + token[len(token) - 1],
                                    )
                                else:
                                    await bot.send_message(
                                        chat_id=os.getenv("CHAT_ID"),
                                        text="Mua hàng thất bại " + data["error"],
                                    )
                            except:
                                await bot.send_message(
                                    chat_id=os.getenv("CHAT_ID"),
                                    text="Mua hàng thất bại " + data["error"],
                                )
                        elif token[0] == "/link":
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"),
                                text="vào đây để xem bảng chi trong tháng "
                                + os.getenv("LINK_SHEET"),
                            )
                        else:
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"),
                                text="Câu lệnh chưa được hỗ trợ",
                            )
        return jsonify(isError=False, message="Success", statusCode=200, data="POST")
