from Enemy import Enemy
import random


class Ogre(Enemy):
    def __init__(self, health_points, attack_demage):
        super().__init__(
            type_of_enemy="Ogre",
            health_points=health_points,
            attack_demage=attack_demage,
        )

    def talk(self):
        print("Ogre is slamming hands all around")

    def special_attack(self):
        did_special_attack_work = random.random() < 0.2
        if did_special_attack_work:
            self.attack_damage += 4
            print("Ogre gets angry and increases attack by 4")
