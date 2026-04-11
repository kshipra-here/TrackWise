from database import get_connection

def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, createdAt) VALUES (?, ?, ?, datetime('now'))",
        (name, email, password)
    )
    conn.commit()
    conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT userID, name FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    return user


