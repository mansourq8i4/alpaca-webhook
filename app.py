from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import os
import threading

app = Flask(__name__)

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

def execute_order(symbol, side, notional):
    try:
        if side == 'sell':
            # تحقق هل عندك رصيد قبل البيع
            try:
                position = api.get_position(symbol)
                if float(position.qty) <= 0:
                    print(f"No position for {symbol}, skipping sell")
                    return
            except:
                print(f"No position for {symbol}, skipping sell")
                return

        api.submit_order(
            symbol=symbol,
            notional=notional,
            side=side,
            type='market',
            time_in_force='ioc'
        )
        print(f"Order: {side} ${notional} {symbol}")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'status': 'ok'}), 200

    symbol = data.get('symbol', '')
    side = data.get('side', '')
    notional = float(data.get('notional', 450))

    thread = threading.Thread(target=execute_order, args=(symbol, side, notional))
    thread.start()

    return jsonify({'status': 'ok'}), 200

@app.route('/')
def home():
    return "Running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
