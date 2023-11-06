from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import telegram
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
            if text is not None:
                bot = telegram.Bot(os.getenv("TELEGRAM_KEY"))
                token = text.split()
                if len(token) > 0:
                    if token[0] == "/start":
                        await bot.send_message(
                            chat_id=os.getenv("CHAT_ID"), text="/start"
                        )
                    elif token[0] == "/buy":
                        await bot.send_message(
                            chat_id=os.getenv("CHAT_ID"), text="/buy"
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
