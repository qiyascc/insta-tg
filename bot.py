from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import sqlite3
import time

app = Client("my_bot", api_id="4662286", api_hash="b45ec4277caaa415cc2246f37c61e091", bot_token="6230545202:AAFJq69LVZqbD_h_fOc4wPdPxfzQgDvbP4U")

user_state = {}
user_data = {}


def create_table():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER, name TEXT)""")
    conn.commit()
    conn.close()


def get_user(user_id):
    create_table() 
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    user = cur.fetchone()
    conn.close()
    return user

def add_user(user_id, name):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name))
    conn.commit()
    conn.close()

def remove_user(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

@app.on_message(filters.command('start'))
def start(client, message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        message.reply_text('a', reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("a", callback_data="name")],
            ]
        ))
    else:
        message.reply_text(f"Salam {user[1]} amk")


@app.on_message(filters.command('mesaj'))
def qiyas(client, message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        message.reply_text('Size olmaz')
    else:
        text = ' '.join(message.command[1:])
        print(text)



@app.on_message(filters.command('logout'))
def logout(client, message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        message.reply_text('Onsuz da yoxduki amk')
    else:
        message.reply_text('Butona klikle', reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Oky sil", callback_data="logout")],
            ]
        ))

@app.on_callback_query(filters.create(lambda _, __, query: query.data == 'name'))
def ask_name(client, callback_query):
    callback_query.message.reply_text('Ad.')
    user_state[callback_query.from_user.id] = 'wait_for_name'

@app.on_message(filters.text & filters.private)
def process_message(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in user_state:
        if user_state[user_id] == 'wait_for_name':
            user_data[user_id] = {'name': message.text}
            user_state[user_id] = 'wait_for_number'
            message.reply_text('Reqem')
        elif user_state[user_id] == 'wait_for_number':
            number = int(message.text)
            # with open('insta.py') as f:
            #     x = int(f.read().strip())

            x = 123456
            if number == x:
                add_user(user_id, user_data[user_id]['name'])
                message.reply_text('okayy')
                del user_state[user_id]
                del user_data[user_id]
            else:
                message.reply_text('Yanlis')
                time.sleep(60)
                message.reply_text('Durduruldu')
                del user_state[user_id]
                del user_data[user_id]

@app.on_callback_query(filters.create(lambda _, __, query: query.data == 'logout'))
def logout_confirm(client, callback_query):
    remove_user(callback_query.from_user.id)
    callback_query.message.reply_text('Silindi')

app.run()
