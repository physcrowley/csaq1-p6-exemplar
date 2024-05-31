
""" Extract and organize the game data """

NAME = 0
DESCRIPTION = 1
OPTIONS = 2
ITEMS = 3
ITEM_MSGS = 4

def load_game(file_path : str) -> tuple[list, list] :
    # read data into memory
    with open(file_path, "r") as file:
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
    
rooms, room_names = load_game("./data/game_data.txt")

