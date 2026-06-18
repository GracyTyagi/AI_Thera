import sqlite3
import hashlib
from datetime import datetime

# Function to hash passwords for security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# Database connection and table creation
def create_usertable():
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

def create_moodtable():
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moodtable(
                    username TEXT, 
                    mood_text TEXT, 
                    sentiment TEXT, 
                    sentiment_score REAL, 
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

# User Management Functions
def add_userdata(username, password):
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, make_hashes(password)))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def login_user(username, password):
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

# Mood Management Functions
def add_mooddata(username, mood_text, sentiment, score):
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO moodtable(username, mood_text, sentiment, sentiment_score, timestamp) VALUES (?,?,?,?,?)', 
              (username, mood_text, sentiment, score, timestamp))
    conn.commit()
    conn.close()

def get_user_moods(username):
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('SELECT mood_text, sentiment, sentiment_score, timestamp FROM moodtable WHERE username = ? ORDER BY timestamp DESC', (username,))
    data = c.fetchall()
    conn.close()
    return data

def view_all_users():
    conn = sqlite3.connect('wellness.db')
    c = conn.cursor()
    c.execute('SELECT username FROM userstable')
    data = c.fetchall()
    conn.close()
    return data
