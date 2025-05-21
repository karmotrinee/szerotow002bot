from flask import Flask, request
import requests
import os
import sys

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/tradingview', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.get_json()
        print("✅ 수신된 데이터:", data)
        sys.stdout.flush()  # 로그 강제 출력

        symbol = data.get('symbol', 'N/A')
        price = data.get('price', 'N/A')
        signal = data.get('signal', 'N/A')
        time = data.get('time', 'N/A')

        message = f"📈 트레이딩뷰 시그널\n\n🪙 종목: {symbol}\n💵 가격: {price}\n📌 시그널: {signal}\n⏰ 시간: {time}"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}

        res = requests.post(url, data=payload)
        print("📤 텔레그램 응답 코드:", res.status_code)
        print("📩 텔레그램 응답 내용:", res.text)
        sys.stdout.flush()

    except Exception as e:
        print("❌ 예외 발생:", str(e))
        sys.stdout.flush()

    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

