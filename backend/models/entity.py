from dataclasses import dataclass, field
from typing import List

@dataclass
class Transaction:
    id: int
    amount: float
    type: str
    source: str
    description: str
    date: str

@dataclass
class User:
    id: int
    username: str
    email: str
    no_telp: str
    saldo: float
    pemasukan: float
    pengeluaran: float
    target_pemasukan: float
    limit_pengeluaran: float
    level: str
    riwayat_transaksi: List[Transaction] = field(default_factory=list)

    def to_dict(self):
        return {
            "nama": self.username,
            "email": self.email,
            "no_hp": self.no_telp,
            "saldo": int(self.saldo),
            "level": self.level,
            "pemasukan": int(self.pemasukan),
            "pengeluaran": int(self.pengeluaran),
            "target_pemasukan": int(self.target_pemasukan),
            "limit_pengeluaran": int(self.limit_pengeluaran),
            "riwayat_transaksi": [
                {
                    "title": t.description,
                    "date": t.date,
                    "amount": int(t.amount),
                    "type": "in" if t.type == "MASUK" else "out"
                } for t in self.riwayat_transaksi
            ]
        }
