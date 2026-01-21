"""This file contains utility functions that can be used throughout the project"""

import logging
import os
import configs.strings

logger = logging.getLogger(__name__)

def get_valid_input(
    prompt: str,
    cast_func=str,
    validator=None,
    error_message=configs.strings.INVALID_INPUT,
    default=None
):
    """Validate user input"""
    while True:
        full_prompt = prompt
        if default:
            full_prompt += f"[{default}] "
        user_input = input(full_prompt).strip()

        # User pressed Enter → use default
        if user_input == "":
            if default is not None:
                return default
            else:
                logger.debug(
                "invalid input received for the prompt: %s, " \
                "input: %s, " \
                "error message: %s", 
                prompt, user_input, error_message)
                print(error_message)
                continue

        try:
            value = cast_func(user_input)
        except ValueError:
            logger.debug(
                "invalid input received for the prompt: %s, " \
                "input: %s, " \
                "error message: %s", 
                prompt, user_input, error_message)
            print(error_message)
            continue

        if validator and not validator(value):
            logger.debug(
                "invalid input received for the prompt: %s," \
                " input: %s, " \
                "error message: %s", 
                prompt, user_input, error_message)
            print(error_message)
            continue

        return value

def print_table(headers, rows, max_width=20):
    """
    headers: list
    rows: list[list[Any]]
    max_width: maximum column width to avoid layout issues
    """

    if not rows:
        return

    # Convert everything to string
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = []
    for i, header in enumerate(headers):
        max_cell = max(len(row[i]) for row in str_rows)
        widths.append(min(max(len(header), max_cell), max_width))

    def truncate(text, width):
        return text if len(text) <= width else text[:width - 1] + "…"

    # Print header
    header_line = " | ".join(
        f"{truncate(h, widths[i]):<{widths[i]}}"
        for i, h in enumerate(headers)
    )
    print("-" * len(header_line))
    print(header_line)

    # Print separator
    print("-" * len(header_line))

    # Print rows
    for row in str_rows:
        print(
            " | ".join(
                f"{truncate(row[i], widths[i]):<{widths[i]}}"
                for i in range(len(headers))
            )
        )
    print("-" * len(header_line))

def draw_box(title, width=40):
    """Draw a box with a title"""
    print("\n")
    print("╔" + "═" * (width - 2) + "╗")
    title_padded = title.center(width - 2)
    print("║" + title_padded + "║")
    print("╚" + "═" * (width - 2) + "╝")
    print()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
