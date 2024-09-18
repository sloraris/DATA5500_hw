class Onewheel:
    def __init__(self, owner, mileage, max_speed, battery_range):
        self.owner = owner
        self.mileage = mileage
        self.max_speed = max_speed
        self.battery_range = battery_range

    def __str__(self):
        return f"Owner: {self.owner}, Mileage: {self.mileage}, Max Speed: {self.max_speed}, Range: {self.battery_range}"

class Pint(Onewheel):
    def __init__(self, owner, mileage):
        super().__init__(owner, mileage, 16, 6)  # Call parent constructor

    def __str__(self):
        return f"Pint {super().__str__()}"  # Extend parent __str__

class GT(Onewheel):
    def __init__(self, owner, mileage):
        super().__init__(owner, mileage, 20, 32)  # Call parent constructor

    def __str__(self):
        return f"GT {super().__str__()}"  # Extend parent __str__

# Create instances
pint = Pint("Parker", 160)
print(pint)  # Pint Owner: Parker, Mileage: 160, Max Speed: 16, Range: 6

gt = GT("Chris", 50)
print(gt)  # GT Owner: Chris, Mileage: 50, Max Speed: 20, Range: 32
