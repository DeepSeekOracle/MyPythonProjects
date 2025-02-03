import random
import sys
from time import sleep

class Card:
    def __init__(self, name, cost, card_type, effect):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.effect = effect

    def __repr__(self):
        return f"""
┌─────────────┐
│ {self.name:<11} │
│ Cost: {self.cost:<6} │
│ Type: {self.card_type:<6} │
└─────────────┘
""".strip()

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.health = 50
        self.armor = 0
        self.max_mana = 0
        self.mana = 0
        self.deck = deck.copy()
        self.hand = []
        self.discard = []
        self.statuses = []
        random.shuffle(self.deck)

    def draw_cards(self, num):
        for _ in range(num):
            if not self.deck:
                if not self.discard:
                    return
                self.deck = self.discard.copy()
                self.discard = []
                random.shuffle(self.deck)
            if self.deck:
                self.hand.append(self.deck.pop())

    def take_damage(self, amount):
        if self.armor > 0:
            damage_blocked = min(amount, self.armor)
            self.armor -= damage_blocked
            amount -= damage_blocked
            print(f"✨ {self.name} blocked {damage_blocked} damage with armor!")
        self.health -= amount
        print(f"💥 {self.name} takes {amount} damage! ({self.health} HP remaining)")

    def add_status(self, name, duration, effect):
        self.statuses.append({
            "name": name,
            "duration": duration,
            "effect": effect
        })
        print(f"🌀 {self.name} gains {name} ({duration} turns)")

    def process_statuses(self):
        for status in self.statuses:
            status["effect"](self)
        self.statuses = [s for s in self.statuses if s["duration"] > 1]
        for status in self.statuses:
            status["duration"] -= 1

    def start_turn(self):
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        self.armor = 0
        self.draw_cards(5)
        print(f"\n=== {self.name}'s Turn ===")
        self.display_status()

    def display_status(self):
        status_str = " | ".join([f"{s['name']}({s['duration']})" for s in self.statuses])
        print(f"\n{self.name}")
        print(f"Health: {self.health}/50 {'♥' * (self.health // 5)}")
        print(f"Mana: {'◆' * self.mana}{'◇' * (self.max_mana - self.mana)}")
        if status_str:
            print(f"Statuses: {status_str}")
        print("Hand:")
        for card in self.hand:
            print(card)

    def play_card(self, card, target):
        if card.cost > self.mana:
            return False
        self.mana -= card.cost
        print(f"\n⚡ {self.name} plays {card.name}!")
        card.effect(target, self)
        self.discard.append(card)
        self.hand.remove(card)
        return True

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play_turn(self, current_player, opponent):
        playable_cards = [c for c in current_player.hand if c.cost <= current_player.mana]
        while playable_cards:
            card = random.choice(playable_cards)
            if not current_player.play_card(card, opponent):
                break
            playable_cards = [c for c in current_player.hand if c.cost <= current_player.mana]
            sleep(1.5)

    def start_game(self):
        players = [self.player1, self.player2]
        random.shuffle(players)
        current_player, opponent = players

        while True:
            current_player.start_turn()
            self.play_turn(current_player, opponent)
            current_player.discard.extend(current_player.hand)
            current_player.hand = []
            
            print("\n🔮 Processing status effects...")
            current_player.process_statuses()
            opponent.process_statuses()
            sleep(2)
            
            if self.player1.health <= 0 or self.player2.health <= 0:
                return self.show_game_over()

            current_player, opponent = opponent, current_player

    def show_game_over(self):
        winner = self.player1 if self.player2.health <= 0 else self.player2
        print(f"\n🎉 {winner.name} wins!")
        print("""
              ___________
            '._==_==_=_.'
            .-\:      /-.
           | (|:.     |) |
            '-|:.     |-'
              \::.    /
               '::. .'
                 ) (
               _.' '._
              `\"\"\"\"\"\"\"`
        """)
        return winner.name

def show_title_screen():
    print(r"""
     _____           _     _____     _     _        
    |  __ \         | |   |  __ \   | |   | |       
    | |  \/ ___ __ _| |__ | |  \/ __| | __| | ___   
    | | __ / __/ _` | '_ \| | __/ _` |/ _` |/ _ \  
    | |_\ \ (_| (_| | |_) | |_\ \ (_| | (_| |  __/  
     \____/\___\__,_|_.__/ \____/\__,_|\__,_|\___|  
    """)
    print("1. Start New Game")
    print("2. Quit")
    while True:
        choice = input("Select option: ")
        if choice in ("1", "2"):
            return choice
        print("Invalid choice!")

# Card effects remain the same
# ...

def main():
    while True:
        choice = show_title_screen()
        if choice == "2":
            print("Thanks for playing!")
            sys.exit()
        
        # Create cards and decks
        cards = [
            Card("Strike", 1, "Attack", strike),
            Card("Block", 1, "Defense", block),
            Card("Fireball", 3, "Spell", fireball),
            Card("Poison Dart", 2, "Spell", poison_dart),
            Card("Heal", 2, "Spell", heal),
        ]
        base_deck = [random.choice(cards) for _ in range(15)]
        
        # Initialize players
        player1 = Player("Hero", base_deck)
        player2 = Player("Villain", base_deck)
        
        # Start game
        game = Game(player1, player2)
        game.start_game()
        
        # Game over menu
        print("\n1. Play Again")
        print("2. Quit")
        choice = input("Select option: ")
        if choice != "1":
            break

if __name__ == "__main__":
    main()
