from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import csv
import os

app = Flask(__name__)
CORS(app)

CSV_FILE = "scraped_emails.csv"

# 🔹 Home page (Frontend)
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Email extractor
def extract_emails(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))

# 🔹 Save emails to CSV
def save_to_csv(url, emails):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Website", "Email"])

        for email in emails:
            writer.writerow([url, email])

# 🔹 API route
@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"emails": []})

    emails = extract_emails(url)
    save_to_csv(url, emails)

    return jsonify({"emails": emails})

if __name__ == "__main__":
    app.run(debug=True)
