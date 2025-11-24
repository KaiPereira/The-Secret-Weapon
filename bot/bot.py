# lemme vibe code in peace guys :(((
# like IM FR BETTER AT WEBSITES and I really want to get this out
# I IIDIDDDOOOOO KNOW SECURITY THOUGH, so me no get hacky wacky

import os
import time
import sqlite3
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from apscheduler.schedulers.background import BackgroundScheduler

DB_PATH = "queue.db"

app = App(token=os.environ["SLACK_BOT_TOKEN"])
scheduler = BackgroundScheduler()

# --- Database Setup ---

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS queue_members (
            user_id TEXT PRIMARY KEY,
            position INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS queue_state (
            id INTEGER PRIMARY KEY,
            current_index INTEGER,
            last_rotation_time INTEGER,
            rotation_hours INTEGER
        )
    """)
    # initialize queue state if missing
    c.execute("SELECT COUNT(*) FROM queue_state")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO queue_state (id, current_index, last_rotation_time, rotation_hours)
            VALUES (1, 0, ?, 4)
        """, (int(time.time()),))
    conn.commit()
    conn.close()

def get_queue():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM queue_members ORDER BY position ASC")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def add_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM queue_members WHERE user_id=?", (user_id,))
    if c.fetchone()[0] > 0:
        conn.close()
        return False
    c.execute("SELECT COUNT(*) FROM queue_members")
    position = c.fetchone()[0]
    c.execute("INSERT INTO queue_members (user_id, position) VALUES (?, ?)", (user_id, position))
    conn.commit()
    conn.close()
    return True

def remove_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM queue_members WHERE user_id=?", (user_id,))
    # reassign positions
    c.execute("SELECT user_id FROM queue_members ORDER BY position ASC")
    users = [row[0] for row in c.fetchall()]
    for i, uid in enumerate(users):
        c.execute("UPDATE queue_members SET position=? WHERE user_id=?", (i, uid))
    conn.commit()
    conn.close()

def get_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT current_index, last_rotation_time, rotation_hours FROM queue_state WHERE id=1")
    state = c.fetchone()
    conn.close()
    return list(state)

def update_state(current_index, last_rotation_time):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE queue_state
        SET current_index=?, last_rotation_time=?
        WHERE id=1
    """, (current_index, last_rotation_time))
    conn.commit()
    conn.close()


# --- Rotation Logic ---

def rotate_queue():
    users = get_queue()
    if not users:
        return

    current_index, last_ts, rotation_hours = get_state()
    current_index = (current_index + 1) % len(users)
    next_user = users[current_index]

    # update state
    update_state(current_index, int(time.time()))

    # DM notification
    app.client.chat_postMessage(
        channel=next_user,
        text=f"⏰ It's now *your turn* in the rotation!"
    )

    # channel announcement
    announce_channel = os.environ.get("ANNOUNCE_CHANNEL_ID")
    if announce_channel:
        app.client.chat_postMessage(
            channel=announce_channel,
            text=f"🔁 Rotation update: It is now <@{next_user}>'s turn!"
        )

# Run every 4 hours automatically
scheduler.add_job(rotate_queue, "interval", hours=4)
scheduler.start()


# --- Slash Commands ---

@app.command("/start-working")
def start_working(ack, body, respond):
    ack()
    user = body["user_id"]
    added = add_user(user)
    if added:
        respond("✅ You have been added to the queue.")
    else:
        respond("✅ You're already in the queue.")

@app.command("/stop-working")
def stop_working(ack, body, respond):
    ack()
    user = body["user_id"]
    remove_user(user)
    respond("❎ You have been removed from the queue.")

@app.command("/queue")
def show_queue(ack, respond):
    ack()
    users = get_queue()
    if not users:
        respond("🚫 The queue is empty.")
        return

    current_index, _, _ = get_state()

    formatted = []
    for i, uid in enumerate(users):
        marker = "🔹"
        if i == current_index:
            marker = "✅ (current)"
        formatted.append(f"{marker} <@{uid}>")

    respond("\n".join(formatted))


# --- Start App ---

if __name__ == "__main__":
    init_db()
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

