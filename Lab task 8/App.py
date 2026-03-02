from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Paste API link here 👇
API_URL = "https://api.deezer.com/search?q="  # <-- Paste API here

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    response = requests.get(API_URL + query)
    data = response.json()
    songs = data.get('data', [])
    return render_template('index.html', songs=songs, query=query)

if __name__ == '__main__':
    app.run(debug=True)
