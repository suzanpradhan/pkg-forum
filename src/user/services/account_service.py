import random
import string


def generate_random_password(length):
    """
    Generate random passsword
    """
    letters = string.printable
    return "".join(random.choice(letters) for _ in range(length))
