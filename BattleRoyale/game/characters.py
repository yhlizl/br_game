class Character:
    def __init__(self, name, position, attack_power=1, stamina=5, level=1):
        self.name = name
        self.position = position
        self.attack_power = attack_power
        self.stamina = stamina
        self.level = level
    def to_dict(self):
        return {
            'name': self.name,
            'position': self.position,
            'attack_power': self.attack_power,
            'stamina': self.stamina,
            'level': self.level
        }