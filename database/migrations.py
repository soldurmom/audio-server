import sqlite3;
import sys

connection = sqlite3.connect('storage/users.db')
cursor = connection.cursor()

if len(sys.argv) > 1:
    if sys.argv[1] == '--del':
        cursor.executescript('''
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS users_auth;
        DROP TABLE IF EXISTS music;
        DROP TABLE IF EXISTS users_music;
        ''')
    else:
        print('invalid argument')

cursor.executescript('''
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_auth (
user_id INTEGER NOT NULL,
remote_key TEXT NOT NULL,
confirmed INTEGER DEFAULT 0,
last_visit TEXT NOT NULL,
UNIQUE(remote_key),
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);                     

CREATE TABLE IF NOT EXISTS music (
id TEXT PRIMARY KEY,
performer TEXT NOT NULL,
title TEXT NOT NULL,
file_path TEXT NOT NULL,
duration INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users_music (
user_id INTEGER NOT NULL,
music_id TEXT NOT NULL,
created_at TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (music_id) REFERENCES music(id) ON DELETE CASCADE
);
''')

connection.commit()
connection.close()