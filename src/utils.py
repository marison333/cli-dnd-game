import time
import sys

if sys.platform == "win32":
    import msvcrt

    def _check_for_skip() -> bool:
        if msvcrt.kbhit():
            msvcrt.getch()
            return True
        return False

    def _sleep_or_skip(duration: float) -> bool:
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            if _check_for_skip():
                return True
            time.sleep(0.005)
        return False

else:
    import select

    def _check_for_skip() -> bool:
        ready = select.select([sys.stdin], [], [], 0)[0]
        if ready:
            sys.stdin.readline()
            return True
        return False

    def _sleep_or_skip(duration: float) -> bool:
        return bool(select.select([sys.stdin], [], [], duration)[0])


def slow_print(text: str, skippable: bool = False) -> None:
    for index, letter in enumerate(text):
        print(letter, end="", flush=True)
        if skippable and _sleep_or_skip(0.03):
            print(text[index + 1:], end="")
            break
        elif not skippable:
            time.sleep(0.03)
    print()


def ask_choice(question: str, options: list) -> str:
    while True:
        choice = input(f"\n{question} ({'/'.join(options)}): ").lower().strip()
        if choice in options:
            return choice
        print("Invalid choice, please try again.")


def print_screen(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        print(file.read())


def handle_choice(scene: dict) -> str | None:
    for line in scene.get("text", []):
        slow_print(f"\n{line}")

    if not scene.get("options"):
        return None

    choice = ask_choice(scene["question"], scene["options"])

    for line in scene["results"].get(choice, []):
        slow_print(f"\n{line}")

    return choice