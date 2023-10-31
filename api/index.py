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
        print(request.json)
        return jsonify(isError=False, message="Success", statusCode=200, data="POST")
