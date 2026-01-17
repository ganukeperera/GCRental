"""This file contains utility functions that can be used throughout the project"""

import logging
import configs.strings

logger = logging.getLogger(__name__)

def get_valid_input(
    prompt: str,
    cast_func=str,
    validator=None,
    error_message=configs.strings.INVALID_INPUT
):
    """Validate user input"""
    while True:
        user_input = input(prompt)

        try:
            value = cast_func(user_input)
        except ValueError:
            # print("Invalid data type.")
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
