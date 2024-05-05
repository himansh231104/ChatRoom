import sqlite3

# Connect to the SQLite database
# If the database does not exist, it will be created automatically
conn = sqlite3.connect('chatrooms.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the chatrooms table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS chatrooms (
#         chatroom_id TEXT PRIMARY KEY CHECK(LENGTH(chatroom_id) = 5),
#         chatroom_password TEXT NOT NULL,
#         chatroom_status TEXT CHECK(chatroom_status IN ('active', 'deactive')) NOT NULL,
#         total_members INTEGER DEFAULT 0,
#         file_path TEXT
#     )
# ''')

# Create the members table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS members (
#         userid TEXT PRIMARY KEY,
#         password TEXT NOT NULL,
#         created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#         color_theme TEXT DEFAULT 'default',
#         chatroom_id TEXT,
#         FOREIGN KEY (chatroom_id) REFERENCES chatrooms (chatroom_id)
#     )
# ''')

    # Define sample entries to insert into the chatrooms table
sample_chatrooms = [
        ('room1', 'password1', 'active', 3, '/path/to/chatroom1.txt'),
        ('room2', 'password2', 'active', 5, '/path/to/chatroom2.txt'),
        ('room3', 'password3', 'deactive', 0, '/path/to/chatroom3.txt')
    ]
cursor.execute('''delete from chatrooms;''')   
    # Insert sample entries into the chatrooms table
cursor.executemany('''
        INSERT INTO chatrooms (chatroom_id, chatroom_password, chatroom_status, total_members, file_path)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_chatrooms)

# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
