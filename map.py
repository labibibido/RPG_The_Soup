import enemies
import sys
import items


class Map:
    """ Map with x and y coordinates"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.searched = False
        self.inventory = []

    def __str__(self):
        return self.inventory

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        """Added modify_player to every tile"""
        pass

    def search_items(self):
        """ Collect items and add  to inventory """
        if len(self.inventory):
            for i, item in enumerate(self.inventory, 1):
                if i == 1:
                    print("You find the following items ! ")
                print("{}. {}.".format(i, item.name))
            self.searched = True
        else:
            print('No itmes in the room.')

    def add_inventory(self, current_inventory):
        """Add items from the supply tile to the player's inventory"""
        if self.searched:
            for item in self.inventory:
                current_inventory.append(item)
            # remove supplies from the tile
            self.inventory = []
        else:
            print("You haven't searched this room")


class StartRoom(Map):
    """Player starting position"""
    def intro_text(self):
        """Descriptive text for the Start Tile"""
        return """
        Then there was a map of the place and a warning text "drink the
        poisoned soup" on the chair next to it.
        """

    def print_map(self):
        """Print a map of the room with directions"""
        self.room_map = """
              -----------------
            |    The kitchen    |
---------------          ------------------------
|              |                      |                         |
| Library  \ Soup Room \  Slave's Room |
|              |                      |                         |
--------------- xxxxx ------------------------
            |    Auditorium    |
              -------------------
        """
        print(self.room_map)

    def modify_player(self, player):
        """Player wins the game if they reach the escape pod"""
        for i in player.inventory:
            if isinstance(i, items.Book):
                player.hp = -100
                print("""
----------------------------- You Died ------------------------------------
You can't take this book !
The door of this room will repeatedly open and close, and then
suddenly begin to melt. Then it melted into black liquid creatures
with no shape and killed you.
-----------------------------------------------------------------------------
                """)
        if player.drink == 1:
            print("""
-----------------------------------------------------------------------------
You drank the poisonous soup together and escaped from this place.
-----------------------------------------------------------------------------
            """)
            player.victory = True
            sys.exit()
        elif player.drink == 0:
            print("""
-----------------------------------------------------------------------------
You drank the poisonous soup alone and escaped from this place.
-----------------------------------------------------------------------------
                        """)
            player.victory = True
            sys.exit()
        elif player.drink == -1:
            print("""
----------------------------- You Died ------------------------------------
You drank the poison !
---------------------------------------------------------------------------
                        """)
            player.hp = -1


class Kitchen(Map):
    """The Kitchen"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.inventory = [items.Soup(), items.KeyToLibrary()]

    def intro_text(self):
        return """
        There are a lot of seasonings and utensils,
        some prepared "soup" in the pot.
        """


class Auditorium(Map):
    """The auditorium"""
    def __init__(self, x, y):
        """Creates a random position for each enemy"""
        # Indices j, k for switching alive_text and dead_text messages
        super().__init__(x, y)
        self.j = 0
        self.k = 0

        self.enemy = enemies.Monster()
        alive_start = """
        Where Chaugnar Faugn is. Do not wake him up unless you have "food"
        for him! He will ate the first person who got into the room.
        """
        alive_attack = "You angered the monster."
        self.alive_text = [alive_start, alive_attack]
        dead_start = """
        The monster is satisfied.
        """
        dead_return = "It decided to let you go !"
        self.dead_text = [dead_start, dead_return]

    def intro_text(self):
        """Intro message dependent on enemy health points"""
        if self.enemy.is_alive():
            # Switch from the intro message after the player starts attacking
            if self.j == 0:
                self.j += 1
                return self.alive_text[0]
            else:
                return self.alive_text[1]
        # switch from the intro message if the player returns to the tile
        # where there is a dead enemy
        else:
            if self.k == 0:
                self.k += 1
                return self.dead_text[0]
            else:
                return self.dead_text[1]

    def modify_player(self, player):
        """
        Checks the enemy's current strength so it can respond to the player
        """
        if self.enemy.is_alive():
            # continue play if there's enough health points
            if player.hp > self.enemy.damage:
                player.hp -= self.enemy.damage
                print("The {} does {} damage. You have {} HP remaining".
                      format(self.enemy.name,
                             self.enemy.damage,
                             player.hp))
            # end the game if the player runs out of health points
            elif player.hp <= self.enemy.damage:
                print("""
