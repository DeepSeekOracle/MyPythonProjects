import random
import time
import os

# Utility function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------
# Define game objects
# ----------------------------

class Weapon:
    def __init__(self, name, bonus_attack, emoji):
        self.name = name
        self.bonus_attack = bonus_attack
        self.emoji = emoji

    def __str__(self):
        return f"{self.name} {self.emoji} (+{self.bonus_attack} ATK)"


class Armor:
    def __init__(self, name, bonus_defense, emoji):
        self.name = name
        self.bonus_defense = bonus_defense
        self.emoji = emoji

    def __str__(self):
        return f"{self.name} {self.emoji} (+{self.bonus_defense} DEF)"


class Character:
    def __init__(self, name, hp, base_attack, base_defense, emoji):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.weapon = None
        self.armor = None
        self.level = 1
        self.emoji = emoji
        self.gold = 0
        self.battles_won = 0

    def total_attack(self):
        if self.weapon:
            return self.base_attack + self.weapon.bonus_attack
        return self.base_attack

    def total_defense(self):
        if self.armor:
            return self.base_defense + self.armor.bonus_defense
        return self.base_defense

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.base_attack += 2
        self.base_defense += 2

    def equip_weapon(self, weapon):
        self.weapon = weapon

    def equip_armor(self, armor):
        self.armor = armor


class Enemy:
    def __init__(self, name, hp, attack, defense, emoji, is_boss=False):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.emoji = emoji
        self.is_boss = is_boss


# ----------------------------
# Game Data
# ----------------------------

weapons = [
    Weapon("Sword", 5, "🗡️"),
    Weapon("Axe", 7, "⚔️"),
    Weapon("Dagger", 3, "🔪"),
    Weapon("Mace", 6, "🔨")
]

armors = [
    Armor("Leather Armor", 3, "🛡️"),
    Armor("Chainmail", 5, "🛡️"),
    Armor("Plate Armor", 8, "🛡️")
]


# ----------------------------
# Menus and Setup
# ----------------------------

