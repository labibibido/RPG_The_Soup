class Enemy():
    """Enemy Class to raise errors and return the enemy's name"""
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Keeper(Enemy):
    """Keeper enemy with name, health points and damage"""
    def __init__(self):
        self.name = "Keeper"
        self.hp = 30
        self.damage = 10


class YoungGirl(Enemy):
    """A young girl with name, health points and damage"""
    def __init__(self):
        self.name = "Young Girl"
        self.hp = 10
        self.damage = 2


class Monster(Enemy):
    """Monster with name, health points and damage"""
    def __init__(self):
        self.name = "Chaugnar Faugn"
        self.hp = 1000
        self.damage = 1000
