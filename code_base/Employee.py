from sqlalchemy import Column, Integer, String, Float, Boolean
from DB import DB
from Person import Person

class Employee(Person, DB.Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    clocked_in = Column(Boolean)

    def __str__(self):
        return 'Employee<%r, clocked_in: %r>' % (self.name, self.clocked_in)

    def __init__(self, name):
        Person.__init__(self, name)
        self.clocked_in = False

    def clock_in(self):
        self.clocked_in = True

    def clock_out(self):
        self.clocked_in = False

if __name__ == '__main__':
    e = Employee('Hulk Hogan')
    print(e)

        