from unittest.mock import patch
from create_player import create_player


@patch("builtins.input", return_value="Aria")
@patch("create_player.slow_print")
def test_create_player(mock_slow_print, mock_input):
    player = create_player()

    assert player.name == "Aria"