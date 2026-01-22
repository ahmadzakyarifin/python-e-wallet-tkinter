from backend.database.connection import get_db_connection

def fix_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print("Checking current schema...")
        cur.execute("DESCRIBE akun")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == 'no_telp':
                print(f"Current definition: {row}")

        print("\nModifying no_telp column to VARCHAR(20)...")
        # Use MODIFY or CHANGE depending on MySQL version compatibility, MODIFY is standard
        cur.execute("ALTER TABLE akun MODIFY no_telp VARCHAR(20)")
        conn.commit()
        print("Schema update successful.")
        
        print("\nVerifying new schema...")
        cur.execute("DESCRIBE akun")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == 'no_telp':
                print(f"New definition: {row}")
                
    except Exception as e:
        print(f"Error updating schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_schema()
