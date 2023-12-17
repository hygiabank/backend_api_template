import re


def is_valid_password(password: str) -> bool:

    if len(password) < 8:
        return False

    # Pelo menos uma letra minúscula
    if not re.search("[a-z]", password):
        return False

    # Pelo menos uma letra maiúscula
    if not re.search("[A-Z]", password):
        return False

    # Pelo menos um dígito
    if not re.search("[0-9]", password):
        return False

    # Pelo menos um símbolo
    if not re.search("[_@$]", password):
        return False

    return True
