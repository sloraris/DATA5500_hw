from collections import namedtuple
from dataclasses import dataclass

a = ['Bob', 'Zimmerman', 72]
d = {'first_name': 'Bob', 'last_name': 'Zimmerman', 'age': 83}

def greet(d):
    print(f"Hello, my name is {d['first_name']} and I'm {d['age']} years old.")

greet(d)

@dataclass
class Student:
    first: str
    last: str
    age: int

    def __str__(self):
        return f"Hello, my name is {self.first} {self.last} and I'm {self.age} years old."

    def are_you_older_than_100(self):
        return self.age > 100


bob = Student('Bob', 'Zimmerman', 83)

print(bob.are_you_older_than_100())

# practicing classes
