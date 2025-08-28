import sqlite3

DB_FILE = "players.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            name TEXT PRIMARY KEY,
            hp INTEGER,
            mana INTEGER,
            lvl INTEGER,
            xp INTEGER,
            max_hp INTEGER,
            max_mana INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
        self.hp = min(self.hp + amount, self.max_hp)

    def mana_use(self, amount=1):
        self.mana = max(self.mana - amount, 0)

    def mana_recover(self, amount=1):
        self.mana = min(self.mana + amount, self.max_mana)

    def lvl_up(self):
        while self.xp >= (self.lvl + 1) * 100:
            self.xp -= (self.lvl + 1) * 100
            self.lvl += 1
            # Não aumenta HP ou Mana automaticamente

    def gain_xp(self, amount):
        self.xp += amount
        self.lvl_up()
        self.save()

    def save(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO players
            (name, hp, mana, lvl, xp, max_hp, max_mana)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.hp, self.mana, self.lvl, self.xp, self.max_hp, self.max_mana))
        conn.commit()
        conn.close()

    @classmethod
    def load(cls, name):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT * FROM players WHERE name = ?', (name,))
        row = c.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return cls(name=name)
