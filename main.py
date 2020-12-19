from player import Player
import map
import sys
from collections import OrderedDict


def play():
    """  Initialize the map and player data, and start the game"""
    print("""
    One night you wake up and find you are trapped in a square room,
    and anything you usually bring with you, disappeared. The only lighting
    in the room is a light bulb hanging from the ceiling, and an old wooden
    table and chairs are placed in the center of the room, a bowl of deep
    red soup was quietly placed on a table.
    """)
    q = input(">>Press enter to start the game. Enter 'Q' to exit the game.")
    # quit game
    if q in ['Q', 'q']:
        print('You opt out of the game!')
        sys.exit()
    map.parse_room_dsl()
    player = Player()
    # Possible player directions and actions continue as long as the player is
    # alive .
    while player.is_alive() and not player.victory:
        # define the player's start position
        position = map.room_at(player.x, player.y, player)
        # print(player.x, player.y)
        # print the intro at the start position
        print(position.intro_text())
        # modify health points of player when attacked
        position.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(position, player)


def get_available_actions(position, player):
    """Only make valid actions available. Actions are stored in a dictionary"""
    # store actions in a dictionary
    actions = OrderedDict()
    print("Choose an action: ")
    # print inventory option if there are any items
    if player.inventory:
        action_adder(actions, "i", player.print_inventory, "Print Inventory")
    # print use poison option
    if player.inventory and map.check_poison(position, player):
        action_adder(actions, "u", player.drink_poison, "User Poison")
    # print the room's map
    if isinstance(position, map.StartRoom):
        action_adder(actions, "m", position.print_map, "Room's Map")
    # read book
    if isinstance(position, map.Library) and position.inventory and \
            position.searched:
        action_adder(actions, "r", position.read_book, "Read Book")
    # if have enemies in the room , attack it
    if isinstance(position, map.SlaveRoom) and position.enemy.is_alive():
        action_adder(actions, "a", player.attack, "Attack")
    # option to move to another tile once all other actions are completed
    else:
        if map.room_at(position.x, position.y - 1, player):
            action_adder(actions, "w", player.move_forward, "Go forward")
        if map.room_at(position.x, position.y + 1, player):
            action_adder(actions, "s", player.move_aftward, "Go aftward")
        if map.room_at(position.x - 1, position.y, player):
            action_adder(actions, "a", player.move_left, "Go left side")
        if map.room_at(position.x + 1, position.y, player):
            action_adder(actions, "d", player.move_right, "Go right side")
        if (isinstance(position, map.Library) or
                isinstance(position, map.SlaveRoom) or
                isinstance(position, map.Kitchen)) and position.inventory:
            action_adder(actions, "c", player.collect_items, "Collect Items")
            action_adder(actions, "e", position.search_items, "Search Items")
    # healing option if the player has less than 100 HP
    if player.hp < 100:
        action_adder(actions, "h", player.heal, "Heal")

    return actions


def action_adder(action_dict, hotkey, action, name):
    """Add actions to the dictionary and prints the corresponding command"""
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))


def choose_action(position, player):
    """Ask the user to choose an action"""
    action = None
    while not action:
        available_actions = get_available_actions(position, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")


def move_player(actions, player, position):
    """Define player movement dependent on position"""
    if map.room_at(position.x, position.y - 1):
        return action_adder(actions, "f", player.move_forward, "Go forward")
    if map.room_at(position.x, position.y + 1):
        return action_adder(actions, "a", player.move_aftward, "Go aftward")
    if map.room_at(position.x - 1, position.y):
        return action_adder(actions, "p", player.move_port, "Go portside")
    if map.room_at(position.x + 1, position.y):
        return action_adder(actions, "s", player.move_starboard,
                            "Go starboard side")


play()
