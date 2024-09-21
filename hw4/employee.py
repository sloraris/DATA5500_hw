class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def promote(self, increase):
        self.salary *= (1 + (increase / 100))
        print(f"Employee {self.name} has been promoted! New salary: ${self.salary}")

employee1 = Employee("John", 5000)
employee1.promote(10)
