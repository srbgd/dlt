import uuid
import time

# Example:
# AccountTable:
# 	Account: name=Account 1, credit=1200, id=8c42695a8bd54f4e, bank=SpearBank
# 	Account: name=Account 2, credit=140, id=f262be080bf24bdb, bank=Tinkoff
# 	Account: name=Account 3, credit=1600, id=f6952b51835f42bf, bank=SpearBank
# 	Account: name=Fee, credit=60, id=eacd9e7d595c4327, bank=
# TransactionTable:
# 	Transaction: from_id=8c42695a8bd54f4e, to_id=f6952b51835f42bf, amount=500 id=4d03a9127457498f, timestamp=1603658584.0692098
# 	Transaction: from_id=f262be080bf24bdb, to_id=8c42695a8bd54f4e, amount=700 id=bff4c2fbe532418c, timestamp=1603658584.0692325
# 	Transaction: from_id=f262be080bf24bdb, to_id=eacd9e7d595c4327, amount=30 id=2b0abf28e0fc436e, timestamp=1603658584.0692477
# 	Transaction: from_id=f262be080bf24bdb, to_id=f6952b51835f42bf, amount=100 id=b33203b7af6b40ce, timestamp=1603658584.0692759
# 	Transaction: from_id=f262be080bf24bdb, to_id=eacd9e7d595c4327, amount=30 id=48ba3d7850ab452d, timestamp=1603658584.0692906

class Account:
	def __init__(self, name, credit, bank, id = ''):
		self.name = name
		self.credit = credit
		self.id = uuid.uuid4().hex[:16]
		self.bank = bank
	
	def __str__(self):
		return f'Account: name={self.name}, credit={self.credit}, id={self.id}, bank={self.bank}'

class Transaction:
	def __init__(self, from_acc, to_acc, amount, id = '', timestamp = 0):
		self.from_id = from_acc.id
		self.to_id = to_acc.id
		self.amount = amount
		self.id = uuid.uuid4().hex[:16]
		self.timestamp = time.time()
	
	def __str__(self):
		return f'Transaction: from_id={self.from_id}, to_id={self.to_id}, amount={self.amount} id={self.id}, timestamp={self.timestamp}'

class TransactionTable:
	transactions = []
	def add_transaction(self, from_acc, to_acc, amount):
		from_acc.credit -= amount
		to_acc.credit += amount
		trx = Transaction(from_acc, to_acc, amount)
		while trx.id in [t.id for t in self.transactions]:
			trx = Transaction(from_acc, to_acc, amount)
		self.transactions.append(trx)
		return trx
	
	def __str__(self):
		return 'TransactionTable:\n\t' +'\n\t'.join(list(map(str, self.transactions)))


class AccountTable:
	accounts = []
	transactions = TransactionTable()
	def __init__(self, accounts):
		for acc in accounts:
			self.add_account(*acc)
		self.fee_account = self.add_account('Fee')
	
	def add_account(self, name, credit = 0, bank = ''):
		acc = Account(name, credit, bank)
		while acc.id in [a.id for a in self.accounts]:
			print(acc)
			print([a.id for a in self.accounts])
			acc = Account(name, credit, bank)
		self.accounts.append(acc)
		return acc
	
	def make_transaction(self, from_acc, to_acc, amount):
		fee = 0 if from_acc.bank == to_acc.bank else 30
		if from_acc.credit >= amount + fee:
			trx = self.transactions.add_transaction(from_acc, to_acc, amount)
			trx_fee = self.transactions.add_transaction(from_acc, self.fee_account, fee) if fee else None
			return (trx, trx_fee)
		return (None, None)
	
	def __getitem__(self, index):
		return self.accounts[index]
	
	def __str__(self):
		return 'AccountTable:\n\t' +'\n\t'.join(list(map(str, self.accounts)))


def main():
	table = AccountTable([
		('Account 1', 1000, 'SpearBank'),
		('Account 2', 1000, 'Tinkoff'),
		('Account 3', 1000, 'SpearBank')
	])
	table.make_transaction(table[0], table[2], 500)
	table.make_transaction(table[1], table[0], 700)
	table.make_transaction(table[1], table[2], 100)
	print(table)
	print(table.transactions)


if __name__ == '__main__':
	main()
