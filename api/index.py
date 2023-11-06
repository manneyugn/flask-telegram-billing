from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import telegram
import requests
import json


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1XqamczY56e232SfJv77yObfjC8sZiEet-yHUpgeHpbo'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

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
        message = body["message"]
        if message is not None:
            text = message["text"]
            sender = message['from']
            if text is not None:
                bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))
                token = text.split()
                if len(token) > 0:
                    if token[0] == "/start":
                        await bot.send_message(
                            chat_id=os.getenv("CHAT_ID"), text="/start"
                        )
                    elif token[0] == "/buy":
                        res = requests.get('https://script.google.com/macros/s/AKfycbxfTbWaY5Sx3m2Quoy6u13B40Hq1FBTw0zcVMvJxDtE5NAQtpBROY630NrWWlI8ya-8/exec?item=' + token [1] + '&price=' +token[2] + '&buyer=' + sender['last_name'] + ' ' + sender['first_name'])
                        data = json.loads(res.text)
                        if data['result'] == "success":
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"), text="Mua hàng thành công " +token [1] + " với giá " +token[2]
                            )
                        else:
                            await bot.send_message(
                                chat_id=os.getenv("CHAT_ID"), text="Mua hàng thất bại " + data['error']
                            )
                    elif token[0] == "/link":
                        await bot.send_message(
                            chat_id=os.getenv("CHAT_ID"), text="/link"
                        )
                    else:
                        await bot.send_message(
                            chat_id=os.getenv("CHAT_ID"),
                            text="Câu lệnh chưa được hỗ trợ",
                        )
        return jsonify(isError=False, message="Success", statusCode=200, data="POST")
