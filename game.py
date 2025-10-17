#!/usr/bin/python3

from map import rooms
from player import *
from items import *
from gameparser import *
MAX_INVENTORY_MASS = 3.0  # Maximum weight in kilograms



def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

    >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'

    >>> list_of_items([item_id])
    'id card'

    >>> list_of_items([])
    ''

    >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'

    """
    if len(items) == 0:
        return ""
    
    item_names = [item["name"] for item in items]
    return ", ".join(item_names)


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(rooms["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>

    >>> print_room_items(rooms["Admins"])

    (no output)

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    items_str = list_of_items(room["items"])
    if items_str:
        print("There is " + items_str + " here.")
        print()


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>

    """
    items_str = list_of_items(items)
    if items_str:
        print("You have " + items_str + ".")
        print()


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room(rooms["Admins"])
    <BLANKLINE>
    MJ AND SIMON'S ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Matt "MJ" John and Simon Jones. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()

    # Display items in the room
    print_room_items(room)

def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(rooms["Reception"]["exits"], "south")
    "MJ and Simon's room"
    >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "MJ and Simon's room")
    GO SOUTH to MJ and Simon's room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to MJ and Simon's room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    # Print take actions for room items
    for item in room_items:
        print("TAKE " + item["id"].upper() + " to take " + item["name"] + ".")
    
    # Print drop actions for inventory items
    for item in inv_items:
        print("DROP " + item["id"].upper() + " to drop " + item["name"] + ".")
    
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    
    if is_valid_exit(current_room["exits"], direction):
        current_room = move(current_room["exits"], direction)
    else:
        print("You cannot go there.")

def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that." If taking the item would exceed the weight limit,
    it prints "You cannot carry that."
    """
    global inventory
    
    # Find the item with the matching id in the current room
    item_to_take = None
    for item in current_room["items"]:
        if item["id"] == item_id:
            item_to_take = item
            break
    
    if item_to_take is None:
        print("You cannot take that.")
    elif not can_take_item(item_to_take):
        print("You cannot carry that.")
    else:
        # Move item from room to inventory
        current_room["items"].remove(item_to_take)
        inventory.append(item_to_take)

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    global inventory
    
    # Find the item with the matching id in the inventory
    item_to_drop = None
    for item in inventory:
        if item["id"] == item_id:
            item_to_drop = item
            break
    
    if item_to_drop is not None:
        # Move item from inventory to room
        inventory.remove(item_to_drop)
        current_room["items"].append(item_to_drop)
    else:
        print("You cannot drop that.")
        

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")

def get_inventory_mass(items):
    """This function takes a list of items and returns the total mass of all items
    in kilograms. For example:
    
    >>> get_inventory_mass([item_id, item_laptop])
    2.6
    
    >>> get_inventory_mass([])
    0
    """
    total_mass = 0
    for item in items:
        total_mass += item["mass"]
    return total_mass

def can_take_item(item):
    """This function checks if the player can take an item by verifying that
    adding it to the inventory would not exceed the weight limit. It returns
    True if the item can be taken, False otherwise.
    """
    current_mass = get_inventory_mass(inventory)
    if current_mass + item["mass"] <= MAX_INVENTORY_MASS:
        return True
    else:
        return False

def get_all_items():
    """This function returns a list of all items in the game by searching
    through all rooms and collecting unique items.
    """
    all_items = []
    item_ids_seen = set()
    
    # Collect items from all rooms
    for room in rooms.values():
        for item in room["items"]:
            if item["id"] not in item_ids_seen:
                all_items.append(item)
                item_ids_seen.add(item["id"])
    
    return all_items

def check_win_condition():
    """This function checks if the player has won the game. The victory condition
    is: the player must have collected all items in the game and be at the
    Reception room. Returns True if the player has won, False otherwise.
    """
    global current_room, inventory
    
    # Check if player is at Reception by checking the room name
    if current_room["name"] != "Reception":
        return False
    
    # Get all items in the game
    all_items = get_all_items()
    
    # Check if all items are in inventory
    inventory_item_ids = {item["id"] for item in inventory}
    all_item_ids = {item["id"] for item in all_items}
    
    return inventory_item_ids == all_item_ids

def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(rooms["Reception"]["exits"], "south") == rooms["Admins"]
    True
    >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
    >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """

    # Next room to go to
    return rooms[exits[direction]]


# This is the entry point of our program
def main():

    # Main game loop
    while True:
        # Check for win condition
        if check_win_condition():
            print()
            print("=" * 50)
            print("CONGRATULATIONS! YOU HAVE WON THE GAME!")
            print("You collected all items and returned to Reception.")
            print("=" * 50)
            break
        
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)
        
        # Display current inventory mass
        current_mass = get_inventory_mass(inventory)
        print(f"Inventory mass: {current_mass:.1f} kg / {MAX_INVENTORY_MASS} kg")
        print()

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()

