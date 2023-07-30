from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Replace 'database.db' with the path to your SQLite database file
DATABASE_FILE = 'database.db'


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sentences
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, sentence TEXT)''')
    conn.commit()
    conn.close()


@app.route('/save', methods=['POST'])
def save_sentence():
    data = request.get_json()
    if 'sentence' not in data:
        return jsonify({"error": "Invalid request. 'sentence' field is missing."}), 400

    sentence = data['sentence']
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # First, check if there's an existing sentence in the database
    cursor.execute('SELECT * FROM sentences LIMIT 1')
    existing_sentence = cursor.fetchone()

    if existing_sentence:
        # If there's an existing sentence, update it
        cursor.execute('UPDATE sentences SET sentence = ?', (sentence,))
    else:
        # If there's no existing sentence, insert a new row
        cursor.execute('INSERT INTO sentences (sentence) VALUES (?)', (sentence,))
        
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Sentence saved successfully."}), 201


@app.route('/get', methods=['GET'])
def get_sentence():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT sentence FROM sentences LIMIT 1')
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"error": "No sentences found in the database."}), 404

    sentence = result[0]
    return jsonify({"sentence": sentence}), 200


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
