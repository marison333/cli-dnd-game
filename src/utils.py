import time


def slow_print(text):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(0.03)
    print()


def ask_choice(question, options):
    print(f"\n{question}")
    for index, option in enumerate(options, start=1):
        print(f"    {index}. {option}")

    valid_numbers = {str(index) for index in range(1, len(options) + 1)}
    valid_words = {option.lower() for option in options}
    hint = ", ".join(
        f"{index} or {option}"
        for index, option in enumerate(options, start=1)
    )

    while True:
        raw = input(f"\n({hint})\n> ").strip().lower()

        if raw in valid_numbers:
            return options[int(raw) - 1]

        if raw in valid_words:
            return next(option for option in options if option.lower() == raw)

        print(f"Invalid choice. Please enter {hint}.")


def print_screen(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        print(file.read())


def handle_choice(scene):
    for line in scene.get("text", []):
        slow_print(f"\n{line}")

    if not scene.get("options"):
        return None

    choice = ask_choice(scene["question"], scene["options"])

    for line in scene["results"].get(choice, []):
        slow_print(f"\n{line}")

    return choice