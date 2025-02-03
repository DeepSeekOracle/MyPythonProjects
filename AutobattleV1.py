import random
import time

# Define Unit class
class Unit:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        damage_taken = max(damage - self.defense, 0)
        self.health -= damage_taken
        return damage_taken

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack // 2, self.attack)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        damage_taken = enemy.take_damage(damage)
        print(f"{enemy.name} takes {damage_taken} damage, remaining health: {enemy.health}")

# Define Team class
class Team:
    def __init__(self, name, units):
        self.name = name
        self.units = units

    def get_alive_units(self):
        return [unit for unit in self.units if unit.is_alive()]

# Define AutoBattler class
class AutoBattler:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def battle(self):
        round_counter = 1
        while self.team1.get_alive_units() and self.team2.get_alive_units():
            print(f"\n--- Round {round_counter} ---")
            self.simulate_turn()
            round_counter += 1
            time.sleep(1)

        self.end_battle()

    def simulate_turn(self):
        team1_unit = random.choice(self.team1.get_alive_units())
        team2_unit = random.choice(self.team2.get_alive_units())

        # Team 1 attacks Team 2
        team1_unit.attack_enemy(team2_unit)

        if not team2_unit.is_alive():
            print(f"{team2_unit.name} has been defeated!")

        # Team 2 attacks Team 1
        if self.team1.get_alive_units() and self.team2.get_alive_units():
            team2_unit = random.choice(self.team2.get_alive_units())
            team1_unit = random.choice(self.team1.get_alive_units())
            team2_unit.attack_enemy(team1_unit)

            if not team1_unit.is_alive():
                print(f"{team1_unit.name} has been defeated!")

    def end_battle(self):
        if not self.team1.get_alive_units():
            print(f"\n{self.team2.name} wins the battle!")
        elif not self.team2.get_alive_units():
            print(f"\n{self.team1.name} wins the battle!")

# Example units
unit1 = Unit("Warrior", health=100, attack=20, defense=5)
unit2 = Unit("Archer", health=80, attack=25, defense=3)
unit3 = Unit("Mage", health=70, attack=30, defense=2)
unit4 = Unit("Tank", health=150, attack=15, defense=10)

unit5 = Unit("Knight", health=120, attack=18, defense=7)
unit6 = Unit("Assassin", health=60, attack=35, defense=1)
unit7 = Unit("Priest", health=90, attack=10, defense=5)
unit8 = Unit("Berserker", health=110, attack=28, defense=4)

# Create two teams
team1 = Team("Red Team", [unit1, unit2, unit3, unit4])
team2 = Team("Blue Team", [unit5, unit6, unit7, unit8])

# Start the battle
battler = AutoBattler(team1, team2)
battler.battle()
