from Account import Account

class Person:

    def __repr__(self):
        return 'Person<%r>' % self.name

    def __init__(self, name):
        self.name = name
        self.account = Account(balance=0.00)

