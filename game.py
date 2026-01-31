import random

from colorama import init, Fore, Style


class Thing:
    def __init__(self, name: str, protection: float, attack: int, hp: int):
        self.name = name
        self.protection = protection
        self.attack = attack
        self.hp = hp


class Person:
    BASE_HP = 100
    BASE_ATTACK = 10
    BASE_PROTECTION = 0.05

    def __init__(self, name: str, hp: int | None,
                 base_attack: int | None,
                 base_protection: float | None):
        self.name = name
        self.hp = hp if hp is not None else self.BASE_HP
        self.base_attack = (base_attack if base_attack is not None
                            else self.BASE_ATTACK)
        self.base_protection = (base_protection if base_protection is not None
                                else self.BASE_PROTECTION)
        self.things: list[Thing] = []
        self.race = 'Creature'

    def set_things(self, things):
        self.things = things
        for thing in self.things:
            self.hp += thing.hp

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
    def __init__(self, name: str, hp=None,
                 base_attack=None, base_protection=None):
        super().__init__(name, hp, base_attack, base_protection)

        if hp is None:
            self.hp *= 2
        if base_protection is None:
            self.base_protection *= 2

        self.race = 'Паладин'


class Warrior(Person):
    def __init__(self, name: str, hp=None,
                 base_attack=None, base_protection=None):
        super().__init__(name, hp, base_attack, base_protection)

        if base_attack is None:
            self.base_attack *= 2

        self.race = 'Воин'


class Elf(Person):
    def __init__(self, name: str, hp=None,
                 base_attack=None, base_protection=None):
        super().__init__(name, hp, base_attack, base_protection)

        if base_attack is None:
            self.base_attack = int(self.base_attack * 2)
        if base_protection is None:
            self.base_protection *= 1.5

        self.race = 'Эльф'


things = [
    Thing('Шлем', 0.05, 0, 10),
    Thing('Нагрудник', 0.1, 0, 20),
    Thing('Кольцо', 0.03, 5, 0),
    Thing('Сапожи', 0.02, 0, 5),
    Thing('Меч', 0.0, 10, 0),
    Thing('Щит', 0.07, 0, 15),
]
elf_things = [
    Thing('Кольцо Эльфов', 0.2, 0, 25),
    Thing('Эльфийский меч', 0.0, 20, 0),
    Thing('Эльфийский лук', 0.0, 15, 0),
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
        person = Paladin(name)
    elif race == 'warrior':
        person = Warrior(name)
    else:
        person = Elf(name)

    persons.append(person)

for person in persons:
    count = random.randint(1, 4)
    items = random.sample(things, count)
    if isinstance(person, Elf):
        items.append(random.choice(elf_things))
    person.set_things(items)


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
    print('В боях ему помогли следующие артефакты:',
          ', '.join(thing.name.lower() for thing in winner.things))


if __name__ == '__main__':
    main()
