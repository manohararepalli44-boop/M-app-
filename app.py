from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# డేటాబేస్ మరియు టేబుల్స్ క్రియేట్ చేసే ఫంక్షన్
def init_db():
    conn = sqlite3.connect('new_instagram.db')
    cursor = conn.cursor()

    # ప్రొఫైల్ టేబుల్
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            posts_count TEXT,
            followers_count TEXT,
            following_count TEXT
        )
    ''')

    # మెసేజ్ల టేబుల్
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ప్రొఫైల్ డేటా ఖాళీగా ఉంటే డిఫాల్ట్ డేటా ఇన్సర్ట్ చేయడం
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO profile (posts_count, followers_count, following_count) VALUES ('0', '150', '180')")

    conn.commit()
    conn.close()

# యాప్ స్టార్ట్ అవ్వగానే డేటాబేస్ ప్రారంభమవుతుంది
init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('new_instagram.db')
    cursor = conn.cursor()
    cursor.execute('SELECT posts_count, followers_count, following_count FROM profile LIMIT 1')
    profile_data = cursor.fetchone()
    conn.close()

    # సేఫ్టీ గార్డ్
    if profile_data is None:
        profile_data = ('0', '150', '180')

    return render_template('index.html', profile=profile_data)

@app.route('/messenger')
def messenger():
    conn = sqlite3.connect('new_instagram.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sender, message_text FROM messages ORDER BY id ASC')
    chat_messages = cursor.fetchall()
    conn.close()

    if chat_messages is None:
        chat_messages = []

    return render_template('messenger.html', messages=chat_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.form.get('message_text')
    sender = "User"

    if message_text and message_text.strip():
        conn = sqlite3.connect('new_instagram.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender, message_text) VALUES (?, ?)', (sender, message_text))
        conn.commit()
        conn.close()

    return redirect('/messenger')

if __name__ == '__main__':
    app.run(debug=True)
  
