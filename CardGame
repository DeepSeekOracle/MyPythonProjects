import random
from random import shuffle
from time import sleep

class Card:
    def __init__(self, name, cost, card_type, effect):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.effect = effect

    def __repr__(self):
        return f"{self.name} ({self.cost} Mana)"

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
        shuffle(self.deck)

    def draw_cards(self, num):
        for _ in range(num):
            if not self.deck:
                if not self.discard:
                    return
                self.deck = self.discard.copy()
                self.discard = []
                shuffle(self.deck)
            if self.deck:
                self.hand.append(self.deck.pop())

    def take_damage(self, amount):
        if self.armor > 0:
            damage_blocked = min(amount, self.armor)
            self.armor -= damage_blocked
            amount -= damage_blocked
            print(f"{self.name} blocked {damage_blocked} damage with armor!")
        self.health -= amount
        print(f"{self.name} takes {amount} damage! ({self.health} HP remaining)")

    def add_status(self, name, duration, effect):
        self.statuses.append({
            "name": name,
            "duration": duration,
            "effect": effect
        })
        print(f"{self.name} gains {name} ({duration} turns)")

    def process_statuses(self):
        for status in self.statuses:
            status["effect"](self)
        self.statuses = [s for s in self.statuses if s["duration"] > 1]
        for status in self.statuses:
            status["duration"] -= 1

    def start_turn(self):
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        self.armor = 0  # Reset armor each turn
        self.draw_cards(5)
        print(f"\n{self.name}'s turn begins!")
        print(f"Mana: {self.mana}/{self.max_mana}")
        print(f"Hand: {self.hand}")

    def play_card(self, card, target):
        if card.cost > self.mana:
            return False
        self.mana -= card.cost
        print(f"\n{self.name} plays {card.name}!")
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
            card = random.choice(playable_cards)  # Simple AI: Random card selection
            if not current_player.play_card(card, opponent):
                break
            playable_cards = [c for c in current_player.hand if c.cost <= current_player.mana]
            sleep(1)

    def start_game(self):
        players = [self.player1, self.player2]
        random.shuffle(players)
        current_player, opponent = players

        while True:
            current_player.start_turn()
            self.play_turn(current_player, opponent)
            current_player.discard.extend(current_player.hand)
            current_player.hand = []
            
            # Process status effects
            print("\nProcessing status effects...")
            current_player.process_statuses()
            opponent.process_statuses()
            sleep(1)
            
            # Check win conditions
            if self.player1.health <= 0:
                print(f"\n{self.player2.name} wins!")
                return
            if self.player2.health <= 0:
                print(f"\n{self.player1.name} wins!")
                return
            
            current_player, opponent = opponent, current_player

# Card effects
def strike(target, caster):
    target.take_damage(6)

def block(target, caster):
    caster.armor += 8
    print(f"{caster.name} gains 8 armor!")

def fireball(target, caster):
    target.take_damage(12)
    target.add_status("Burn", 3, lambda t: t.take_damage(3))

def poison_dart(target, caster):
    target.add_status("Poison", 4, lambda t: t.take_damage(2))

def heal(target, caster):
    caster.health = min(caster.health + 10, 50)
    print(f"{caster.name} heals 10 HP!")

# Create cards
cards = [
    Card("Strike", 1, "Attack", strike),
    Card("Block", 1, "Defense", block),
    Card("Fireball", 3, "Spell", fireball),
    Card("Poison Dart", 2, "Spell", poison_dart),
    Card("Heal", 2, "Spell", heal),
]

# Create decks
base_deck = [random.choice(cards) for _ in range(15)]  # Random starter decks

# Initialize players
player1 = Player("Player 1", base_deck)
player2 = Player("Player 2", base_deck)

# Start game
game = Game(player1, player2)
game.start_game()
