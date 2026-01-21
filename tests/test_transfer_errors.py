import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent dir to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.repositories.wallet_repo import WalletRepository

class TestTransferErrors(unittest.TestCase):
    
    def setUp(self):
        self.repo = WalletRepository()

    @patch('backend.repositories.wallet_repo.get_db_connection')
    def test_receiver_not_found(self, mock_get_conn):
        # Mock DB
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Scenario: Receiver not found (fetchone returns None)
        mock_cursor.fetchone.return_value = None
        
        success, msg = self.repo.transfer_balance(1, "08123456789", 50000, "desc", "desc")
        
        self.assertFalse(success)
        self.assertEqual(msg, "Nomor tujuan tidak ditemukan")

    @patch('backend.repositories.wallet_repo.get_db_connection')
    def test_transfer_to_self(self, mock_get_conn):
        # Mock DB
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Scenario: Receiver found but ID is same as sender
        # fetchone returns (id, username)
        mock_cursor.fetchone.return_value = (1, "myself") 
        
        success, msg = self.repo.transfer_balance(1, "08123456789", 50000, "desc", "desc")
        
        self.assertFalse(success)
        self.assertEqual(msg, "Tidak bisa transfer ke diri sendiri")

    @patch('backend.repositories.wallet_repo.get_db_connection')
    def test_insufficient_balance(self, mock_get_conn):
        # Mock DB
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Scenario: Receiver found (ID 2), but Sender (ID 1) insufficient balance
        # 1. Check receiver -> returns (2, "other")
        # 2. Check balance -> returns (40000,)
        def side_effect(*args):
             # First call is fetchone for receiver
             # Second call is fetchone for sender balance
             return [(2, "other"), (40000,)]
        
        # Simulating sequential fetchone calls requires side_effect on the iterator or managing call count
        # Easier: mock_cursor.fetchone.side_effect = [(2, "other"), (40000,)]
        mock_cursor.fetchone.side_effect = [(2, "other"), (40000,)]

        success, msg = self.repo.transfer_balance(1, "08123456789", 50000, "desc", "desc")
        
        self.assertFalse(success)
        self.assertEqual(msg, "Saldo tidak mencukupi")

if __name__ == '__main__':
    unittest.main()
