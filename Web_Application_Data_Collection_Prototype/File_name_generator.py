import random
import string


def file_name_generator(length: int) -> str:
    """
    Generate a random string to act as a unique file name.
    A combination of lower and upper case letters.
    Attaches '.wav' to end of generated string
    :param length: length of string to be generated
    :return: concatenation of generated string and '.wav'
    """

    # Get all ASCII letters
    letters = string.ascii_letters

    # Initialise an empty string
    random_string = ''

    # Concatenate random choice from letters
    for i in range(length):
        random_string += ''.join(random.choice(letters))

    # Concatenate '.wav' to random_string
    random_string += '.wav'

    return random_string
