# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import json

# APIにHTTPリクエストを送るためのモジュール
import requests
# BotのチャネルIDとかが書いてあるsettings.pyを読み込む
import settings

# APIのURL
LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
# APIにリクエストを送る時のヘッダ
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':settings.CHANNEL_ID,
    'X-Line-ChannelSecret':settings.CHANNEL_SECRET,
    'X-Line-Trusted-User-With-ACL':settings.MID
}

# Flaskのおまじない
app = Flask(__name__)

# contentをto宛に送る
# NOTE: toはリストじゃないといけない
def post_event(to, content):
    # APIの仕様に従ってJSONメッセージを作る
    # pythonの辞書型（ディクショナリ）について理解しておくこと
    msg = {
            'to': to,
            'toChannel': 1383378250,
            'eventType': "138311608800106203",
            'content': content
    }
    # requestsモジュールを使ってmsgを投稿する
    # requests.post(送信先URL, headers=ヘッダ, data=JSONにエンコードされたデータ
    # NOTE: json.dumpsで辞書型をJSONデータに変換できる
    r = requests.post(LINEBOT_API_EVENT, headers = LINE_HEADERS, data = json.dumps(msg))
    # 変換されたJSONを表示する。デバック用。
    print(json.dumps(msg))

# contentをto宛に送る
# NOTE: toはリストじゃないといけない
#       この関数はcontentの部分を作ってpost_eventに渡すだけ
#       実際に送信の処理をするのはpost_event
def post_text(to, text):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)

# インデックスで適当な文字列を返すメソッド
# NOTE: これはbotには必要ない
@app.route("/")
def hello():
    # NOTE: returnした内容がブラウザに表示される
    return("started")

# /callbackにPOSTアクセスがあった時の処理
# NOTE: Flaskで @app.route(文字列) とすると、その直後のメソッドを使って応答する。
#       例えば、http://localhost:5000/というサーバが立っていたとすると
#       @app.route('/hoge')としておくと、http://localhost:5000/hoge に対して応答する
@app.route("/callback", methods=['POST'])
def callback():
    # 受け取ったリクエストメッセージに含まれるJSONメッセージをresultに保存
    # NOTE: LINE APIがcallbackに送るJSONメッセージの仕様を見ておくこと
    #       request.jsonはjsonデータをpythonの辞書型に変換したやつが入ってる。Flaskの機能。
    result = request.json['result']
    # resultは、受け取ったイベントのリストなので、forで回す
    # NOTE: pythonのforはリストやイテレータの中身を一つづつ取り出して処理してくれる
    for message in result:
        # ここはcallbackが受け取るメッセージを見ると理解できる
        sender = message['content']['from']
        # botが返すメッセージ
        response = 'Your MID is ' + sender + '\nStay metal.'
        response = post_text([sender], response)
        # デバッグ用
        print(sender)
        print(result)
        
    # ブラウザに空のメッセージを返す        
    return("")

if __name__ == "__main__":
    # Flaskのサーバをデバッグモードで起動する
    app.run(debug=True)
