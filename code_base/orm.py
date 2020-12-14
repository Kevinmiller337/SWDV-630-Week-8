from sqlalchemy import create_engine, Column, Integer, String, Float, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DB:

    class MultipleResultsError(Exception):
        pass

    Base = declarative_base()

    __instance = None

    def __dirty_session(self):
        return self.session.dirty

    dirty = property(__dirty_session, None, None)

    def __new_session(self):
        return self.session.new

    new = property(__new_session, None, None)

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            instance = object.__new__(cls)
            # set instance attributes
            engine = create_engine('sqlite:///', echo=False)
            instance.engine = engine
            cls.Base.metadata.create_all(engine)
            instance.session = sessionmaker(bind=engine)()
            cls.__instance = instance
        return cls.__instance

    @staticmethod
    def __split_key_val_pair(string):
        """
            Splits a string with n key/val pairs

            @param {string} a string with key val pairs, each pair must be seperated with a comma, and each key/val must be separated with '='
                    @example 'name=Pizza, type=Large'
            
            @return {tuple[]} an array of tuples representing key/val pairs
                    @example [('name', 'Pizza'), ('type', 'large')]
        """

        pairs = []
        split = string.split(',')
        for key_val_pair in split:
            stripped_pair = key_val_pair.strip()
            key, val = stripped_pair.split('=')
            pairs.append((key.strip(), val.strip()))
        return pairs

    @staticmethod
    def __build_query(cls, params):
        """
            Builds a query filter statement

            @param {class} cls = the class type to search
            @param {tuple[]} params = an array of tuples representing key/val pairs
                    @example [('name', 'Pizza'), ('type', 'medium')]
            
            @returns {object[]}
        """
        
        query = []
        for key, val in params:
            query.append(getattr(cls, key) == val)
        return query

    def __get_query(self, cls, key_val_pair_string):
        """Facilitates the generation of a DB query"""

        return self.__build_query(
            cls, 
            self.__split_key_val_pair(key_val_pair_string)
        )

    def query(self, cls, key_val_pair_string):
        """
            Query a specific item in the DB.

            @param {class} cls = the class type to search
            @param {string} key_val_pair_string = the key val pair string 
                        example: 'foo=bar, charlie=brown'

            Example Usage: 
                item1 = db.query(<class>, 'name=Pants, color=blue')
        """

        items = None

        try:
            if cls == None or key_val_pair_string == None:
                return

            query = self.__get_query(cls, key_val_pair_string)
        
            items = self.session.query(cls).filter(*query).all()
            
            # if multiple items were returned, warn the user
            if len(items) > 1:
                raise DB.MultipleResultsError()

        except DB.MultipleResultsError: 
            # catch the exception if multiple items were returned from the query and print a warning message 
            print('Multiple results returned: type = %r, query = %r; returning first result. %r' % (cls, key_val_pair_string, items[0]))

        return items[0]

    def query_all(self, cls):
        """
            Query all items of a specific type

            @param {class} cls = the class type to search

            Example Usage:
                items = db.query_all(<class>)
        """

        if cls == None:
            return
        return self.session.query(cls).all()

    def insert(self, item, commit=False):
        """Add an item to the DB"""

        self.session.add(item)
        if commit:
            self.commit()

    def insert_many(self, items, commit=False):
        """Add multiple items to the DB"""

        self.session.add_all(items)
        if commit:
            self.commit()

    def commit(self):
        """Commit updates to the DB"""

        self.session.commit()

    def cancel_update(self):
        """Cancel updates to the DB"""

        self.session.rollback()


class Item(DB.Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    color = Column(String)

    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.color = color

    def __repr__(self):
        return 'Item<%r, %r, %r>' % (self.name, self.price, self.color)


if __name__ == '__main__':
    # instantiate the DB class
    db = DB()

    # add some items
    db.insert(Item('Pizza-small', 12.99, 'two-toppings'))

    # validate the session has an uncommitted update
    assert(len(db.new) == 1)

    db.insert_many([
            Item('Pizza-sml', 9.99, 'one-toppings'),
            Item('Pizza-med', 12.99, 'one-toppings'),
            Item('Pizza-lrg', 14.99, 'one-toppings'),
            Item('Pizza-xlrg', 19.99, 'one-toppings'),
            Item('Pizza-sml', 12.99, 'two-toppings'),
            Item('Pizza-med', 14.99, 'two-toppings'),
            Item('Pizza-lrg', 19.99, 'two-toppings'),
            Item('Pizza-xlrg', 25.99, 'two-toppings'),
        ], commit=True)
    
    # increment the price of all items by 1
    for item in db.query_all(Item):
        item.price += 1
    
    # commit the updated pricing
    db.commit()

    # print the pricing for manual validation
    # for item in db.query_all(Item):
    #     print(item.price)

    # validate the pricing has increased by 1
    assert(db.query(Item('Pizza-xlrg', 25.99, 'two-toppings')))
    

    # update the name of the hat
    pizza = db.query(Item, 'name=pizza, size=lrg')
    assert(type(pizza) == Item)
    Pizza.name = 'Large Pizza'

    # validate the session is dirty
    assert(len(db.dirty) == 1)

    # cancel the update of the pizza name
    db.cancel_update()

    # validate the update was not committed
    assert(len(db.dirty) == 0)
    assert(Pizza.name == 'Large Pizza')
