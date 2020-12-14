from Vendor import Vendor, Item

VendorData = [
    ('Troco Food', '123 Main St.', [Item('Meat', .99, 'sausage'),Item('Meat', .99, 'bacon'),Item('Meat', .99, 'pepperoni'),Item('Cheese', .99, 'shredded american'), Item('Cheese', .99, 'shredded sharp cheddar'),Item('Cheese', .99, 'shredded provolone')]),
    ('Juntico Beverages', '456 Fruitridge Ave', [Item('Beverage', 2.00, 'Lemonaides')]),
]

class Vendors:
    def __init__(self, pos):
        self.pos = pos
        vendors = []
        for name, address, items in VendorData:
            vendors.append(Vendor(name, address, items))
        
        self.pos.db.insert_many(vendors, commit=True)
        self.vendors = self.pos.db.query_all(Vendor)

    def update(self, vendor_id=None, vendor=None):
        """
            Controls the update of a vendor
        """
        if not vendor:
            if not vendor_id:
                self.print_all()
                vendor_id = input('Enter vendor ID to update: ')
            vendor = self.pos.db.query(Vendor, 'id={}'.format(vendor_id))
        
        update = input('Do you want to update the vendor name? (y/n) ') == 'y'
        if update:
            updated_name = input('What is the new vendor name? ')
            vendor.update_name(updated_name)

        update = input('Do you want to update the vendor items? (y/n) ') == 'y'
        if update:
            vendor.print_items()
            item_id = int(input('Enter Item ID to update: '))
            if item_id:
                item = vendor.get_item(item_id)

                update = input('Update name? (y/n) ') == 'y'
                if update:
                    new_name = input('Enter the new name: ')
                    item.set_name(new_name)
                
                update = input('Update type? (y/n) ') == 'y'
                if update:
                    new_type = input('Enter the new color: ')
                    item.set_type(new_type)

                update = input('Update price? (y/n) ') == 'y'
                if update:
                    new_price = float(input('Enter the new price: '))
                    item.set_price(new_price)

            print('\nUpdated items:')
            vendor.print_items()

        # save changes
        save = input('Save changes? (y/n) ') == 'y'
        if save:
            self.pos.db.commit()
        else:
            self.pos.db.cancel_update()


    def print_all(self):
        """Prints all vendors"""

        # print heading
        print('{0:20} | {1:>20} | {2:>20}'.format('Vendor ID', 'Vendor Name', 'Active Orders'))

        # print each vendor
        for vendor in self.vendors:
            print('{0:<20} | {1:>20} | {2:>20}'.format(vendor.id, vendor.name, len(vendor.get_active_orders())))


    def __get_item_details(self):
        item_name = input('\nEnter item name: ')
        item_price = float(input('Enter item price: '))
        item_color = input('Enter item color: ')
        return Item(item_name, item_price, item_color)

    def __get_vendor_details(self):
        name = input('Enter vendor name: ')

        existing_vendor = self.pos.db.query(Vendor, 'name={}'.format(name))
        if existing_vendor:
            print('Vendor %r already exists.' % existing_vendor.name)
            return self.update(vendor=existing_vendor)

        address = input('Enter vendor address: ')

        new_vendor = Vendor(name, address)
        
        more_items = True
        print('\nEnter first item available from {}'.format(name))
        while more_items:
            new_vendor.add_item(self.__get_item_details())
            more_items = input('Enter another item? (y/n) ') == 'y'
        return new_vendor

    def add(self):
        vendor = self.__get_vendor_details()
        if vendor:
            self.pos.db.insert(vendor, commit=True)
            self.vendors.append(vendor)

    def remove(self):
        self.print_all()

        remove_id = int(input('Enter the Vendor ID to remove: '))
        if remove_id:
            vendor = self.pos.db.query(Vendor, 'id={}'.format(remove_id))
            if vendor:
                confirm = input('This action is irreversible; are you sure you want to delete? (y/n) ') == 'y'
                if confirm:
                    self.pos.db.delete(vendor)
                    self.vendors = self.pos.db.query_all(Vendor)