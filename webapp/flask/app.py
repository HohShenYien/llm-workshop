from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai

model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="API_KEY")

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 128,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

app = Flask(__name__)
CORS(app)


@app.route("/hello")
def hello_world():
    return {"message": "Hello, World!"}


@app.route("/prompt", methods=["POST"])
def chat():
    data = request.json

    responses = model.generate_content(
        data["prompt"],
        generation_config=generation_config,
        stream=False,
    )
    response = jsonify({"response": responses.text})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
