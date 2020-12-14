from Employee import Employee

EmployeeData = ['Bruce Wayne', 'Clark Kent', 'Hulk Hogan', 'Tony Stark', 'Kobe Bryant']

class Employees:
    def __init__(self, pos):
        self.pos = pos
        self.employees = []

        for name in EmployeeData:
            self.employees.append(Employee(name))

        self.pos.db.insert_many(self.employees, commit=True)       

    def print_all(self):
        """Prints all employees"""

        # print heading
        print('{0:20}|{1:^20}|{2:>20}'.format('Employee Name', 'Employee ID', 'Clocked In'))

        # print each employee
        for emp in self.employees:
            clocked_in = 'Y' if emp.clocked_in else 'N'
            print('{0:20}|{1:^20}|{2:>20}'.format(emp.name, emp.id, clocked_in))

    def add(self, employee):
        self.pos.db.insert(employee, commit=True)
        self.employees.append(employee)

    def get(self, id=None):
        target = None
        for emp in self.employees:
            if emp.id == id:
                target = emp
                break
        return target