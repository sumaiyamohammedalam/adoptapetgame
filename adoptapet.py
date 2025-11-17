# adopt a pet game - enhanced version
# Enhancements:
# - Persistent save/load to JSON (savefile.json)
# - Additional pet stats: health, energy, age
# - New actions: sleep, heal (vet), rename, release
# - Auto time tick each main loop iteration (hunger/energy/health changes)
# - Better mood/status reporting
# - Commands to act on all pets
# - Autosave on quit (optional)
import json
import os
import time
from datetime import datetime

SAVEFILE = "savefile.json"

class Pet:
    def __init__(self, name, species, hunger=50, happiness=50, health=100, energy=70, age_days=0):
        self.name = name
        self.species = species
        self.hunger = hunger          # 0 = full, 100 = starving
        self.happiness = happiness    # 0-100
        self.health = health          # 0-100
        self.energy = energy          # 0-100
        self.age_days = age_days      # age in days

    def feed(self, amount=15):
        prev_hunger = self.hunger
        self.hunger = max(0, self.hunger - amount)
        self.happiness = min(100, self.happiness + int(amount / 3))
        print(f"You fed {self.name}! Hunger: {prev_hunger} -> {self.hunger}, Happiness: {self.happiness}")

    def play(self, duration=10):
        if self.energy < 15:
            print(f"{self.name} is too tired to play. Try sleeping first.")
            return
        prev_happy = self.happiness
        prev_energy = self.energy
        self.happiness = min(100, self.happiness + int(duration / 1.5))
        self.hunger = min(100, self.hunger + int(duration / 2))
        self.energy = max(0, self.energy - int(duration / 2))
        print(f"You played with {self.name}! Happiness: {prev_happy} -> {self.happiness}, Energy: {prev_energy} -> {self.energy}")

    def sleep(self, hours=3):
        prev_energy = self.energy
        self.energy = min(100, self.energy + hours * 10)
        self.hunger = min(100, self.hunger + hours * 2)
        print(f"{self.name} slept for {hours} hours. Energy: {prev_energy} -> {self.energy}")

    def heal(self, amount=20):
        prev_health = self.health
        self.health = min(100, self.health + amount)
        self.happiness = min(100, self.happiness + 5)
        print(f"You took {self.name} to the vet. Health: {prev_health} -> {self.health}")

    def age_one_day(self):
        self.age_days += 1

    def mood(self):
        states = []
        if self.hunger > 80:
            states.append("very hungry")
        elif self.hunger > 50:
            states.append("hungry")

        if self.happiness < 30:
            states.append("sad")
        elif self.happiness > 80:
            states.append("very happy")

        if self.energy < 20:
            states.append("exhausted")

        if self.health < 40:
            states.append("sick")

        if not states:
            return f"{self.name} seems content."
        else:
            return f"{self.name} is " + ", ".join(states) + "."

    def status(self):
        return (f"{self.name} ({self.species}) | Age: {self.age_days}d | Hunger: {self.hunger} | "
                f"Happiness: {self.happiness} | Energy: {self.energy} | Health: {self.health}")

    def tick(self, days=0, time_units=1):
        # Simulate passage of time: time_units is a rough multiplier per loop iteration
        self.hunger = min(100, self.hunger + 3 * time_units)
        self.happiness = max(0, self.happiness - 2 * time_units)
        self.energy = max(0, self.energy - 3 * time_units)
        # Health degrades if very hungry or exhausted
        if self.hunger > 90 or self.energy < 10:
            self.health = max(0, self.health - 2 * time_units)
        # Age increment occasionally
        if days:
            for _ in range(days):
                self.age_one_day()

    def rename(self, new_name):
        old = self.name
        self.name = new_name
        print(f"{old} has been renamed to {self.name}.")

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "health": self.health,
            "energy": self.energy,
            "age_days": self.age_days
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d.get("name"),
            species=d.get("species"),
            hunger=d.get("hunger", 50),
            happiness=d.get("happiness", 50),
            health=d.get("health", 100),
            energy=d.get("energy", 70),
            age_days=d.get("age_days", 0)
        )

    def __repr__(self):
        return f"<Pet {self.name} ({self.species}) | Hunger={self.hunger}, Happiness={self.happiness}, Health={self.health}, Energy={self.energy}>"

class Person:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def adopt(self, pet):
        self.pets.append(pet)
        print(f"{self.name} adopted {pet.name} the {pet.species}!")

    def release(self, pet_name):
        for i, pet in enumerate(self.pets):
            if pet.name.lower() == pet_name.lower():
                removed = self.pets.pop(i)
                print(f"{self.name} released {removed.name}.")
                return True
        print("Pet not found.")
        return False

    def show_pets(self):
        if not self.pets:
            print(f"{self.name} has no pets yet.")
        else:
            print(f"{self.name}'s pets:")
            for pet in self.pets:
                print(f" - {pet.status()}")

    def save(self, filename=SAVEFILE):
        data = {
            "owner": self.name,
            "saved_at": datetime.utcnow().isoformat() + "Z",
            "pets": [p.to_dict() for p in self.pets]
        }
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Game saved to {filename}.")
        except Exception as e:
            print(f"Failed to save: {e}")

    @classmethod
    def load(cls, filename=SAVEFILE):
        if not os.path.exists(filename):
            print("No save file found.")
            return None
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            owner = data.get("owner", "Player")
            p = cls(owner)
            for d in data.get("pets", []):
                p.pets.append(Pet.from_dict(d))
            print(f"Loaded game for {owner} from {filename}.")
            return p
        except Exception as e:
            print(f"Failed to load save file: {e}")
            return None

