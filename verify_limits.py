import sys
import os
import hashlib
from backend.repositories.wallet_repo import WalletRepository
from backend.database.connection import get_db_connection

def verify_limits():
    repo = WalletRepository()
    conn = get_db_connection()
    cursor = conn.cursor()
    print("--- SETUP TEST USER ---")
    email = "test_strict_limit@example.com"
    username = "StrictTest"
    
    # Cleanup
    for ident in [email, username]:
        sql = "SELECT id FROM akun WHERE email=%s" if '@' in ident else "SELECT id FROM akun WHERE username=%s"
        cursor.execute(sql, (ident,))
        res = cursor.fetchone()
        if res:
            uid = res[0]
            cursor.execute("DELETE FROM transaksi WHERE akun_id=%s", (uid,))
            cursor.execute("DELETE FROM akun WHERE id=%s", (uid,))
            conn.commit()

    password_hash = hashlib.sha256("123456".encode()).hexdigest()
    cursor.execute("INSERT INTO akun (username, email, password, no_telp, saldo) VALUES (%s, %s, %s, %s, %s)", (username, email, password_hash, "081234567890", 0))
    conn.commit()
    cursor.execute("SELECT id FROM akun WHERE email=%s", (email,))
    user_id = cursor.fetchone()[0]
    print(f"Created User ID: {user_id}")

    print("\n--- TEST 1: Fill Max Balance (10jt) ---")
    success, msg = repo.create_transaction(user_id, 10_000_000, "MASUK", "TOP_UP", "Fill 10jt")
    if success: print(f"[PASS] {msg}")
    else: print(f"[FAIL] {msg}")

    print("\n--- TEST 2: Add 1jt (Total 11jt) - Should Fail (Balance Limit) ---")
    success, msg = repo.create_transaction(user_id, 1_000_000, "MASUK", "TOP_UP", "Overflow")
    if not success and "Saldo akan melebihi 10jt" in msg: print(f"[PASS] Blocked: {msg}")
    else: print(f"[FAIL] Result: {success}, Msg: {msg}")

    print("\n--- TEST 3: Drain 10jt (Balance -> 0) ---")
    success, msg = repo.create_transaction(user_id, 10_000_000, "KELUAR", "TARIK_TUNAI", "Drain")
    if success: print(f"[PASS] Drained. In: 10jt, Out: 10jt.")
    else: print(f"[FAIL] {msg}")

    print("\n--- TEST 4: Refill 10jt (Total In 20jt) ---")
    success, msg = repo.create_transaction(user_id, 10_000_000, "MASUK", "TOP_UP", "Refill")
    if success: print(f"[PASS] Refilled. In: 20jt. Balance: 10jt.")
    else: print(f"[FAIL] {msg}")

    print("\n--- TEST 5: Add 1jt (Total In 21jt) - Should Fail (Income Limit) ---")
    # Need to reduce balance first to ensure it's not Balance Limit blocking it
    cursor.execute("UPDATE akun SET saldo=0 WHERE id=%s", (user_id,))
    conn.commit()
    success, msg = repo.create_transaction(user_id, 1_000_000, "MASUK", "TOP_UP", "Over Income")
    if not success and "Limit pemasukan" in msg: print(f"[PASS] Blocked: {msg}")
    else: print(f"[FAIL] Result: {success}, Msg: {msg}")

    print("\n--- TEST 6: Expenditure Limit Check ---")
    # Current Out: 10jt (from Test 3).
    # Drain another 10jt (Total Out 20jt). Enforce via SQL to bypass limit temporarily or standard flow?
    # Standard flow: Balance 10jt. Withdraw 10jt.
    # Current State (after Test 5): Balance 0.
    # Restore Balance 10jt via SQL
    cursor.execute("UPDATE akun SET saldo=10000000 WHERE id=%s", (user_id,))
    conn.commit()
    
    repo.create_transaction(user_id, 10_000_000, "KELUAR", "TARIK_TUNAI", "Drain 2")
    # Now Out 20jt. Balance 0.
    
    # Try Out 1jt.
    cursor.execute("UPDATE akun SET saldo=5000000 WHERE id=%s", (user_id,))
    conn.commit()
    success, msg = repo.create_transaction(user_id, 1_000_000, "KELUAR", "TARIK_TUNAI", "Over Expend")
    if not success and "Limit pengeluaran" in msg: print(f"[PASS] Blocked: {msg}")
    else: print(f"[FAIL] Result: {success}, Msg: {msg}")
    
    conn.close()

if __name__ == "__main__":
    verify_limits()
