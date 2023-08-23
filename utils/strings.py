def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0

# print(is_positive_number('10'))
# print(is_positive_number('-5'))
# print(is_positive_number('a'))
# print(is_positive_number('10b'))