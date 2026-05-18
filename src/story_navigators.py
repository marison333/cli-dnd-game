import json
import os
from entities import monster
from utils import slow_print, print_screen, handle_choice
from core.game_state import create_game_state
from core.game_state import trigger_event
from create_player import create_player

TITLE_SCREEN = 'assets/title.txt'
BASE_DIRECTORY = os.path.dirname(__file__)
STORY_PATH = os.path.join(BASE_DIRECTORY, 'story.json')


def load_story():
    with open(STORY_PATH, 'r') as file:
        return json.load(file)


def show_intro():
    print_screen(TITLE_SCREEN)
    slow_print("\nWelcome to Valoria, the capital of this Kingdom.\n")


def play_story(story: dict, game_state: dict) -> bool | None:
    current_scene = story["start"]

    while current_scene:
        scene = story[current_scene]
        choice = handle_choice(scene)

        if not scene.get("options"):
           if scene.get("monster"):
                game_state['active_monster'] = monster.Monster(
                    name=scene["monster"]["name"], 
                    health=scene["monster"]["health"], 
                    loot=scene["monster"]["loot"]
                )
                trigger_event(game_state)
            
                if game_state['player'].health <= 0:
                    return False
           
           next_scene = scene.get("next")
           current_scene = next_scene if next_scene else None
           continue

        if "next" not in scene or not scene["next"]:
            return 

        current_scene = scene["next"].get(choice)

    return False


if __name__ =="__main__":
    story = load_story()
    player = create_player()
    game_state = create_game_state(player)
    play_story(story, game_state)