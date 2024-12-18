from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import telegram
import requests
import json
import http.client


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

@app.route("/cat-fact")
async def catFact():
    bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))

    conn = http.client.HTTPSConnection("catfact.ninja")
    payload = ''
    headers = {
      'accept': 'application/json',
      'X-CSRF-TOKEN': 'MIiXAo8WKG85yRgxzHIJ7g2WSkg9XGlsysjdacAJ'
    }
    conn.request("GET", "/fact?max_length=200", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    
    await bot.send_message(chat_id=os.getenv("CHAT_ID"), text=data.decode("utf-8"))
    return "Ok"
    
@app.route("/billing", methods=["GET", "POST"])
async def billing():
    if request.method == "GET":
        return jsonify(isError=False, message="Success", statusCode=200, data="Billing")
    if request.method == "POST":
        body = request.json
        print("body", body)
        message = body.get("message")
        bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))
        if message is not None:
            if "text" in message:
                text = message.get("text")
                sender = message.get("from")
                if text is not None:
                    token = text.split()
                    if len(token) > 0:
                        if token[0] == "/start":
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"), text="/start"
                            )
                        elif token[0] == "/buy":
                            try:
                                if not token[len(token) - 1].isnumeric():
                                    await bot.send_message(
                                        chat_id=os.getenv("CHAT_ID"),
                                        text="Sai cú pháp, vui lòng thử lại"
                                    )
                                    return jsonify(isError=False, message="Success", statusCode=200, data="POST") 
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
        else:
            await bot.send_message(
                                        chat_id=os.getenv("CHAT_ID"),
                                        text="Vui lòng thử lại, câu lệnh chưa đúng"
                                    )
        return jsonify(isError=False, message="Success", statusCode=200, data="POST")
