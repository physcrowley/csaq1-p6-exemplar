"""
Name: Exemplar by David Crowley
Date: 2024-05-31
File: main.py
Description:
This is a text-based adventure game where the player moves around a map
and collects items. It uses file input and output for the game data and
for saving and loading game sessions.

The file IO logic is in the game_files module.

This game also applies decomposition by breaking down the game logic into
smaller, more coherent functions.

The game script is at the bottom of the file.

KNOWN ISSUES:
- The game could probably use a univeral exit command. It wasn't in the plan, but it would be a nice feature.

"""

# Import data manipulation logic and data from game_files module
from game_files import load_game
from game_files import NAME, ITEMS, ITEM_MSGS
from game_files import load_session, save_session, show_saved_sessions
from game_files import user_log

rooms, room_names = load_game()

room = rooms[0]
current_move = room_names[0]
collected_items = []


def fresh_game() -> tuple[str, list[str], list]:
    """Returns starting current_move, collected_items, and room values."""
    return room_names[0], [], rooms[0]


def get_valid_option(options: list[str]) -> str:
    """
    Utility function that always returns a valid item from a list of options
    given a user input matching at least the first 3 characters of an option.

    If the options have less than three characters, the length of the shortest
    option is used as the minimum length for the user input.
    """
    least_chars = min(len(o) for o in options)
    while True:
        choice = input("> ")
        if len(choice) < min(3, least_chars):
            continue
        for o in options:
            if o.lower().startswith(choice[:3].lower()):
                return o


def end() -> None:
    print("You have ended the game. Would you like to save your session?")
    print("  [Yes]  [No]")
    save = get_valid_option(["Yes", "No"])

    if save == "No":
        return

    print("Enter your name:")
    user_name = input("> ")
    print("Enter a name for this session:")
    session_name = input("> ")
    save_session(user_name, session_name, collected_items)


def welcome() -> None:
    """
    Get's the users choice for a game and returns an empty set of users if they
    start a new game, the saved set of users if they load a game or None if they exit.
    """
    global collected_items

    options = ["Start a new game", "Load a saved game", "Exit"]
    START, LOAD, _ = options

    print("Welcome to the game!")
    print("You are about to be teleported into the game world.\n")
    print("Here are your options. Type at least 3 characters to select an option.")
    for o in options:
        print(f"  [{o}]", end="")
    print()
    choice = get_valid_option(options)

    if choice == START:
        print("Let's start a new game!")

    elif choice == LOAD:
        print("Here are the saved sessions:")
        show_saved_sessions()
        print()
        print("Enter the number of the session you wish to load.")
        id = get_valid_option([str(i) for i in range(1, len(user_log) + 1)])
        user, session, _ = user_log[int(id) - 1]
        collected_items = load_session(user, session)
        print(user, ", you are now equipped with the following items:")
        print(collected_items)


    else:  # choice == EXIT
        exit()


def play() -> None:
    """Main game loop"""

    global current_move, collected_items, room

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
        name, description, options, items, _ = room

        # show room information
        print("\n\n" + name)
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
        current_move = get_valid_option(options + available_items)


#
# GAME SCRIPT
#

while True:
    welcome()  # program exit condition is here
    play()
    end()
    current_move, collected_items, room = fresh_game()
