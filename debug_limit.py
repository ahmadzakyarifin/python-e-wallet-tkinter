import sys
import os
from datetime import datetime

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from backend.repositories.wallet_repo import WalletRepository
from backend.services.wallet_service import WalletService

# Init
repo = WalletRepository()
# Assume user_id = 32 (found in DB)
user_id = 32
service = WalletService(user_id)

print(f"--- DEBUGGING USER ID {user_id} ---")

# 1. Check Current Data
user_data = repo.get_user_by_id(user_id)
if not user_data:
    print("User not found!")
    sys.exit(1)

print(f"Saldo: {user_data.saldo}")
print(f"Pemasukan Bulan Ini: {user_data.pemasukan}")
print(f"Pengeluaran Bulan Ini: {user_data.pengeluaran}")

# 2. Test Top Up Limit (Max Saldo 10jt)
print("\n--- TEST 1: Top Up causing Saldo > 10jt ---")
# Calculate amount needed to exceed 10jt
gap = 10_000_000 - user_data.saldo
test_amount = gap + 50000 
print(f"Trying to Top Up: {test_amount} (Target Saldo: {user_data.saldo + test_amount})")

success, msg = service.process_topup(test_amount, "TEST_BCA")
print(f"Result: Success={success}, Msg='{msg}'")

if success:
    print("❌ BUG: Top Up SUCCEEDED but should have FAILED (Max Balance Limit)")
else:
    print("✅ OK: Top Up Failed as expected.")

# 3. Test Income Limit (Max 20jt)
print("\n--- TEST 2: Top Up causing Monthly Income > 20jt ---")
# Calculate amount needed to exceed 20jt income
gap_in = 20_000_000 - user_data.pemasukan
# If gap_in is negative, we are already over limit. Test small amount.
if gap_in < 0:
    test_amount_in = 10000
    print("User already over income limit.")
else:
    test_amount_in = gap_in + 50000
    
print(f"Trying to Top Up: {test_amount_in} (Target Income: {user_data.pemasukan + test_amount_in})")

# We expect this to fail either due to Balance limit OR Income limit.
success, msg = service.process_topup(test_amount_in, "TEST_LIMIT")
print(f"Result: Success={success}, Msg='{msg}'")

if success:
     print("❌ BUG: Top Up SUCCEEDED but should have FAILED (Income Limit)")
else:
     print("✅ OK: Top Up Failed as expected.")
