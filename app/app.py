from flask import Flask, jsonify, request, render_template
import json
import random

app = Flask(__name__)

# Load food data
with open('app/food_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    FOOD_DATA = data['foods']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random')
def random_food():
    return jsonify(random.choice(FOOD_DATA))

@app.route('/api/search')
def search_food():
    q = request.args.get('q', '').lower()
    result = next((f for f in FOOD_DATA if q in f['name'].lower() or q in f.get('eng_name', '').lower()), None)
    if result:
        return jsonify(result)
    else:
        return jsonify(None), 404

if __name__ == '__main__':
    app.run(debug=True)
