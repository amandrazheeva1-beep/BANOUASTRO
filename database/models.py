from database.db import cursor, conn

def save_user(tg_id, name, birthdate, request):
    cursor.execute("""
    INSERT INTO users (tg_id, name, birthdate, request, status)
    VALUES (?, ?, ?, ?, ?)
    """, (tg_id, name, birthdate, request, "new"))

    conn.commit()
  
