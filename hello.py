from flask import Flask
from flask import request
from flask import json

import requests
import settings

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':settings.CHANNEL_ID,
    'X-Line-ChannelSecret':settings.CHANNEL_SECRET,
    'X-Line-Trusted-User-With-ACL':settings.MID
}

app = Flask(__name__)

def post_event(to, content):
    msg = {
            'to': to,
            'toChannel': 1383378250,
            'eventType': "138311608800106203",
            'content': content
    }
    r = requests.post(LINEBOT_API_EVENT, headers = LINE_HEADERS, data = json.dumps(msg))
    print(json.dumps(msg))

def post_text(to, text):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)

@app.route("/")
def hello():
    return("started")

@app.route("/callback", methods=['POST'])
def callback():
    result = request.json['result']
    for message in result:
        sender = message['content']['from']
        response = 'Your MID is ' + sender + '\nStay metal.'
        print(sender)
        response = post_text([sender], response)
        print(result)
        
    return("")

if __name__ == "__main__":
    app.run(debug=True)
