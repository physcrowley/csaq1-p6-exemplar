# File: game.py

"""
Added items and an associated item-message list to each room

Updated the file reading and game logic accordingly
"""

""" Extract and organize the game data """

from game_files import NAME, ITEMS, ITEM_MSGS, rooms, room_names


""" Game logic """

# welcome message
print("Welcome to the game!")
print("You are about to be teleported into the game world.")
print("Here are your options:")
print("  [exit] or [enter]\n")
choice = ""
while choice not in ["exit", "enter"]:
    choice = input("> ").lower()

if choice == "exit":
    print("Goodbye!")
    exit()

# game loop
room = rooms[0]
current_move = room_names[0]
collected_items = []
current_item = None


while room[NAME] != "Computer" or current_move == "power button":
    # the current exit condition is in the Computer room... but the power
    # button item shows a special message before triggering the exit

    # interpret the current move as navigation or item selection
    if current_move in room_names:
        room_id = room_names.index(current_move)
        room = rooms[room_id]
        show_description = True
    else:
        item_id = room[ITEMS].index(current_move)
        item_name = room[ITEMS][item_id]
        item_msg = room[ITEM_MSGS][item_id]
        # show item message
        print("\n| ", item_msg)
        # special exit condition
        if item_name == "power button":
            print("Shutting down... ", end="")
            break
        # update collection and show results
        collected_items.append(item_name)
        print("|  You have added", item_name, "to your collection.")
        print("|  Inventory: ", collected_items)
        # skip the room description
        show_description = False

    # extract room data
    name, description, options, items, item_msgs = room

    # show room information
    print("\n" + name)
    if show_description:
        print(description)
    # show navigation options
    print("\nYou can go here: ", end="")
    for o in options:
        print(f"  [{o}]  ", end="")
    # show items available to pick up
    print("\nOr you can pick up one of these items : ", end="")
    available_items = [i for i in items if i not in collected_items]
    for i in available_items:
        print(f"  [{i}]  ", end="")
    if len(available_items) == 0:
        print("(nothing here)", end="")
    print("\n")
    # get the next valid move
    print("Enter your move (at least 3 characters)")
    valid_move = False
    while not valid_move:
        current_move = input("> ")
        if len(current_move) < 3:
            continue
        for e in options + available_items:
            if e.lower().startswith(current_move.lower()):
                current_move = e
                valid_move = True
                break

print("Goodbye!")
