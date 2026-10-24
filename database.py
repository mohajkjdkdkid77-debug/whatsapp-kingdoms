import sqlite3

def init_db():
    conn = sqlite3.connect('kingdoms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id TEXT PRIMARY KEY,
            kingdom_name TEXT,
            gold INTEGER DEFAULT 1000,
            soldiers INTEGER DEFAULT 50,
            power INTEGER DEFAULT 100
        )
    ''')
    conn.commit()
    conn.close()

def create_kingdom(user_id, name):
    conn = sqlite3.connect('kingdoms.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO players (user_id, kingdom_name) VALUES (?, ?)", (user_id, name))
        conn.commit()
        return f"👑 تم تأسيس مملكة '{name}' بنجاح!\n💰 الذهب: 1000\n⚔️ الجنود: 50"
    except sqlite3.IntegrityError:
        return "⚠️ أنت تمتلك مملكة بالفعل!"
    finally:
        conn.close()

def get_status(user_id):
    conn = sqlite3.connect('kingdoms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT kingdom_name, gold, soldiers, power FROM players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"🏰 *مملكة {row[0]}*\n\n💰 الذهب: {row[1]}\n⚔️ الجيش: {row[2]} جندي\n🛡️ القوة: {row[3]}"
    else:
        return "❌ ليس لديك مملكة بعد! أرسل `!انشاء [اسم المملكة]` للبدء."
