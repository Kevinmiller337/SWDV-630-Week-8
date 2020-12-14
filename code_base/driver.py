from Vendor import Item

def run_uc6(pos):
    print('\n*** UC6: Create Order ***')
    orders = pos.open_orders()
    orders.new()

def run_uc7(pos):
    print('\n*** UC7: Update Order ***')
    orders = pos.open_orders()
    orders.update()

def run_uc8(pos):
    print('\n*** UC8: Cancel Order ***')
    orders = pos.open_orders()
    orders.cancel()

def run_uc11(pos):
    print('\n*** UC11: Purchase Item ***')
    register = pos.open_register()
    register.checkout()

def run_uc12(pos):
    print('\n*** UC12: Return Item ***')
    register = pos.open_register()
    register.return_item()