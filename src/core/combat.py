import time
import random
from utils import slow_print, print_screen, ask_choice
from entities.player import Player
from entities.monster import Monster

hit_threshold = 10 # 50% chance for a succesfull attack
hit_threshold_flee = 0 # if player is trying to flee, monster has a guaranteed hit
flee_threshold = 15 # 30% chance to flee successfully

CLEAR_SCREEN = "\033[H\033[J"
DEATH_SCREEN = 'assets/death_screen.txt'


def print_status(player, monster) -> None:
    max_player_health = player.max_health
    max_monster_health = monster.max_health

    print("\n" + "=" * 40)
    print(f"  {player.name:<20} HP: {player.health if player.health > 0 else 0}/{max_player_health}")
    print(f"  {monster.name:<20} HP: {monster.health if monster.health > 0 else 0}/{max_monster_health}")
    print("=" * 40)

    
def print_action(message) -> None:
    slow_print(f">> {message}")


def roll_dice(sides=20) -> int:
    return random.randint(1, sides)


def resolve_attacker(attacker, defender, is_player_fleeing=False):
    attack_roll = roll_dice(20)
    crit = attack_roll == 20
    fumble = attack_roll == 1

    if fumble:
        print_action(f"{attacker.name} fumbles and does not land an attack!")
        return False

    if is_player_fleeing:
        if attack_roll >= hit_threshold_flee or crit:
            base_damage = random.randint(5, 15)
            damage = base_damage * 2 if crit else base_damage
            defender.take_damage(damage)

            if crit:
                print_action(f"Critical hit! {attacker.name} slams {defender.name} for {damage} damage.\n\n")
            else:
                print_action(f"{attacker.name} hits {defender.name} for {damage} damage.")
            return True
        else:
            print_action(f"{attacker.name} misses {defender.name} (rolls {attack_roll}, need at least {hit_threshold_flee}).")
            time.sleep(2)
            return False
        
    elif not is_player_fleeing:
        if attack_roll >= hit_threshold or crit:
            base_damage = random.randint(5, 15)
            damage = base_damage * 2 if crit else base_damage
            defender.take_damage(damage)

            if crit:
                print_action(f"Critical hit! {attacker.name} slams {defender.name} for {damage} damage.\n\n")
            else:
                print_action(f"{attacker.name} hits {defender.name} for {damage} damage.")
            return True
        else:
            print_action(f"{attacker.name} misses {defender.name} (rolls {attack_roll}, need at least {hit_threshold}).")
            time.sleep(2)
            return False
    

def attempt_flee(player, monster) -> bool:
    flee_roll = roll_dice(20)
    
    if flee_roll >= flee_threshold:
        print(CLEAR_SCREEN, end="")
        print_action(f"{player.name} successfully flees from {monster.name}!")
        time.sleep(2)
        return True
    else:
        print(CLEAR_SCREEN, end="")
        print_action(f"{player.name} attempts to flee but fails (rolls {flee_roll}, need at least {flee_threshold}).")
        print_action(f"{monster.name} takes advantage of the opening!")
        time.sleep(2)
        resolve_attacker(monster, player, is_player_fleeing=True)

    return False


def fight(player, monster) -> str:
    slow_print("Combat starts!")
    fled = False

    while player.health > 0 and monster.health > 0:
        time.sleep(2)
        print(CLEAR_SCREEN, end="")
        print_status(player, monster,)
        action = ask_choice("Choose your action:", ["Attack", "Flee"]).lower()

        if action == "flee":
            fled = attempt_flee(player, monster)
            if fled:
                break
            if player.health <= 0:
                print(CLEAR_SCREEN, end="")
                print_action(f"{player.name} has fallen in battle!")
                time.sleep(2)
                break
            continue

        resolve_attacker(player, monster)
        if monster.health <= 0:
            print(CLEAR_SCREEN, end="")
            print_action(f"{monster.name} has been defeated!")
            time.sleep(2)
            break

        resolve_attacker(monster, player)
        if player.health <= 0:
            print(CLEAR_SCREEN, end="")
            print_action(f"{player.name} has fallen in battle!")
            time.sleep(2)
            break

    print_status(player, monster)

    if player.health > 0 and monster.health <= 0:
        print(CLEAR_SCREEN, end="")
        print_action(f"{player.name} win the fight!")

        heal_amount = int(player.max_health * 0.3)
        player.health = min(player.health + heal_amount, player.max_health)
        print_action(f"{player.name} recovers {heal_amount} HP!")

        time.sleep(2)
        fight_result = "won"

    elif fled:
        print(CLEAR_SCREEN, end="")
        print_action(f"{player.name} escapes from the fight!")
        time.sleep(2)
        fight_result = "fled"

    else:
        print(CLEAR_SCREEN, end="")
        print_screen(DEATH_SCREEN)
        time.sleep(2.5)
        print_action(f"{monster.name} has killed you!")
        time.sleep(2)
        fight_result = "lost"

    return fight_result


if __name__ == "__main__":
    fight(Player("Hero", 100, []), Monster("Monster", 50, ["Ancient Bone Sword"]))
