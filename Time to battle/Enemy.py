class Enemy:
    def __init__(self, type_of_enemy, health_points=10, attack_demage=1):
        self.__type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.attack_damage = attack_demage

    def get_type_of_enemy(self):
        return self.__type_of_enemy

    def talk(self):
        print(f"I'm a {self.__type_of_enemy}. Be prepared to fight!")

    def walk_forward(self):
        print(f"{self.__type_of_enemy} moves closer to you.")

    def attack(self):
        print(f"{self.__type_of_enemy} attacks for {self.attack_damage} damage.")

    def special_attack(self):
        print("Enemy has no special attack")
