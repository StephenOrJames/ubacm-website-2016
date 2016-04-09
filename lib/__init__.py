import random
import string


def random_generator(size=16, chars=string.ascii_uppercase + string.digits):
    """
    Generates a random hash with characters and digits.
    :param size:  The length of the string.
    :param chars: The characters to include in the hash.
    :return: A random hash combination of the chars input and size.
    """
    return ''.join(random.choice(chars) for x in range(size))