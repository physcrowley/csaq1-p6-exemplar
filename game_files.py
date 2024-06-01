"""
This module handles all file operations related to the game. This includes
loading the game data from a file and loading or saving user game data.

Exports these functions :
- load_game() -> tuple[list, list]: Returns a ragged list of rooms and a flat list of room names.
- show_saved_sessions(): Displays the list of saved user sessions.
- save_session(user: str, session_name: str, items: list[str], location: str) -> bool: Saves the user game data to a file.
- load_session(user: str, session_name: str) -> tuple[str, list[str]: Loads the user game data from a file.

Exports these constants:
- NAME: The index of the room name in the room data structure.
- DESCRIPTION: The index of the room description in the room data structure.
- OPTIONS: The index of the room options in the room data structure.
- ITEMS: The index of the room items in the room data structure.
- ITEM_MSGS: The index of the room item messages in the room data structure.
- USER: The index of the user name in the user log structure.
- USER_SESSION: The index of the user session name in the user log structure.
- TIMESTAMP: The index of the timestamp in the user log structure.

Exports these variables:
- users: A set of user names.
- user_log: A list of user log records.

These functions and variables are reserved for internal use:
- _add_user_file_to_log(user: str, session_name: str) -> None: Updates the log file and the in-memory collections.
- _load_user_log(): Loads the user log file into memory.
- _SAVE_DIR: The directory where user game files are saved.
- _USER_FILE_LOG: The path to the user log file.
- _GAME_FILE: The path to the main game file.
"""

import datetime
import os

# User game files
_SAVE_DIR = "./data/saved_games/"
_USER_FILE_LOG = os.path.join(_SAVE_DIR, "log.txt")

# Main game file
_GAME_FILE = "./data/game_data.txt"

# Game file sections
NAME = 0
DESCRIPTION = 1
OPTIONS = 2
ITEMS = 3
ITEM_MSGS = 4

# Log file tuple elements
USER = 0
USER_SESSION = 1
TIMESTAMP = 2

users = set() # this variable is a candidate for removal but I haven't tested the edge cases
user_log = []


def load_game() -> tuple[list, list]:
    """
    This functions extracts the structured game data from the game file and returns it as
    a ragged list of rooms and a flat list of room names.

    The room list elements may be a single value or a list of values. Their contents
    are described by the constants NAME, DESCRIPTION, OPTIONS, ITEMS, and ITEM_MSGS.
    """
    # read data into memory
    with open(_GAME_FILE, "r") as file:
        data = file.read()

    # split the data into rooms
    rooms = data.strip().split("###")

    # split each room into sections
    for i in range(len(rooms)):
        rooms[i] = rooms[i].strip().split("\n\n")

    room_names = [r[NAME] for r in rooms]

    for r in rooms:
        # split options section into a list of options
        r[OPTIONS] = r[OPTIONS].strip().split(", ")
        # split items section into a list of items
        r[ITEMS] = r[ITEMS].strip().split(", ")
        # split item_message section into a list of item_messages
        r[ITEM_MSGS] = r[ITEM_MSGS].strip().split(", ")

    return rooms, room_names


def _add_user_file_to_log(user: str, session_name: str) -> None:
    """update the log file and the in-memory collections"""

    now = str(datetime.datetime.now())
    user = user.lower()

    with open(_USER_FILE_LOG, "a") as file:
        file.write(f"{user};{session_name};{now}\n")

    user_log.append((user, session_name, now))

    users.add(user)


def _load_user_log() -> None:
    """Pulls data from the user log file into memory"""
    if len(user_log) > 0:  # already loaded
        return

    if not os.path.exists(_USER_FILE_LOG):  # no log file yet
        return

    with open(_USER_FILE_LOG, "r") as file:
        # build both user collections
        for line in file:
            user_log.append((line.strip().split(";")))
            users.add(user_log[-1][USER])


def show_saved_sessions() -> None:
    """Displays the list of saved user sessions"""
    if len(user_log) == 0:  # not loaded yet
        _load_user_log()

    for i, record in enumerate(user_log):
        user, session_name, timestamp = record
        print(f"{i+1} : {session_name} - by {user} at {timestamp}")


def save_session(user: str, session_name: str, items: list[str]) -> None:
    """Saves the user session data to a file"""

    # create the user file path
    user_file = os.path.join(_SAVE_DIR, f"{user.lower()}_{session_name}.txt")

    # write the user data to the file, overwriting any existing data
    with open(user_file, "w") as file:
        file.write(f"{','.join(items)}\n")

    # update the log file
    _add_user_file_to_log(user, session_name)


def load_session(user: str, session_name: str) -> tuple[str, list[str]]:
    """Loads the user session data from a file"""

    if len(user_log) == 0:  # not loaded yet
        _load_user_log()

    if user.lower() not in users:
        return None, None

    # create the user file path
    user_file = os.path.join(_SAVE_DIR, f"{user.lower()}_{session_name}.txt")

    # read the user data from the file
    with open(user_file, "r") as file:
        items = file.readline().strip().split(",")

    return items
