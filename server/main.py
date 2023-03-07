from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('gpt.db', check_same_thread=False)
table_name = 'questions'
header = ['question_id', 'answer_id', 'question', 'answer', 'conversation_id']
CORS(app)


@app.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE question_id = ?', (question_id,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        return jsonify({'error': 'Question not found'}), 404
    else:
        question = dict(zip(header, result))
        return jsonify(question)


@app.route('/api/questions', methods=['POST'])
def create_question():
    question_data = request.json
    if not question_data or 'question' not in question_data:
        return jsonify({'error': 'Invalid question data'}), 400
    cursor = conn.cursor()
    cursor.execute('INSERT INTO questions (answer_id, question, answer, conversation_id) VALUES (?, ?, ?, ?)',
                   (question_data.get('answer_id', None), question_data['question'], question_data.get('answer', None),
                    question_data.get('conversation_id', None)))
    conn.commit()
    question_id = cursor.lastrowid
    cursor.close()

    return jsonify({'question_id': question_id}), 201


@app.route('/api/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question_data = request.json
    if not question_data or 'question' not in question_data:
        return jsonify({'error': 'Invalid question data'}), 400
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE question_id = ?', (question_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Question not found'}), 404
    cursor.execute('UPDATE questions SET question = ?, answer = ? WHERE question_id = ?',
                   (question_data['question'], question_data.get('answer', result[3]), question_id))
    conn.commit()
    cursor.close()
    return '', 204


@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM questions WHERE question_id = ?', (question_id,))
    conn.commit()
    if cursor.rowcount == 0:
        cursor.close()
        return jsonify({'error': 'Question not found'}), 404
    else:
        cursor.close()
        return '', 204


@app.route('/update', methods=['POST'])
def update():
    c = conn.cursor()
    question_id = request.json['question_id']
    answer_id = request.json['answer_id']
    question = request.json['question']
    answer = request.json['answer']
    conversation_id = request.json['conversation_id']
    c.execute("UPDATE questions SET answer_id=?, question=?, answer=?, conversation_id=? WHERE question_id=?",
              (answer_id, question, answer, conversation_id, question_id))
    conn.commit()
    return jsonify({'message': 'Question updated successfully!'})


@app.route('/delete/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    c = conn.cursor()
    c.execute("DELETE FROM questions WHERE question_id=?", (question_id,))
    conn.commit()
    return jsonify({'message': 'Question deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
