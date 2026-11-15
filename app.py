from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = 'database.json'

# JSON ဖိုင်ကနေ Data ဖတ်ရန်
def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# JSON ဖိုင်ထဲ Data သိမ်းရန်
def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(load_data())

@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.json
    data = load_data()
    data.append(new_product)
    save_data(data)
    return jsonify({"status": "success", "product": new_product})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    data = load_data()
    data = [p for p in data if p.get('id') != product_id]
    save_data(data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
