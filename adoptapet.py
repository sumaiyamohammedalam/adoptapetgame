# adopt a pet game

# pet_game.py

class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.hunger = 50
        self.happiness = 50

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.happiness = min(100, self.happiness + 5)
        print(f"You fed {self.name}! Hunger: {self.hunger}, Happiness: {self.happiness}")

    def play(self):
        self.happiness = min(100, self.happiness + 10)
        self.hunger = min(100, self.hunger + 5)
        print(f"You played with {self.name}! Hunger: {self.hunger}, Happiness: {self.happiness}")

    def mood(self):
        if self.hunger > 70:
            return f"{self.name} is very hungry!"
        elif self.happiness < 40:
            return f"{self.name} is sad."
        else:
            return f"{self.name} is happy!"

    def __repr__(self):
        return f"<Pet {self.name} ({self.species}) | Hunger={self.hunger}, Happiness={self.happiness}>"

class Person:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def adopt(self, pet):
        self.pets.append(pet)
        print(f"{self.name} adopted {pet.name} the {pet.species}!")

    def show_pets(self):
        if not self.pets:
            print(f"{self.name} has no pets yet.")
        else:
            print(f"{self.name}'s pets:")
            for pet in self.pets:
                print(f" - {pet.name} ({pet.species}) | Hunger: {pet.hunger}, Happiness: {pet.happiness}")

def main():
    print("🐾 Welcome to Adopt-a-Pet Game! 🐾")
    player_name = input("What is your name? ")
    player = Person(player_name)

    while True:
        print("\n--- Main Menu ---")
        print("1. Adopt a pet")
        print("2. View your pets")
        print("3. Feed a pet")
        print("4. Play with a pet")
        print("5. Quit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            pet_name = input("Enter a name for your new pet: ")
            pet_species = input("What species is your pet? (dog, cat, rabbit, etc.): ")
            new_pet = Pet(pet_name, pet_species)
            player.adopt(new_pet)

        elif choice == "2":
            player.show_pets()

        elif choice == "3":
            if not player.pets:
                print("You don't have any pets yet!")
                continue
            pet_name = input("Which pet do you want to feed? ")
            found = False
            for pet in player.pets:
                if pet.name.lower() == pet_name.lower():
                    pet.feed()
                    print(pet.mood())
                    found = True
                    break
            if not found:
                print("Pet not found.")

        elif choice == "4":
            if not player.pets:
                print("You don't have any pets yet!")
                continue
            pet_name = input("Which pet do you want to play with? ")
            found = False
            for pet in player.pets:
                if pet.name.lower() == pet_name.lower():
                    pet.play()
                    print(pet.mood())
                    found = True
                    break
            if not found:
                print("Pet not found.")

        elif choice == "5":
            print("Thanks for playing! 🐶🐱🐰")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

# More updates in the future
