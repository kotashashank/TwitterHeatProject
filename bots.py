from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-bot-score', methods=['POST'])
def get_bot_score():
    url = "https://botometer.osome.iu.edu/api/get-score"
    headers = {
        "User-Agent": request.headers.get('User-Agent'),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "X-CSRFToken": request.headers.get('X-CSRFToken'),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    data = request.json(content_type=None)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.raw())
    else:
        return jsonify(response.raw())

if __name__ == '__main__':
    app.run(debug=True)
