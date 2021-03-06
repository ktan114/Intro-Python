from os import system

from room import Room
from player import Player
from item import Item, Treasure, LightSource

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", True),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", False),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", True),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", False),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. But after some searching you find a key... """, False),

    'secret': Room("Secret Room", """With all of your knowledge and sheer fortitude
you have found a way into this room and found the treasure. And go east to exit this ride\n\nDon't forget to claim your prize!""", False)
}

# Create Items Dictionary

Items = {
    "Sword" : Item('Sword', 'Shiny'),
    "BronzeCoin" : Treasure('BronzeCoin', 'Bronze', '5'),
    "SilverCoin" : Treasure('SilverCoin', 'Silver', '10'),
    "GoldCoin" : Treasure('GoldCoin', 'Gold', '20'),
    "Lamp" : LightSource('Lamp', 'Illuminator'),
    "Key" : Item('Key', 'Secret Hidden Key'),
    "Pebble" : Item('Pebble', 'Yep, Just A Pebble')
}

# Adding Items to a Room

room['outside'].addItem(Items['Sword'])
room['foyer'].addItem(Items['BronzeCoin'])
room['narrow'].addItem(Items['SilverCoin'])
room['overlook'].addItem(Items['GoldCoin'])
room['outside'].addItem(Items['Lamp'])
room['treasure'].addItem(Items['Key'])
room['secret'].addItem(Items['Pebble'])

# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']
room['treasure'].e_to = room['secret']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

system("clear")
name = input("Enter your name:\n")
player = Player(name, room['outside'])

# Game Features:
    # 1. Display current room, room description, room items

    # 2. Takes an input as an instruction

    # 3. Travels through rooms using cardinal directions (North, East, South, West)

    # 4. Quits the game (Quit)

    # 5. Take items from the room or drop items from the inventory (Take Item(Name) | Drop Item(Name))
        # Also increase/decrease player's score dynamically

    # 6. Checks the inventory (Inventory)

    # 7. Display end game message

    # 8. Checks the score (Score)

    # 9. Added light scenarios and light sources 

    # 10. A win scenario

system("clear")
while (player.room != 'exit'):

    key_checker = [item for item in player.inventory if item.name == "Key"]

    if (player.room.name == "Secret Room" and len(key_checker) == 0):
        player.room = room['treasure']
        print("Sorry, you don't have the key to the secret room!\n")

    # - Added light scenarios and light sources
    natural_room = [room[x] for x in ['outside', 'foyer', 'overlook', 'narrow', 'treasure'] if room[x].is_Light]
    illuminated_room = [room[x] for x in ['outside', 'foyer', 'overlook', 'narrow', 'treasure']
        if [item for item in room[x].items if type(item) is LightSource] 
    ]

    illuminated = False

    if (player.room in natural_room or player.room in illuminated_room or [item for item in player.inventory if type(item) is LightSource]): 
        illuminated = True

    if (illuminated):

    # - Display current room, room description, room items

        print(player.name + " is at the\n" + player.room.name + ": " + player.room.description + "\n")
        print("The item(s) in the " + player.room.name + ": " + str(player.room.items) + "\n")
    else:
        print("It's pitch black! Go to a different room or find a light source. \n")

    # - Takes an input as an instruction

    instruction = input("Enter: North | East | South | West | Take Item(Name) | Drop Item(Name) | Inventory | Score | Quit:\n")

    # - Travels through rooms using cardinal directions (North, East, South, West)
    
    direction = {
        "North": player.room.n_to,
        "East": player.room.e_to,
        "South": player.room.s_to,
        "West": player.room.w_to
    }

    new_room = direction.get(instruction, None)
    

    # Single Word Commands

    system("clear")

    if (len(instruction.split()) == 1):

    # - Quits the game (Quit)

        if (instruction == "Quit" or instruction == "East" and player.room.name == "Secret Room"):
            break
        elif (new_room):
            player.room = new_room

    # - Checks the inventory (Inventory)

        elif (instruction == "Inventory"):
            print("In your inventory:", player.inventory)
            print("")
    
    # - Checks the score (Score)

        elif (instruction == "Score"):
            print(player.name + "'s Current Score: " + str(player.score) + "\n")
        elif (instruction in ["North", "East", "South", "West"]):
            print("Nowhere to go\n")
        else:
            print("Invalid Command. Enter: North | East | South | West | Take Item(Name) | Drop Item(Name) | Inventory | Score | Quit:\n")

    # Two Word Commands
    
    # - Take items from the room or drop items from the inventory (Take Item(Name) | Drop Item(Name))
    # - Add score accordingly

    elif (len(instruction.split()) == 2):
        verb, target = [x for x in instruction.split()]
        if (verb == "Take"):
            if (illuminated):
                if (player.room.searchItems(target)):
                    player.toInventory(Items[target])
                    print("You took the " + target + '\n')
                    if (type(Items[target]) is Treasure and Items[target].dropped == False):
                        player.score += int(Items[target].on_take())
                        Items[target].dropped = True
                        print('Your score increases by: ' + str(Items[target].value) + '\n')
                        print('Your score is now: ' + str(player.score) + '\n')
                    player.room.removeItem(target)
                else: 
                    print(target + " is not available\n")
            else:
                print("Good luck finding that in the dark!\n")  
        elif (verb == "Drop"):
            if (player.searchInventory(target)):
                if (target == "Lamp"):
                    print("It's not wise to drop your source of light!\n")
                player.removeItem(target)
                print("You dropped the " + target + "\n")
                if (type(Items[target]) is Treasure):
                    player.score -= int(Items[target].on_drop())
                    print('Your score decreases by: ' + str(Items[target].value) + '\n')
                    print('Your score is now: ' + str(player.score) + '\n')
                player.room.addItem(Items[target])
            else:
                print(target + " is not in your inventory\n")
    else:
        print("Invalid Command. Enter: North | East | South | West | Take Item(Name) | Drop Item(Name) | Inventory | Score | Quit:\n")

# - Display end game message

system("clear")
if (instruction == "Quit"):
    print("You quit and gained nothing\n")
else:
    if (len(player.inventory) == 0):
        print("You left the cave empty handed!\n")
    elif ([item for item in player.inventory if item.name == "Key"]):
        print("You have won the game!\n")
        if ([item for item in player.inventory if item.name == "Pebble"]):
            print("And you were also able to get the marvelous Pebble!\n")
            print("What's that? Your pebble is dirty...\n")
            counter = 0
            while (counter < 3):
                surprise = input("Enter \"Clean\" to clean your pebble:\n\n")
                if (surprise == "Clean"):
                    # system('clear')
                    counter += 1
                    if (counter == 1):
                        print('\nStill a little dirty\n')
                    elif (counter == 2):
                        print('\nTry once more\n')
                    else:
                        print('\nYou\'ve wiped off the dust to reveal that your marvelous Pebble is actually an\n\nInfinity Pebble!\n')
                        print('******* You can now do anything you want *******\n')
                        player.inventory.pop()
                        player.inventory.append(Item("Infinity Pebble", "You can now do anything you want"))
    if (player.score == 0):
        print("You managed to leave the cave with: " + str(player.inventory) + "\n")
    else:
        print("You managed to leave the cave with: " + str(player.inventory) + " and your score is: " + str(player.score) + "\n")