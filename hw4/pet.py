class Pet:
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def life_span(self):
        if self.species == "Dog":
            print(f"{self.name} has a life span of 10-13 years")
        elif self.species == "Cat":
            print(f"{self.name} has a life span of 15-20 years")
        elif self.species == "Bird":
            print(f"{self.name} has a life span of 20-25 years")
        else:
            print(f"{self.name} is not a recognized species")

    def animal_years(self):
        if self.species == "Dog":
            print(f"{self.name} is {self.dog_years()} in dog years")
        elif self.species == "Cat":
            print(f"{self.name} is {self.cat_years()} in cat years")
        elif self.species == "Bird":
            print(f"{self.name} is {self.bird_years()} in bird years")
        else:
            print(f"{self.name} is not a recognized species")

    def dog_years(self):
        if self.age == 0:
            return 0
        elif self.age == 1:
            return 15
        elif self.age == 2:
            return 24
        else:
            return 24 + (self.age - 2) * 5

    def cat_years(self):
        if self.age == 0:
            return 0
        elif self.age == 1:
            return 15
        elif self.age == 2:
            return 24
        else:
            return 24 + (self.age - 2) * 4

    def bird_years(self):
        if self.age == 0:
            return 0
        elif self.age == 1:
            return 12
        elif self.age == 2:
            return 24
        else:
            return 24 + (self.age - 2) * 4


dog1 = Pet("Zipper", 2, "Dog")
dog1.life_span()
dog1.animal_years()

cat1 = Pet("Whiskers", 5, "Cat")
cat1.life_span()
cat1.animal_years()

bird1 = Pet("Tweety", 1, "Bird")
bird1.life_span()
bird1.animal_years()
