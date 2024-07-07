import random

class Object:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.description} (Value: {self.value} gold)"

class NPC:
    def __init__(self, name, description, disposition):
        self.name = name
        self.description = description
        self.disposition = disposition  # peaceful, neutral, aggressive

    def __str__(self):
        return f"{self.name} ({self.disposition}): {self.description}"

class Location:
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type  # peaceful, neutral, aggressive
        self.objects = []
        self.npcs = []
        self.connections = {}

    def add_object(self, obj):
        self.objects.append(obj)

    def add_npc(self, npc):
        self.npcs.append(npc)

    def connect(self, direction, location):
        self.connections[direction] = location

    def __str__(self):
        obj_descriptions = '\n'.join([str(obj) for obj in self.objects])
        npc_descriptions = '\n'.join([str(npc) for npc in self.npcs])
        return (f"{self.name} ({self.type})\n{self.description}\n\n"
                f"Objects here:\n{obj_descriptions}\n\nNPCs here:\n{npc_descriptions}\n")

class Player:
    def __init__(self):
        self.inventory = []
        self.gold = 50

    def add_to_inventory(self, obj):
        self.inventory.append(obj)

    def remove_from_inventory(self, obj_name):
        for obj in self.inventory:
            if obj.name == obj_name:
                self.inventory.remove(obj)
                return obj
        return None

    def show_inventory(self):
        if not self.inventory:
            return "Your inventory is empty."
        return "\n".join([str(obj) for obj in self.inventory])

class Game:
    def __init__(self):
        self.player = Player()
        self.create_world()
        self.current_location = self.start_location

    def create_world(self):
        # Create locations
        town = Location("Town", "A bustling town with traders and shops.", "peaceful")
        forest = Location("Forest", "A dark and mysterious forest.", "neutral")
        cave = Location("Cave", "A damp and dark cave. Beware of creatures!", "aggressive")
        lake = Location("Lake", "A serene lake with crystal clear water.", "peaceful")

        # Connect locations
        town.connect("north", forest)
        forest.connect("south", town)
        forest.connect("east", cave)
        cave.connect("west", forest)
        town.connect("west", lake)
        lake.connect("east", town)

        # Add objects to locations
        sword = Object("Sword", "A sharp sword with a gleaming blade.", 100)
        potion = Object("Potion", "A healing potion.", 25)
        gold_coin = Object("Gold Coin", "A shiny gold coin.", 1)

        town.add_object(gold_coin)
        forest.add_object(potion)
        cave.add_object(sword)

        # Add NPCs to locations
        merchant = NPC("Merchant", "A friendly merchant selling various goods.", "neutral")
        bandit = NPC("Bandit", "A dangerous bandit looking for trouble.", "aggressive")
        healer = NPC("Healer", "A kind healer offering to restore health.", "peaceful")

        town.add_npc(merchant)
        forest.add_npc(bandit)
        lake.add_npc(healer)

        self.start_location = town

    def move(self, direction):
        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            print(f"You move {direction} to the {self.current_location.name}.")
            self.road_encounter()
        else:
            print("You can't go that way.")

    def road_encounter(self):
        encounter_chance = random.randint(1, 100)
        if encounter_chance <= 20:
            self.encounter_enemy()
        elif encounter_chance <= 40:
            self.get_robbed()
        elif encounter_chance <= 60:
            self.find_gold()
        else:
            print("You travel without incident.")

    def encounter_enemy(self):
        print("You encounter an enemy on the road!")
        # Simple enemy encounter mechanics
        fight_or_flee = input("Do you want to fight (f) or flee (l)? ").strip().lower()
        if fight_or_flee == 'f':
            if random.choice([True, False]):
                print("You defeat the enemy and find some gold!")
                self.player.gold += 10
            else:
                print("The enemy defeats you. You lose some gold!")
                self.player.gold = max(0, self.player.gold - 10)
        else:
            print("You manage to flee without incident.")

    def get_robbed(self):
        if self.player.gold > 0:
            print("You get robbed on the road! You lose some gold.")
            self.player.gold = max(0, self.player.gold - 10)
        else:
            print("You get robbed on the road, but you have no gold to lose.")

    def find_gold(self):
        print("You find some gold on the road!")
        self.player.gold += 10

    def look(self):
        print(self.current_location)

    def show_inventory(self):
        print(self.player.show_inventory())

    def trade(self):
        print("You approach the merchant for trading.")
        if self.current_location.name != "Town":
            print("There is no merchant here.")
            return

        print("Items available for trade:")
        for obj in self.current_location.objects:
            print(f"{obj.name} - {obj.value} gold")

        action = input("Do you want to buy (b) or sell (s)? ").strip().lower()
        if action == 'b':
            item_name = input("Enter the name of the item you want to buy: ").strip()
            for obj in self.current_location.objects:
                if obj.name.lower() == item_name.lower():
                    if self.player.gold >= obj.value:
                        self.player.gold -= obj.value
                        self.player.add_to_inventory(obj)
                        self.current_location.objects.remove(obj)
                        print(f"You bought {obj.name}.")
                    else:
                        print("You don't have enough gold.")
                    return
            print("Item not found.")
        elif action == 's':
            item_name = input("Enter the name of the item you want to sell: ").strip()
            obj = self.player.remove_from_inventory(item_name)
            if obj:
                self.player.gold += obj.value
                print(f"You sold {obj.name}.")
            else:
                print("Item not found in your inventory.")
        else:
            print("Invalid action.")

    def play(self):
        print("Welcome to the Text Adventure RPG!")
        print("You can move by typing 'north', 'south', 'east', or 'west'.")
        print("Type 'look' to see your surroundings.")
        print("Type 'inventory' to see your inventory.")
        print("Type 'trade' to trade with the merchant.")
        print("Type 'exit' to quit the game.")
        print()

        while True:
            command = input("> ").strip().lower()

            if command in ["north", "south", "east", "west"]:
                self.move(command)
            elif command == "look":
                self.look()
            elif command == "inventory":
                self.show_inventory()
            elif command == "trade":
                self.trade()
            elif command == "exit":
                print("Thank you for playing!")
                break
            else:
                print("Invalid command.")

if __name__ == "__main__":
    game = Game()
    game.play()