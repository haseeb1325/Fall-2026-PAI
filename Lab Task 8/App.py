from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "5bd283f1eb84439fe350db749cf2a3a9"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    data = request.get_json()
    city = data.get("city", "").strip()

    if not city:
        return jsonify({"error": "City not provided"}), 400

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)
