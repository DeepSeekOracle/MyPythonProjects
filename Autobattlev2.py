import random
import time
import os
import json
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Utility function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------
# Data Classes
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

class Item:
    def __init__(self, name, effect, cost, emoji):
        self.name = name
        self.effect = effect  # HP restoration amount
        self.cost = cost
        self.emoji = emoji

    def __str__(self):
        return f"{self.name} {self.emoji} (Restores {self.effect} HP, Cost: {self.cost} gold)"

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
        self.inventory = {}  # inventory will hold items (by name)
        self.special_meter = 0  # Build up for a special ability
        self.combo_meter = 0    # Increases with consecutive hits

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

    def add_item(self, item, quantity=1):
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def use_item(self):
        if not self.inventory:
            print(Fore.YELLOW + "You have no items in your inventory!")
            return False
        print(Fore.CYAN + "Inventory:")
        for idx, (item_name, info) in enumerate(self.inventory.items(), 1):
            print(f"{idx}. {info['item']} x{info['quantity']}")
        try:
            choice = int(input("Choose an item to use (0 to cancel): "))
            if choice == 0:
                return False
            if 1 <= choice <= len(self.inventory):
                chosen_item = list(self.inventory.items())[choice - 1]
                item_obj = chosen_item[1]['item']
                heal = item_obj.effect
                self.hp = min(self.max_hp, self.hp + heal)
                print(Fore.GREEN + f"Used {item_obj.name} {item_obj.emoji}. Restored {heal} HP!")
                self.inventory[item_obj.name]['quantity'] -= 1
                if self.inventory[item_obj.name]['quantity'] <= 0:
                    del self.inventory[item_obj.name]
                return True
            else:
                print(Fore.YELLOW + "Invalid choice.")
                return False
        except ValueError:
            print(Fore.YELLOW + "Invalid input.")
            return False

    def use_special_ability(self, enemy):
        """Use special ability: deals triple damage and resets special meter."""
        if self.special_meter >= 100:
            bonus = self.total_attack() * 3
            enemy.hp -= bonus
            print(Fore.RED + f"{self.name} unleashes a SPECIAL MOVE {self.weapon.emoji if self.weapon else 'fists'} for {bonus} damage!")
            self.special_meter = 0
            self.combo_meter = 0  # Reset combo meter as well
            return True
        return False

class Enemy:
    def __init__(self, name, hp, attack, defense, emoji, is_boss=False):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.emoji = emoji
        self.is_boss = is_boss
        self.heal_used = False  # Can heal once per battle

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

items = [
    Item("Health Potion", 30, 20, "🧪"),
    Item("Greater Health Potion", 50, 35, "🧪"),
    Item("Elixir", 100, 50, "✨")
]

# ----------------------------
# Save/Load Game Functions
# ----------------------------

SAVE_FILE = "savegame.json"

