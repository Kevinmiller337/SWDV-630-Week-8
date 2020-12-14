class Account:

    def __repr__(self):
        return 'Account<%r>' % self.balance

    def __init__(self, balance=0.00):
        self.balance = balance

    def credit(self, amount):
        self.balance += amount
    
    def debit(self, amount):
        self.balance -= amount

    def print(self):
        print(self)
