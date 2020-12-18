class Weapon():
    """Weapon Class to raise errors and return the weapon's name"""

    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects")

    def __str__(self):
        return "{} (+ {} Damage)".format(self.name, self.damage)


class Guns(Weapon):
    """Guns weapon class with description and damage"""

    def __init__(self):
        self.name = "Guns"
        self.description = """
                            A guns without bullet
                            """
        self.damage = 1
        self.count = 1

    def has_bullets(self):
        return self.bullet_count


class Bullet(Weapon):
    def __init__(self):
        self.name = "Bullet"
        self.damage = 19
        self.count = 10


class Book():
    """Weapon Class to raise errors and return the weapon's name"""

    def __init__(self):
        self.name = "Book's <Eroded dream>"
        self.description = """
In the book there is a note
    - The room in the middle: you can't leave if you don't finish drinking
       the soup, and the real soup is written on the back of the note (Blood,
        no poison at first.)
    - The Kitchen: There are a lot of seasonings and utensils, some prepared
     “soup” in the pot.
    - The Auditorium: the gods are sleeping here, with information about
       poison, the guards will not disappear if they don't eat living things.
    - The library: books are very important so you can't take them out,
       but the candles are okay. You might find what you need in the room,
       but how to use it?
    - The Slave’s room: the good kid is waiting for you, she has good
       things in her hands.
    - The most important thing-: please drink it with the consciousness of
       death."""

    def __str__(self):
        return "{} ({})".format(self.name, self.description)


class Consumable():
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+ {} HP)".format(self.name, self.healing_value)


class Soup(Consumable):
    def __init__(self):
        self.name = "Soup"
        self.healing_value = 100


class Poison(Consumable):
    def __init__(self):
        self.name = "Poison"
        self.healing_value = -99


class Key():
    def __init__(self):
        raise NotImplementedError("Do not create raw Key objects.")

    def __str__(self):
        return "{} (x {})".format(self.name, self.count)


class KeyToLibrary(Key):
    """Key to the library"""

    def __init__(self):
        self.name = "Key To Library"
        self.count = 1


class KeyToAuditorium(Key):
    """Key to the auditorium"""

    def __init__(self):
        self.name = "KeyToAuditorium"
        self.count = 1