----------------------------- You Died ------------------------------------
The {} causes mortal damage. You die.
---------------------------------------------------------------------------
                """.
                      format(self.enemy.name))
                sys.exit()


class Library(Map):
    """The library"""
    def __init__(self, x, y):
        """Initial supplies at the tile"""
        # index for switching descriptive messagages
        super().__init__(x, y)
        self.inventory = [items.Book()]

    def intro_text(self):
        return """
        The door of the west room is a wooden door with ornate decoration,
        you opened this door with a key. In the center of this room is a small
        old four-legged table with candles on a candlestick illuminating the
        room with faint light. The four sides of the room were filled with a
        large number of bookcases.
        """

    def read_book(self):
        if self.inventory:
            print(self.inventory[0])


class SlaveRoom(Map):
    """The Slave's room"""
    def __init__(self, x, y):
        """Creates a random position for each enemy"""
        super().__init__(x, y)
        # Indices j, k for switching alive_text and dead_text messages
        self.j = 0
        self.k = 0

        self.enemy = enemies.Keeper()
        alive_start = """
        There is a keeper here ! There is a girl in the prison behind him.
        The young girl (about 16 to 17)  with a white dress full of blood.
        """
        alive_attack = "You angered the keeper."
        self.alive_text = [alive_start, alive_attack]
        dead_start = """
        The keeper fell.
        """
        dead_return = "You rescued that girl."
        self.dead_text = [dead_start, dead_return]
        self.inventory = [items.Poison(), items.KeyToAuditorium()]

    def intro_text(self):
        """Intro message dependent on enemy health points"""
        if self.enemy.is_alive():
            # Switch from the intro message after the player starts attacking
            if self.j == 0:
                self.j += 1
                return self.alive_text[0]
            else:
                return self.alive_text[1]
        # switch from the intro message if the player returns to the tile
        # where there is a dead enemy
        else:
            if self.k == 0:
                self.k += 1
                return self.dead_text[0]
            else:
                return self.dead_text[1]

    def modify_player(self, player):
        """
        Checks the enemy's current strength so it can respond to the player
        """
        if self.enemy.is_alive():
            # continue play if there's enough health points
            if player.hp > self.enemy.damage:
                player.hp -= self.enemy.damage
                print("The {} does {} damage. You have {} HP remaining".
                      format(self.enemy.name, self.enemy.damage, player.hp))
            # end the game if the player runs out of health points
            elif player.hp <= self.enemy.damage:
                print("""
----------------------------- You Died ------------------------------------
The {} causes mortal damage. You die.
---------------------------------------------------------------------------
                                """.
                      format(self.enemy.name))
                sys.exit()
        elif len(player.partner) == 0 and self.enemy.is_alive() is False:
            player.partner = [enemies.YoungGirl]

# room_map = [
#     [NoRoom(0, 0), SuppliesTile(1, 0), NoRoom(2, 0)],
#     [Library(0, 1), StartRoom(1, 1), SlaveRoom(2, 1)],
#     [NoRoom(0, 2), Auditorium(1, 2), NoRoom(2, 2)]
# ]

room_map = []


# check you has keys
def check_key(room_name, player):
    need_key = ''
    if isinstance(room_name, Library):
        need_key = items.KeyToLibrary().name
    elif isinstance(room_name, Auditorium):
        need_key = items.KeyToAuditorium().name
    if len(need_key) and need_key not in [i.name for i in player.inventory]:
        return False
    return True


# check you has keys
def check_poison(room_name, player):
    need_items = []
    for i in player.inventory:
        if isinstance(i, items.Soup):
            need_items.append(i.name)
        if isinstance(i, items.Poison):
            need_items.append(i.name)
    if isinstance(room_name, StartRoom) and need_items:
        return True
    return False


#  will go to the room of  you choose
def room_at(x, y, player):
    """Locates the tile at a coordinate"""
    if x < 0 or y < 0:
        return None
    try:
        room_name = room_map[y][x]
        if check_key(room_name, player) is False:
            return ''
        return room_name

    except IndexError:
        return None


# rom's map
room_dsl = """
|NO|K|NO|
|L|SR|S|
|NO|A|NO|
"""


def is_dsl_valid(dsl):
    """
    Check to make sure there is only one start tile and escape pod.
    Also check that each row has the same number of columns
    """
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True


# key to the room's map
tile_type_dict = {"K": Kitchen,
                  "L": Library,
                  "S": SlaveRoom,
                  "SR": StartRoom,
                  "A": Auditorium,
                  "NO": None}
# initialize the start tile
start_tile_location = None


# initialize the room's map
def parse_room_dsl():
    """Taking the room's map as a string and returning a list"""
    if not is_dsl_valid(room_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = room_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]
    # Iterate over each line in the DSL.
    for y, dsl_row in enumerate(dsl_lines):
        # Create an object to store the tiles
        row = []
        # Split the line into abbreviations
        dsl_cells = dsl_row.split("|")
        # The split method includes the beginning
        # and end of the line so we need to remove
        # those nonexistent cells
        dsl_cells = [c for c in dsl_cells if c]
        # Iterate over each cell in the DSL line
        for x, dsl_cells in enumerate(dsl_cells):
            # Look up the abbreviation in the dictionary
            tile_type = tile_type_dict[dsl_cells]
            # set the start tile location
            if tile_type == StartRoom:
                global start_tile_location
                start_tile_location = x, y
            # If the dictionary returned a valid type, create
            # a new tile object, pass it the X-Y coordinates
            # as required by the tile __init__(), and add
            # it to the row object. If None was found in the
            # dictionary, we just add None.
            row.append(tile_type(x, y) if tile_type else None)
        # Add the whole row to the room_map
        room_map.append(row)

# parse_room_dsl()
