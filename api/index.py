from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return "About"


@app.route("/billing", methods=["GET", "POST"])
def billing():
    if request.method == "GET":
        return jsonify(isError=False, message="Success", statusCode=200, data="Billing")
    if request.method == "POST":
        return jsonify(
            isError=False, message="Success", statusCode=200, data= "POST"

        )