def choose_character():
    clear_screen()
    print("=== Choose Your Character ===")
    characters = [
        Character("Knight", 100, 15, 10, "🤺"),
        Character("Wizard", 80, 20, 5, "🧙"),
        Character("Rogue", 90, 18, 8, "🗡️")
    ]
    for i, char in enumerate(characters, 1):
        print(f"{i}. {char.name} {char.emoji} - HP: {char.max_hp}, ATK: {char.base_attack}, DEF: {char.base_defense}")
    while True:
        try:
            choice = int(input("Enter choice (number): "))
            if 1 <= choice <= len(characters):
                return characters[choice - 1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def options_menu():
    clear_screen()
    print("=== Options Menu ===")
    print("1. Difficulty (Not implemented, default is normal)")
    print("2. Back")
    input("Press Enter to return to main menu...")

def shop_menu(player):
    while True:
        clear_screen()
        print("=== Shop Menu ===")
        print(f"Gold: {player.gold}")
        print("1. Buy/Equip Weapon")
        print("2. Buy/Equip Armor")
        print("3. Exit Shop")
        choice = input("Enter choice: ")
        if choice == "1":
            clear_screen()
            print("Available Weapons:")
            for i, weapon in enumerate(weapons, 1):
                print(f"{i}. {weapon}")
            try:
                choice_w = int(input("Enter weapon number to equip: "))
                if 1 <= choice_w <= len(weapons):
                    player.equip_weapon(weapons[choice_w - 1])
                    print(f"Equipped {weapons[choice_w - 1].name}!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")
            time.sleep(1)
        elif choice == "2":
            clear_screen()
            print("Available Armors:")
            for i, armor in enumerate(armors, 1):
                print(f"{i}. {armor}")
            try:
                choice_a = int(input("Enter armor number to equip: "))
                if 1 <= choice_a <= len(armors):
                    player.equip_armor(armors[choice_a - 1])
                    print(f"Equipped {armors[choice_a - 1].name}!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")
            time.sleep(1)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

# ----------------------------
# Enemy Creation and Random Events
# ----------------------------

def create_enemy(battle_number):
    # Every 10th battle is a boss battle
    is_boss = (battle_number % 10 == 0)
    if is_boss:
        name = "Boss " + random.choice(["Goblin King", "Orc Warlord", "Dragon", "Lich"])
        hp = 100 + battle_number * 5
        attack = 15 + battle_number
        defense = 10 + battle_number // 2
        emoji = "👹"
    else:
        name = random.choice(["Goblin", "Orc", "Skeleton", "Zombie"])
        hp = 50 + battle_number * 3
        attack = 10 + battle_number // 2
        defense = 5 + battle_number // 3
        emoji = random.choice(["👾", "💀", "🧟", "👹"])
    return Enemy(name, hp, attack, defense, emoji, is_boss)

def random_event(player):
    # 20% chance for a random event after battle
    if random.random() < 0.2:
        clear_screen()
        event_type = random.choice(["gold", "trap", "stat"])
        if event_type == "gold":
            gold_found = random.randint(5, 20)
            player.gold += gold_found
            print(f"Random Event: You discovered a treasure chest with {gold_found} gold! 💰")
        elif event_type == "trap":
            damage = random.randint(5, 15)
            player.hp = max(0, player.hp - damage)
            print(f"Random Event: A hidden trap triggers! You take {damage} damage! ⚠️")
        elif event_type == "stat":
            print("Random Event: A magical aura empowers you! Your stats increase slightly!")
            player.base_attack += 1
            player.base_defense += 1
        time.sleep(2)

# ----------------------------
# Battle Function
# ----------------------------

def battle(player, enemy):
    clear_screen()
    print(f"A wild {enemy.name} {enemy.emoji} appears!")
    time.sleep(1)
    while player.hp > 0 and enemy.hp > 0:
        clear_screen()
        print(f"{player.name} {player.emoji}: HP {player.hp}/{player.max_hp}")
        print(f"{enemy.name} {enemy.emoji}: HP {enemy.hp}/{enemy.max_hp}")
        print("\nBattle in progress...\n")
        # Simulate attack effect
        time.sleep(0.5)
        
        # Player attacks enemy
        p_attack = player.total_attack()
        damage = max(0, p_attack - enemy.defense)
        enemy.hp -= damage
        effect = "💥" if damage > 0 else "🌀"
        print(f"{player.name} attacks with {player.weapon.emoji if player.weapon else 'bare hands'} {effect} for {damage} damage!")
        time.sleep(1)
        if enemy.hp <= 0:
            print(f"{enemy.name} is defeated!")
            break
        
        # Enemy attacks player
        damage = max(0, enemy.attack - player.total_defense())
        player.hp -= damage
        effect = "🔥" if damage > 0 else "💨"
        print(f"{enemy.name} attacks {player.name} {effect} for {damage} damage!")
        time.sleep(1)
    return player.hp > 0

# ----------------------------
# Main Game Loop
# ----------------------------

def game_loop(player):
    battle_number = 1
    while player.hp > 0:
        enemy = create_enemy(battle_number)
        won = battle(player, enemy)
        if not won:
            break
        player.battles_won += 1
        clear_screen()
        print("Battle won!")
        # Award gold for victory
        gold_reward = random.randint(10, 30)
        player.gold += gold_reward
        print(f"You earned {gold_reward} gold!")
        time.sleep(1)
        # Trigger a random event chance
        random_event(player)
        # Prompt for leveling up
        print("Do you want to level up your character? (y/n)")
        if input().lower() == "y":
            player.level_up()
            print("Level Up! Your stats have increased!")
            time.sleep(1)
        # Option to visit the shop for new gear
        print("Do you want to visit the shop? (y/n)")
        if input().lower() == "y":
            shop_menu(player)
        battle_number += 1
    # Game Over Screen
    clear_screen()
    print("=== Game Over ===")
    print(f"You won {player.battles_won} battles before falling in combat.")
    input("Press Enter to return to the main menu...")

# ----------------------------
# Start Game and Main Menu
# ----------------------------

def start_game():
    player = choose_character()
    # Equip default gear if none chosen
    if not player.weapon:
        player.equip_weapon(weapons[0])
    if not player.armor:
        player.equip_armor(armors[0])
    game_loop(player)

def main_menu():
    while True:
        clear_screen()
        print("=== Dungeon Auto Battler ===")
        print("1. Start Game")
        print("2. Options")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            start_game()
        elif choice == "2":
            options_menu()
        elif choice == "3":
            clear_screen()
            print("Goodbye, adventurer!")
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