def save_game(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "base_attack": player.base_attack,
        "base_defense": player.base_defense,
        "level": player.level,
        "gold": player.gold,
        "battles_won": player.battles_won,
        "special_meter": player.special_meter,
        "combo_meter": player.combo_meter,
        "weapon": player.weapon.name if player.weapon else None,
        "armor": player.armor.name if player.armor else None,
        "inventory": {k: v['quantity'] for k, v in player.inventory.items()},
        "emoji": player.emoji
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print(Fore.GREEN + "Game saved!")
    time.sleep(1)

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        # Reconstruct character from saved data
        player = Character(data["name"], data["max_hp"], data["base_attack"], data["base_defense"], data["emoji"])
        player.hp = data["hp"]
        player.level = data["level"]
        player.gold = data["gold"]
        player.battles_won = data["battles_won"]
        player.special_meter = data["special_meter"]
        player.combo_meter = data["combo_meter"]
        if data["weapon"]:
            for w in weapons:
                if w.name == data["weapon"]:
                    player.weapon = w
                    break
        if data["armor"]:
            for a in armors:
                if a.name == data["armor"]:
                    player.armor = a
                    break
        for item_name, qty in data["inventory"].items():
            for itm in items:
                if itm.name == item_name:
                    player.inventory[item_name] = {'item': itm, 'quantity': qty}
                    break
        print(Fore.GREEN + "Game loaded successfully!")
        time.sleep(1)
        return player
    except Exception as e:
        print(Fore.RED + f"Failed to load game: {e}")
        time.sleep(1)
        return None

# ----------------------------
# Menus and Setup
# ----------------------------

def game_intro():
    clear_screen()
    print(Fore.CYAN + "Welcome, brave adventurer!")
    print("In a land of peril and mystery, you embark on a quest to vanquish foes, discover treasures,")
    print("and challenge the forces of darkness. May the dice roll in your favor, and your sword strike true!")
    input("\nPress Enter to begin your quest...")

def choose_character():
    clear_screen()
    print(Fore.MAGENTA + "=== Choose Your Character ===")
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
    print(Fore.MAGENTA + "=== Options Menu ===")
    print("1. Difficulty (Not implemented, default is normal)")
    print("2. Back")
    input("Press Enter to return to the main menu...")

def shop_menu(player):
    while True:
        clear_screen()
        print(Fore.BLUE + "=== Shop Menu ===")
        print(f"Gold: {player.gold}")
        print("1. Buy/Equip Weapon")
        print("2. Buy/Equip Armor")
        print("3. Buy Items")
        print("4. Save Game")
        print("5. Exit Shop")
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
                    print(Fore.GREEN + f"Equipped {weapons[choice_w - 1].name}!")
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
                    print(Fore.GREEN + f"Equipped {armors[choice_a - 1].name}!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")
            time.sleep(1)
        elif choice == "3":
            clear_screen()
            print("Available Items:")
            for i, item in enumerate(items, 1):
                print(f"{i}. {item}")
            try:
                choice_i = int(input("Enter item number to buy: "))
                if 1 <= choice_i <= len(items):
                    chosen_item = items[choice_i - 1]
                    if player.gold >= chosen_item.cost:
                        player.gold -= chosen_item.cost
                        player.add_item(chosen_item)
                        print(Fore.GREEN + f"Bought {chosen_item.name}!")
                    else:
                        print(Fore.YELLOW + "Not enough gold!")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")
            time.sleep(1)
        elif choice == "4":
            save_game(player)
        elif choice == "5":
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
        event_type = random.choice(["gold", "trap", "stat", "potion", "fountain"])
        if event_type == "gold":
            gold_found = random.randint(5, 20)
            player.gold += gold_found
            print(Fore.GREEN + f"Random Event: You discovered a treasure chest with {gold_found} gold! 💰")
        elif event_type == "trap":
            damage = random.randint(5, 15)
            player.hp = max(0, player.hp - damage)
            print(Fore.RED + f"Random Event: A hidden trap triggers! You take {damage} damage! ⚠️")
        elif event_type == "stat":
            print("Random Event: A magical aura empowers you! Your stats increase slightly!")
            player.base_attack += 1
            player.base_defense += 1
        elif event_type == "potion":
            found_item = random.choice(items)
            print(Fore.GREEN + f"Random Event: You found a {found_item.name} {found_item.emoji} on the ground!")
            player.add_item(found_item)
        elif event_type == "fountain":
            heal_amount = random.randint(10, 25)
            player.hp = min(player.max_hp, player.hp + heal_amount)
            print(Fore.BLUE + f"Random Event: You find a healing fountain and recover {heal_amount} HP!")
        time.sleep(2)

# ----------------------------
# Battle Function with Enhancements
# ----------------------------

def battle(player, enemy):
    clear_screen()
    print(Fore.MAGENTA + f"A wild {enemy.name} {enemy.emoji} appears!")
    time.sleep(1)
    battle_log = []
    while player.hp > 0 and enemy.hp > 0:
        clear_screen()
        print(f"{player.name} {player.emoji}: HP {Fore.GREEN}{player.hp}/{player.max_hp} | Special: {player.special_meter}/100 | Combo: {player.combo_meter}")
        print(f"{enemy.name} {enemy.emoji}: HP {Fore.RED}{enemy.hp}/{enemy.max_hp}")
        print("\nBattle in progress...\n")
        time.sleep(0.5)
        
        # --- Player's Turn ---
        # Offer special ability if meter is full
        if player.special_meter >= 100:
            choice = input(Fore.RED + "Your special meter is full! Use special ability? (y/n): ")
            if choice.lower() == "y":
                used = player.use_special_ability(enemy)
                battle_log.append("Special ability used!")
                if enemy.hp <= 0:
                    print(Fore.GREEN + f"{enemy.name} is defeated by your special move!")
                    break
                time.sleep(1)
                continue  # Skip normal attack this turn
        
        # Normal attack
        p_attack = player.total_attack()
        base_damage = max(0, p_attack - enemy.defense)
        damage = base_damage
        
        # Chance for critical hit
        critical = False
        if random.random() < 0.1:
            damage *= 2
            critical = True
        
        # Update combo meter if damage dealt
        if damage > 0:
            player.combo_meter += 1
            # Every 3 consecutive hits add bonus damage
            if player.combo_meter >= 3:
                bonus = int(0.5 * base_damage)
                damage += bonus
                battle_log.append(f"Combo bonus! +{bonus} damage.")
                player.combo_meter = 0
        else:
            player.combo_meter = 0  # reset if miss
        
        enemy.hp -= damage
        # Increase special meter slightly with every hit
        player.special_meter = min(100, player.special_meter + 10)
        effect = Fore.YELLOW + "💥" if damage > 0 else "🌀"
        crit_text = Fore.RED + " Critical Hit!" if critical else ""
        print(f"{player.name} attacks with {player.weapon.emoji if player.weapon else 'bare hands'} {effect}{crit_text} for {damage} damage!")
        battle_log.append(f"Player dealt {damage} damage.")
        time.sleep(1)
        if enemy.hp <= 0:
            print(Fore.GREEN + f"{enemy.name} is defeated!")
            battle_log.append("Enemy defeated.")
            break

        # --- Check for Low HP and Offer to Use Item ---
        if player.hp < 0.3 * player.max_hp and player.inventory:
            print(Fore.GREEN + "Your HP is low. Do you want to use an item? (y/n)")
            if input().lower() == "y":
                player.use_item()
                time.sleep(1)
        
        # --- Enemy's Turn ---
        # Enemy special: Heal themselves if low on HP and not used yet
        if enemy.hp < enemy.max_hp/2 and not enemy.heal_used and random.random() < 0.2:
            heal_amount = int(0.1 * enemy.max_hp)
            enemy.hp = min(enemy.max_hp, enemy.hp + heal_amount)
            enemy.heal_used = True
            print(Fore.CYAN + f"{enemy.name} uses a healing ability and recovers {heal_amount} HP!")
            battle_log.append("Enemy healed.")
            time.sleep(1)
        else:
            # Enemy attack with a chance for critical hit
            enemy_attack = enemy.attack
            enemy_critical = False
            if random.random() < 0.1:
                enemy_attack *= 2
                enemy_critical = True
            damage = max(0, enemy_attack - player.total_defense())
            player.hp -= damage
            effect = Fore.MAGENTA + "🔥" if damage > 0 else "💨"
            crit_text = Fore.RED + " Critical Hit!" if enemy_critical else ""
            print(f"{enemy.name} attacks {player.name} {effect}{crit_text} for {damage} damage!")
            battle_log.append(f"Enemy dealt {damage} damage.")
            time.sleep(1)
    return player.hp > 0

# ----------------------------
# Main Game Loop and Game Over
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
        print(Fore.GREEN + "Battle won!")
        # Award gold for victory
        gold_reward = random.randint(10, 30)
        player.gold += gold_reward
        print(f"You earned {gold_reward} gold!")
        time.sleep(1)
        # Trigger a random event
        random_event(player)
        # Prompt for leveling up
        print("Do you want to level up your character? (y/n)")
        if input().lower() == "y":
            player.level_up()
            print("Level Up! Your stats have increased!")
            time.sleep(1)
        # Option to visit the shop for new gear or items
        print("Do you want to visit the shop? (y/n)")
        if input().lower() == "y":
            shop_menu(player)
        # Option to save game progress after each battle
        print("Do you want to save your progress? (y/n)")
        if input().lower() == "y":
            save_game(player)
        battle_number += 1
    # Game Over Screen
    clear_screen()
    print(Fore.RED + "=== Game Over ===")
    print(f"You won {player.battles_won} battles before falling in combat.")
    highscore = load_high_score()
    if player.battles_won > highscore:
        print(Fore.YELLOW + "New High Score!")
        save_high_score(player.battles_won)
        highscore = player.battles_won
    print(f"High Score: {highscore}")
    input("Press Enter to return to the main menu...")

# ----------------------------
# High Score Functions
# ----------------------------

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# ----------------------------
# Start Game and Main Menu
# ----------------------------

def start_game(new=True):
    if new:
        game_intro()
        player = choose_character()
        # Equip default gear if none chosen
        if not player.weapon:
            player.equip_weapon(weapons[0])
        if not player.armor:
            player.equip_armor(armors[0])
    else:
        player = load_game()
        if player is None:
            return
    game_loop(player)

def main_menu():
    while True:
        clear_screen()
        highscore = load_high_score()
        print(Fore.MAGENTA + "=== Dungeon Auto Battler ===")
        print(f"Current High Score: {highscore}")
        print("1. New Game")
        print("2. Load Game")
        print("3. Options")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            start_game(new=True)
        elif choice == "2":
            start_game(new=False)
        elif choice == "3":
            options_menu()
        elif choice == "4":
            clear_screen()
            print("Goodbye, adventurer!")
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