def find_pet_by_name(person, pet_name):
    for pet in person.pets:
        if pet.name.lower() == pet_name.lower():
            return pet
    return None

def print_main_menu():
    print("\n---~~Main Menu~~---")
    print("1. Adopt a pet")
    print("2. View your pets")
    print("3. Feed a pet (or all)")
    print("4. Play with a pet (or all)")
    print("5. Put a pet to sleep")
    print("6. Take a pet to the vet (heal)")
    print("7. Rename a pet")
    print("8. Release a pet")
    print("9. Save game")
    print("10. Load game")
    print("11. Quit game")

def ask_pet_choice(player, prompt="Which pet? (name or 'all'): "):
    if not player.pets:
        print("You don't have any pets yet!")
        return None, None
    pet_name = input(prompt).strip()
    if pet_name.lower() == "all":
        return "all", player.pets
    pet = find_pet_by_name(player, pet_name)
    if not pet:
        print("Pet not found.")
        return None, None
    return pet, [pet]

def main():
    print("🐾 Welcome to Adopt-a-Pet Game! 🐾")
    player_name = input("What is your name? ").strip() or "Player"
    # offer to load existing save
    if os.path.exists(SAVEFILE):
        use_save = input("Found a saved game. Load it? (y/n): ").strip().lower()
        if use_save == "y":
            loaded = Person.load(SAVEFILE)
            if loaded:
                player = loaded
            else:
                player = Person(player_name)
        else:
            player = Person(player_name)
    else:
        player = Person(player_name)

    autosave = True

    loop_count = 0
    while True:
        # each loop simulates a time tick for pets
        loop_count += 1
        for pet in player.pets:
            pet.tick(time_units=1)
            # every 24 loops, age by 1 day (very rough simulation)
            if loop_count % 24 == 0:
                pet.age_one_day()

        print_main_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            pet_name = input("Enter a name for your new pet: ").strip()
            if not pet_name:
                print("Pet must have a name.")
                continue
            pet_species = input("What species is your pet? (dog, cat, rabbit, etc.): ").strip() or "pet"
            new_pet = Pet(pet_name, pet_species)
            player.adopt(new_pet)

        elif choice == "2":
            player.show_pets()

        elif choice == "3":
            pet_or_all, pets = ask_pet_choice(player, "Which pet do you want to feed? (name or 'all'): ")
            if pet_or_all is None:
                continue
            if pet_or_all == "all":
                for p in pets:
                    p.feed()
                    print(p.mood())
            else:
                pets[0].feed()
                print(pets[0].mood())

        elif choice == "4":
            pet_or_all, pets = ask_pet_choice(player, "Which pet do you want to play with? (name or 'all'): ")
            if pet_or_all is None:
                continue
            if pet_or_all == "all":
                for p in pets:
                    p.play()
                    print(p.mood())
            else:
                pets[0].play()
                print(pets[0].mood())

        elif choice == "5":
            pet_or_all, pets = ask_pet_choice(player, "Which pet do you want to put to sleep? (name or 'all'): ")
            if pet_or_all is None:
                continue
            hours = input("How many hours should they sleep? (default 3): ").strip()
            try:
                hours = int(hours) if hours else 3
            except ValueError:
                hours = 3
            if pet_or_all == "all":
                for p in pets:
                    p.sleep(hours=hours)
            else:
                pets[0].sleep(hours=hours)

        elif choice == "6":
            pet_or_all, pets = ask_pet_choice(player, "Which pet to take to the vet? (name or 'all'): ")
            if pet_or_all is None:
                continue
            if pet_or_all == "all":
                for p in pets:
                    p.heal()
            else:
                pets[0].heal()

        elif choice == "7":
            pet, pets = ask_pet_choice(player, "Which pet do you want to rename? (name): ")
            if pet is None or pet == "all":
                continue
            new_name = input(f"What should {pet.name}'s new name be? ").strip()
            if new_name:
                pet.rename(new_name)

        elif choice == "8":
            pet_name = input("Which pet do you want to release? ").strip()
            if pet_name:
                player.release(pet_name)

        elif choice == "9":
            player.save()

        elif choice == "10":
            loaded = Person.load()
            if loaded:
                player = loaded

        elif choice == "11":
            if autosave:
                player.save()
            print("Thanks for playing! 🐶🐱🐰")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

# More updates and features to be added:
# - Inventory and item system (buy food, toys)
# - Random events (lost toy, found treat)
# - Multiple players / multiplayer save slots
# - GUI using tkinter or a web UI
