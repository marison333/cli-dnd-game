from entities.player import Player
from utils import slow_print


def create_player():
    while True:
        slow_print("Hero, what is your name?") 
        name = input("> ").strip()
        if 3 <= len(name) <= 10:
            return Player(name, 100, [])
        
        slow_print("Name must be between 3 and 10 characters long.")


if __name__ == "__main__":
    player = create_player()
    print(f"Welcome, {player.name}! Your adventure begins now.")