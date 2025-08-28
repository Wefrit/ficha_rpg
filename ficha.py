import json
import os

class Player:
    def __init__(self, name, hp=10, mana=5, lvl=1, xp=0, max_hp=None, max_mana=None):
        self.name = name
        self.hp = hp
        self.mana = mana
        self.lvl = lvl
        self.xp = xp
        self.max_hp = max_hp if max_hp is not None else hp
        self.max_mana = max_mana if max_mana is not None else mana

    def take_damage(self, amount=1):
        self.hp = max(self.hp - amount, 0)

    def heal(self, amount=1):
        self.hp += amount

    def mana_use(self, amount=1):
        self.mana = max(self.mana - amount, 0)

    def mana_recover(self, amount=1):
        self.mana += amount

    def lvl_up(self):
        """
        Sobe de nível consumindo o XP necessário.
        Aqui você pode chamar sua lógica de ajustar HP/Mana máximos.
        """
        while self.xp >= (self.lvl + 1) * 100:
            xp_needed = (self.lvl + 1) * 100
            self.xp -= xp_needed
            self.lvl += 1
            # HP e Mana máximos podem ser ajustados no Flask na interface

    def gain_xp(self, amount):
        self.xp += amount
        self.lvl_up()

    def save(self):
        if not os.path.exists("players"):
            os.makedirs("players")
        path = os.path.join("players", f"{self.name}.json")
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    @classmethod
    def load(cls, name):
        path = os.path.join("players", f"{name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            return cls(**data)
        else:
            return cls(name=name)
