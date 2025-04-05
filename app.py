from flask import Flask, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

# Solana base58 address validation
solana_regex = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')

@app.route('/submit', methods=['GET'])
def save_address():
    address = request.args.get('address', '').strip()

    if not address:
        return jsonify({'error': 'Missing address parameter'}), 400

    if not solana_regex.match(address):
        return jsonify({'error': 'Invalid Solana address'}), 400

    try:
        with open('solana_addresses.txt', 'a') as f:
            f.write(f"{address} - {datetime.utcnow().isoformat()} UTC\n")
        return jsonify({'message': 'Address saved successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to save address: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

