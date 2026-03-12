from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import os

app = Flask(__name__)

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    symbol = data.get('symbol')
    side = data.get('side')
    qty = data.get('qty', '1')
    
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        return jsonify({'status': 'success', 'order_id': order.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Webhook Server Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
