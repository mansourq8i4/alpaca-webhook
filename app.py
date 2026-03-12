from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import os
import threading

app = Flask(__name__)

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

def execute_order(symbol, side, qty):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"Order: {side} {qty} {symbol}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'status': 'ok'}), 200
    
    symbol = data.get('symbol', '')
    side = data.get('side', '')
    qty = data.get('qty', '1')
    
    # رد فوري ثم نفذ الأمر في الخلفية
    thread = threading.Thread(target=execute_order, args=(symbol, side, qty))
    thread.start()
    
    return jsonify({'status': 'ok'}), 200

@app.route('/')
def home():
    return "Running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
