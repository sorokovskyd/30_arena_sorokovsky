import random

from colorama import init, Fore, Style


class Thing:
    def __init__(self, name: str, protection: float, attack: int, hp: int):
        self.name = name
        self.protection = protection
        self.attack = attack
        self.hp = hp


class Person:
    def __init__(self, name: str, hp: int,
                 base_attack: int, base_protection: float):
        self.name = name
        self.hp = hp
        self.base_attack = base_attack
        self.base_protection = base_protection
        self.things: list[Thing] = []
        self.race = 'Creature'

    def set_things(self, things):
        self.things = things

    def take_damage(self, attack_damage):
        final_protection = self.base_protection
        for thing in self.things:
            final_protection += thing.protection

        damage = attack_damage - attack_damage*final_protection
        if damage < 0:
            damage = 0
        self.hp -= int(damage)
        return int(damage)

    def get_attack_damage(self):
        attack = self.base_attack
        for thing in self.things:
            attack += thing.attack
        return attack

    def attack(self, other):
        attack_damage = self.get_attack_damage()
        damage = other.take_damage(attack_damage)
        return damage


class Paladin(Person):
    def __init__(self, name: str, hp: int,
                 base_attack: int, base_protection: float):
        super().__init__(
            name,
            hp*2,
            base_attack,
            base_protection*2,
        )
        self.race = 'Паладин'


class Warrior(Person):
    def __init__(self, name: str, hp: int,
                 base_attack: int, base_protection: float):
        super().__init__(
            name,
            hp,
            base_attack*2,
            base_protection,
        )
        self.race = 'Воин'


class Elf(Person):
    def __init__(self, name: str, hp: int,
                 base_attack: int, base_protection: float):
        super().__init__(
            name,
            hp,
            base_attack*2,
            base_protection*1.5,
        )
        self.race = 'Эльф'


things = [
    Thing('Helmet', 0.05, 0, 10),
    Thing('Armor', 0.1, 0, 20),
    Thing('Ring', 0.03, 5, 0),
    Thing('Boots', 0.02, 0, 5),
    Thing('Sword', 0.0, 10, 0),
    Thing('Shield', 0.07, 0, 15),
]
things.sort(key=lambda x: x.protection)

names = [
    'Aragorn', 'Legolas', 'Gimli', 'Geralt', 'Kratos',
    'Arthur', 'Ezio', 'Altair', 'Thor', 'Loki',
    'Achilles', 'Hector', 'Zeus', 'Ritis', 'Ares',
    'Odin', 'Leonid', 'Perseus', 'Hercules', 'Boromir',
]

persons = []

for _ in range(10):
    name = random.choice(names)
    race = random.choice(['paladin', 'warrior', 'elf'])
    if race == 'paladin':
        person = Paladin(name, 100, 10, 0.05)
    elif race == 'warrior':
        person = Warrior(name, 100, 10, 0.05)
    else:
        person = Elf(name, 100, 10, 0.05)

    persons.append(person)

for person in persons:
    count = random.randint(1, 4)
    person.set_things(random.sample(things, count))


def main():
    round_number = 1
    while len(persons) > 1:
        attacker, defender = random.sample(persons, 2)
        damage = attacker.attack(defender)

        print(
            Fore.YELLOW + f'Раунд {round_number}: ' + Style.RESET_ALL +
            f'{attacker.name} атакует {defender.name} '
            + Fore.RED + f'на {damage} урона' + Style.RESET_ALL
        )

        if defender.hp <= 0:
            print(Fore.LIGHTRED_EX + f'{defender.name} погиб в бою\n'
                  + Style.RESET_ALL)
            persons.remove(defender)

        round_number += 1

    winner = persons[0]
    print(Fore.GREEN + '🏆 Победитель арены:'
          + Style.RESET_ALL + f' {winner.race} {winner.name}')


if __name__ == '__main__':
    main()
