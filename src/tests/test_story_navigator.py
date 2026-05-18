from unittest.mock import patch
from story_navigators import show_intro, TITLE_SCREEN


@patch("story_navigators.print_screen")
@patch("story_navigators.slow_print")
def test_show_intro(mock_slow_print, mock_print_screen):
    show_intro()

    mock_print_screen.assert_called_once_with(TITLE_SCREEN)

    mock_slow_print.assert_called_once_with(
        "\nWelcome to Valoria, the capital of this Kingdom.\n"
    )