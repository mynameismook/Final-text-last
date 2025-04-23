import json
import random
import os
from flask import Blueprint, render_template, jsonify, request
from .sentiment_model import predict_sentiment

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/random_food')
def random_food():
    data_path = os.path.join(os.path.dirname(__file__), 'food_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        food_data = json.load(f)
    selected_food = random.choice(food_data)
    return jsonify(selected_food)


@main.route('/search_food')
def search_food():
    query = request.args.get('q', '').lower()
    data_path = os.path.join(os.path.dirname(__file__), 'food_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        food_data = json.load(f)
    results = [item for item in food_data if query in item['name'].lower() or query in item['eng_name'].lower()]
    return jsonify(results)


@main.route('/comment', methods=['POST'])
def add_comment():
    try:
        comment = request.json.get('comment', '').strip()
        print("📩 Received comment:", comment)

        if not comment:
            return jsonify({'error': 'กรุณากรอกข้อความคอมเมนต์'}), 400

        sentiment = predict_sentiment(comment)
        print("✅ Predicted sentiment:", sentiment)

        comment_entry = {
            'text': comment,
            'sentiment': sentiment
        }

        file_path = os.path.join(os.path.dirname(__file__), 'comments.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                comments = json.load(f)
        except FileNotFoundError:
            comments = []

        comments.append(comment_entry)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

        return jsonify({'message': 'คอมเมนต์ถูกบันทึกแล้ว', 'data': comment_entry})

    except Exception as e:
        print("❌ Error while adding comment:", e)
        return jsonify({'error': 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์'}), 500


@main.route('/comments')
def get_comments():
    file_path = os.path.join(os.path.dirname(__file__), 'comments.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError:
        comments = []
    return jsonify(comments)
