import json
import os
from random import choice
from entities import monster
from utils import slow_print, print_screen, handle_choice
from core.game_state import create_game_state
from core.game_state import trigger_event
from create_player import create_player

TITLE_SCREEN: str = 'assets/title.txt'
BASE_DIRECTORY: str = os.path.dirname(__file__)
STORY_PATH: str = os.path.join(BASE_DIRECTORY, 'story.json')


def load_story() -> dict:
    MANIFEST_PATH: str = os.path.join(BASE_DIRECTORY, "story", "manifest.json")
    with open(MANIFEST_PATH) as file:
        manifest = json.load(file)

    scenes: dict = {"start": manifest["start"]}
    story_directory = os.path.dirname(MANIFEST_PATH)

    for relative_path in manifest["files"]:
        file_path = os.path.join(story_directory, relative_path)
        with open(file_path) as file:
            scenes.update(json.load(file))

    return scenes


def show_intro():
    print_screen(TITLE_SCREEN)
    slow_print("\nWelcome to Valoria, the capital of this Kingdom.\n")


def validate_story(scene: dict):
    # @TODO: check that the story is well-formed
    # every scene has a type
    # every next value either points to an existing scene ID or is null
    # every choice scene has questions, options, and results keys
    # every combat scene has a monster key with name, health, and loot
    pass

def play_story(story: dict, game_state: dict) -> bool | None:
    current_scene = story["start"]

    while current_scene:
        scene = story[current_scene]
        scene_type = scene["type"]

        if scene_type == "combat":
            game_state['active_monster'] = monster.Monster(
                    name=scene["monster"]["name"], 
                    health=scene["monster"]["health"], 
                    loot=scene["monster"]["loot"]
                )
            trigger_event(game_state)
            current_scene = scene.get("next")

        elif scene_type == "choice":
            choice = handle_choice(scene)
            next_scene_map = scene.get("next") or {}
            current_scene = next_scene_map.get(choice)

        elif scene_type == "linear":
            handle_choice(scene)
            current_scene = scene.get("next")
            
        else:
            raise ValueError(f"Unknown scene type: {scene_type} in scene {current_scene}")

    return False


if __name__ =="__main__":
    story = load_story()
    player = create_player()
    game_state = create_game_state(player)
    play_story(story, game_state)