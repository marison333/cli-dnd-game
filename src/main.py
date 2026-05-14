from core.combat import fight
from story_navigators import load_story, show_intro, play_story
from create_player import create_player
from core.game_state import consume_event, create_game_state
from utils import slow_print


def start():
    story = load_story()

    show_intro()
    player = create_player()
    game_state = create_game_state(player)

    play_story(story, game_state)
    event = consume_event(game_state)
    if event:
        slow_print(f"\nA {game_state['active_monster']} appears!")
        fight(game_state["player"], game_state["active_monster"])
    else:
        slow_print("\nYour adventure ends here. Thanks for playing!")


if __name__ == "__main__":
    start()