from unittest.mock import patch
from create_player import create_player


@patch("builtins.input", side_effect=["Al", "Aria"])
@patch("create_player.slow_print")
def test_create_player_retries_after_invalid_name(mock_slow_print, mock_input):
    player = create_player()

    assert player.name == "Aria"
    assert player.health == 100
    assert player.inventory == []
    assert mock_input.call_count == 2

    mock_slow_print.assert_any_call(
        "Name must be between 3 and 10 characters long."
    )


@patch("builtins.input", return_value="Abe")
@patch("create_player.slow_print")
def test_create_player_min_length(mock_slow_print, mock_input):
    player = create_player()

    assert player.name == "Abe"
    assert player.health == 100
    assert player.inventory == []


@patch("builtins.input", return_value="Maximilian")
@patch("create_player.slow_print")
def test_create_player_max_length(mock_slow_print, mock_input):
    player = create_player()

    assert player.name == "Maximilian"
    assert player.health == 100
    assert player.inventory == []