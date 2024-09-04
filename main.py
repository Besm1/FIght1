import random

WEAPONS = ['меч', 'палица']
ARMORS = ['щит', 'кольчуга']
MEDECINS = ['зелье']

class Hero:

    def __init__(self, health=100, level=1, attack_damage=10):
        self.health = health
        self.level = level
        self.attack_damage = attack_damage
        self.inventory = {}

    def __add_invent(self, i: str):
        if i in self.inventory.keys():
            self.inventory[i,0] += 1
        else:
            self.inventory[i] = (1,)

    def find_item(self, *item):
        if item[0] in WEAPONS + ARMORS + MEDECINS:
            print(f'Вы нашли {item}')
            if item[0] in self.inventory.keys():
                self.inventory[item[0]][0] += 1
                self.inventory[item[0]].append(list([item[1] if len(item) >= 2 else random.randint(3,7),  # сила меча/ защита щита
                                                     item[2] if len(item) >= 3 else random.randint(3,5),
                                                     item[3] if len(item) >= 4 else 'weapon' if item[0] in WEAPONS
                                                        else 'armor' if item[0] in ARMORS else 'medecin'
                                                     ])) # прочность меча/ щита
            else:
                self.inventory[item[0]] = list((1, list((item[1] if len(item) >= 2 else random.randint(3,7),  # сила меча
                                                         item[2] if len(item) >= 3 else random.randint(3,5),
                                                         item[3] if len(item) >= 4 else 'weapon' if item[0] in WEAPONS
                                                              else 'armor' if item[0] in ARMORS else 'medecin'
                                                         )))) # прочность меча/щита

        else:
            print(f'Вы нашли непонятный предмет "{item}"! Бросьте, это бяка!')

    def use_inventory(self, item: str) -> int:   # возвращает изменение силы удара от применения оружия или защиты
        variation = 0
        if item in self.inventory.keys():
            print(f'  -> Вы применили {item}... ', end='')
            item_properties = self.inventory[item][1]
            # print(f'self.inventory[item][1] = {self.inventory[item][1]}')
            # print(f'item_properties: {item_properties}')
            variation = item_properties[0] * -1 if item_properties[2] == 'armor' else 1 # уменьшили силу удара на силу щита
            # print(f"self.inventory['щит'][1] {self.inventory['щит'][1]}")
            self.inventory[item][1][1] -= 1  # Отняли одну жизнь у предмета
            if self.inventory[item][1][1] <= 0:  # предмет разрушен
                print(f'Ваш {item} разрушен! У Вас ', end='')
                self.inventory[item][0] -= 1  # уменьшим кол-во щитов
                # print('До уничтожения', self.inventory[item])
                if self.inventory[item][0] == 0:  # щитов не осталось
                    print(f'не осталось предметов "{item}"!', end='')
                    self.inventory.pop(item)
                    # print('После уничтожения', self.inventory[item])
                else:
                    print(f'осталось {self.inventory[item][0]} предметов "{item}".', end='')
                    self.inventory[item].pop(1)
                    # print('После уничтожения', self.inventory[item])
            print()
        return variation

    def is_attacked(self, hit_power: int) -> int:
        for item_ in ARMORS:
            hit_power += self.use_inventory(item_)
        self.health -= hit_power
        return hit_power



    def attack(self, mob):
        print(f"Вы напали на {mob.name}!!!")
        hit_power = self.attack_damage
        for item_ in WEAPONS:
            hit_power += self.use_inventory(item_)
        # print('hit power', hit_power)
        damage = mob.is_attacked(hit_power)
        print(f"Вы нанесли урон {damage}. У {mob.name} осталось {mob.health} здоровья.")

    def show_status(self):
        health_status = f"Здоровье героя: {self.health}"
        inventory_status = f"Инвентарь героя: {', '.join(self.inventory) if self.inventory else 'пусто'}"
        level_status = f"Уровень героя: {self.level}"
        attack_status = f"Урон атаки героя: {self.attack_damage}"
        print(health_status)
        print(inventory_status)
        print(level_status)
        print(attack_status)

class Mob:

    def __init__(self, name, health, attack_damage):
        self.name = name
        self.health = health
        self.attack_damage = attack_damage

    def attack(self, hero):
        print(f'На вас напал {self.name}!!!')
        damage = hero.is_attacked(self.attack_damage)
        print(f"Вам нанесён урон {damage}. У вас осталось {hero.health} здоровья.")

    def is_attacked(self, hit_power: int) -> int:
        self.health -= hit_power
        return hit_power

def main():
    hero = Hero()
    orc = Mob("Орк", 120, 15)
    # hero.find_item('меч', 5, 5)
    # hero.find_item('меч')
    # hero.find_item('щит')
    # hero.find_item('щит')
    hero.show_status()

    print(hero.inventory)

    print("\nНачинается бой!")
    round = 0
    while hero.health > 0 and orc.health > 0:
        round += 1
        print(f'Раунд {round}')
        if random.randint(0, 1) == 0:
            hero.attack(orc)
        else:
            orc.attack(hero)

        if random.randint(0, 5) == 3:  # случайное число
            kind = random.randint(0, 2)
            if kind == 0:
                hero.find_item(WEAPONS[random.randint(0, len(WEAPONS)-1)])
            elif kind == 1:
                hero.find_item(ARMORS[random.randint(0, len(ARMORS) - 1)])
            else:
                hero.find_item(MEDECINS[random.randint(0, len(MEDECINS) - 1)])
        print()

    if hero.health > 0:
        print(f"Вы победили {orc.name}!")
    else:
        print(f"Вы были побеждены {orc.name}...")

if __name__ == '__main__':
    main()
"""Дальше на фантазию (что можно реализовать еще): 
Может уровень героя как-то будет влиять на характеристики? Что с инвентарем? Как на счет придумать свой метод 
взаимодействия с ним? (может предметы будут теряться от какого-то условия? Или использоваться?) 
Зелья для восстановления хит-поинтов? Броня?
С самой интересной реализацией будем продолжать на следующем вебинаре (этот код пока без наследования делайте).
"""