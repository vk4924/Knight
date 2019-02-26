from abc import ABC, abstractmethod
import pygame
import random


class AbstractObject(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, display):
        pass


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)
        for message in hero.level_up():
            engine.notify(message)

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

    def interact(self, engine, hero):
        hero.exp += self.xp
        hero.hp -= int(0.2*self.xp)
        if hero.hp < 0:
            engine.notify("Game over")
            engine.game_process = False
            return
        engine.score +=  1
        engine.notify(f"+{self.xp} exp")
        engine.notify(f"-{int(0.2*self.xp)} hp")

        for message in hero.level_up():
            engine.notify(message)

class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

# FIXME
class Berserk(Effect):
    def apply_effect(self):
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["luck"] += 7
        self.stats["intelligence"] -= 3
        return self.stats


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["luck"] += 2
        self.stats["intelligence"] += 2
        return self.stats


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4
        self.stats["luck"] -= 4
        self.stats["intelligence"] -= 4
        return self.stats


