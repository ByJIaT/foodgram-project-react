def is_digit(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
