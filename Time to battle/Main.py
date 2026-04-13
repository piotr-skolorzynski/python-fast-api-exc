from Enemy import Enemy
from Zombie import Zombie
from Ogre import Ogre
from Hero import Hero
from Weapon import Weapon


# def battle(hero: Enemy, enemy: Enemy):
#     hero.talk()
#     enemy.talk()

#     while hero.health_points > 0 and enemy.health_points > 0:
#         print("-----------------")
#         hero.special_attack()
#         enemy.special_attack()
#         print(f"{hero.get_type_of_enemy()}: {hero.health_points} HP left")
#         print(f"{enemy.get_type_of_enemy()}: {enemy.health_points} HP left")
#         enemy.attack()
#         hero.health_points -= enemy.attack_damage
#         hero.attack()
#         enemy.health_points -= hero.attack_damage

#     print("-----------------")
#     if hero.health_points > 0:
#         print(f"{hero.get_type_of_enemy()} wins!")
#     else:
#         print(f"{enemy.get_type_of_enemy()} wins!")


# zombie = Zombie(10, 1)
# print(zombie.get_type_of_enemy())
# print(zombie.talk())
# print(zombie.spread_disease())

# ogre = Ogre(20, 3)

# print(
#     f"\n{zombie.get_type_of_enemy()} has {zombie.health_points} and can do attack of {zombie.attack_damage} damage"
# )
# print(
#     f"\n{ogre.get_type_of_enemy()} has {ogre.health_points} and can do attack of {ogre.attack_damage} damage"
# )


# zombie.talk()
# ogre.talk()

# battle(zombie, ogre)


def hero_battle(hero: Hero, enemy: Enemy):

    while hero.health_points > 0 and enemy.health_points > 0:
        print("-----------------")

        enemy.special_attack()

        print(f"Hero: {hero.health_points} HP left")
        print(f"{enemy.get_type_of_enemy()}: {enemy.health_points} HP left")
        enemy.attack()
        hero.health_points -= enemy.attack_damage
        hero.attack()
        enemy.health_points -= hero.attack_damage

    print("-----------------")
    if hero.health_points > 0:
        print("Hero wins!")
    else:
        print(f"{enemy.get_type_of_enemy()} wins!")


hero = Hero(10, 1)
zombie = Zombie(10, 1)
ogre = Ogre(20, 3)
weapon = Weapon("Sword", 5)
hero.weapon = weapon
hero.equip_weapon()
# hero_battle(hero, zombie)
hero_battle(hero, ogre)
