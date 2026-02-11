from database.db import cursor, conn

def save_user(tg_id, name, birthdate, place of birth, request):
    cursor.execute("""
    INSERT INTO users (tg_id, name, birthdate, place of birth, request, status)
    VALUES (?, ?, ?, ?, ?)
    """, (tg_id, name, birthdate, place of birth, request, "new"))

    conn.commit()
  
