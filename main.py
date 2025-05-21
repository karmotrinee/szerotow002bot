from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 환경변수에서 토큰과 채팅 ID 불러오기
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/tradingview', methods=['POST'])
def tradingview_webhook():
    # 📌 진단용 로그: 트레이딩뷰에서 전송된 데이터 확인
    data = request.get_json()
    print("✅ 수신된 데이터:", data)

    symbol = data.get('symbol', 'N/A')
    price = data.get('price', 'N/A')
    signal = data.get('signal', 'N/A')
    time = data.get('time', 'N/A')

    message = f"📈 트레이딩뷰 시그널\n\n🪙 종목: {symbol}\n💵 가격: {price}\n📌 시그널: {signal}\n⏰ 시간: {time}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        res = requests.post(url, data=payload)
        print("📤 텔레그램 응답 코드:", res.status_code)
        print("📩 텔레그램 응답 내용:", res.text)
    except Exception as e:
        print("❌ 텔레그램 전송 중 예외 발생:", str(e))

    return 'ok', 200

# Render 서버 실행용 포트 설정
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
