import items
import map


class Player:
    """Player class with inventory and best weapon"""

    def __init__(self):
        # begining items in inventory
        self.inventory = []
        # begining items in weapon
        self.weapon = [items.Bullet(), items.Guns()]
        # player starting soup room
        self.x = map.start_tile_location[0]
        self.y = map.start_tile_location[1]
        self.hp = 100
        self.victory = False
        # 100  No drink ; -1 drink poison ; 0, 1 drink soup and poison
        self.drink = 100
        self.partner = []

    def is_alive(self):
        """The player is alive if they have at least 1 HP"""
        return self.hp > 0

    def print_inventory(self):
        """Print the inventory of items and the best weapon"""
        print("#### #### ####")
        print("Inventory:")
        for item in self.inventory:
            print("* " + str(item))
        print("#### #### ####")
        # best_weapon = self.most_powerful_weapon()
        # print("Your best weapon is your {}".format(best_weapon))

    def move(self, dx, dy):
        """Define player movement"""
        self.old_x = self.x
        self.old_y = self.y
        self.x += dx
        self.y += dy

    def move_forward(self):
        """Define forward movement"""
        self.move(dx=0, dy=-1)

    def move_aftward(self):
        """Define aftward movement"""
        self.move(dx=0, dy=1)

    def move_right(self):
        """Define movement towards the starboard side"""
        self.move(dx=1, dy=0)

    def move_left(self):
        """Define movement towards the port side"""
        self.move(dx=-1, dy=0)

    def attack(self):
        """Attack the enemy by removing health points"""
        # always use the best weapon in the inventory
        damage = self.most_powerful_weapon()
        # define the enemy's poition in the room
        position = map.room_at(self.x, self.y, self)
        enemy = position.enemy
        # declare which weapon is used and change the value of the enemy's hp
        print("You use {} against {}!".format('guns', enemy.name))
        enemy.hp -= damage
        # print out if the enemy is alive and how many hps remain
        if not enemy.is_alive():
            print("You killed a {}".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def most_powerful_weapon(self):
        """Determine the most power weapon in the inventory"""
        max_damage = 0
        # check the damage of each weapon in the inventory
        for weapon in self.weapon:
            if weapon.count:
                max_damage += weapon.damage
                if weapon.name == 'Bullet':
                    weapon.count = weapon.count - 1
        return max_damage

    def heal(self):
        """Check and use consumables for healing"""
        # add consumables from the inventory
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]

        # print a message if there are no consumables
        if not consumables:
            print("You do not have any items to heal you!")
            return

        # print out a list of available consumables
        print("Choose an item to use to heal yourself: ")
        for i, item in enumerate(consumables, 1):
            print("{}. {}".format(i, item))

        # choose a consumable from the list and use it
        valid = False
        while not valid:
            choice = input("")
            try:
                to_use = consumables[int(choice) - 1]
                # cap player's health points to 100
                self.hp = min(100, self.hp + to_use.healing_value)
                # remove the used item from the inventory
                # and print current health points
                print("Current HP: {}".format(self.hp))
                if isinstance(to_use, items.Poison) and self.hp < 0:
                    print("""
----------------------------- You Died ------------------------------------
You drank the poison !
-----------------------------------------------------------------------------
                    """)
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def drink_poison(self):
        soup_and_poison = []
        for i in self.inventory:
            if isinstance(i, items.Soup):
                soup_and_poison.append(i.name)
            if isinstance(i, items.Poison):
                soup_and_poison.append(i.name)
        if 'Soup' in soup_and_poison and 'Poison' in soup_and_poison:
            if self.partner:
                self.drink = 1
            else:
                self.drink = 0
        else:
            self.drink = -1

    def collect_items(self):
        """Add items to the player's inventory """
        # define the position in the room
        position = map.room_at(self.x, self.y, self)
        # add the inventory from the room tile to the player's inventory
        current_inventory = self.inventory
        position.add_inventory(current_inventory)
