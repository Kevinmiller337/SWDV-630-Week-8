from Vendor import Order, Vendor

class Orders:

    def __init__(self, pos):
        self.pos = pos

    def __get_parsed_date(self):
        date = input('Requested delivery date? (YYYY/MM/DD) ')
        (year, month, day) = date.split('/')

        return int(year), int(month.lstrip('0')), int(day.lstrip('0'))

    def __print_active_orders(self):
        """Prints all orders"""

        orders = []

        for vendor in self.pos.open_vendors().vendors:
            for order in vendor.get_active_orders():
                orders.append(order)
            
        # # print vendor heading
        print('{0:<20} | {1:^20} | {2:>20} | {3:>20}'.format('Order ID', 'Order Item', 'Order Quantity', 'Order Price'))

        # # print each vendor
        for order in orders:
            print('{0:<20} | {1:^20} | {2:>20} | ${3:>19.2f}'.format(order.id, order.item.name, order.quantity, order.price))

    def __get_order_details(self, vendor):
        vendor.print_items()
        item_id = input('\nEnter item ID to order: ')
        quantity = input('Enter quantity to order: ')
        return (item_id, quantity)

    def new(self):
        vendors = self.pos.open_vendors()
        vendors.print_all()

        vendor_id = int(input('\nEnter vendor ID to create order: '))
        if vendor_id:
            vendor = self.pos.db.query(Vendor, 'id={}'.format(vendor_id))
            year, month, day = self.__get_parsed_date()

            item = self.__get_order_details(vendor)
            vendor.create_order(year=year, month=month, day=day, item=item)

            self.pos.db.commit()
        
        vendors.print_all()

    def update(self):
        self.__print_active_orders()

        order_id = input('\nEnter order ID to update: ')
        if order_id:
            order = self.pos.db.query(Order, 'id={}'.format(order_id))
            if order:
                update_quantity = input('Do you want to update the quantity? (y/n) ') == 'y'
                if update_quantity:
                    new_quantity = input('Enter new quantity: ')
                    order.set_quantity(new_quantity)
                    self.pos.db.commit()
            else:
                print('\nOrder with ID %r does not exist' % (order_id))

    def cancel(self):
        self.__print_active_orders()

        order_id = input('\nEnter order ID to cancel: ')
        if order_id:
            order = self.pos.db.query(Order, 'id={}'.format(order_id))
            order.cancel()
        
        self.__print_active_orders()
