import secrets

from copy import deepcopy

seperators = [" ", "_", "-"]

int_replacement_map = {
    "e": "3",
    "b": "6",
    "l": "1",
    "o": "0",
    "s": "5",
    "g": "9"
}

special_char_replacement_map = {
    "a": "@",
    "l": "!",
    "g": "&",
    "s": "$",
    "c": "<",
    "n": "~",
    "t": "+"
}
def generate_password():
    print("Hello Password Generator!")

    # Get user input for security level 1-3
    print("Welcome to The Password Generator!")
    print("Please choose a security level from the options below:")
    print("\t 1: Basic Password (default)")
    print("\t 2: Basic Safety Password")
    print("\t 3: Super Secure Password")
    choice = input("Enter your desired level of password security now!\n\t-->")

    choice = "1" if choice == "" else choice
    safety_net = 1
    while choice not in ["1", "2", "3"] and safety_net <= 3:
        safety_net += 1
        print(f"Please enter a valid choice....{3 - safety_net} chances before defaulting to Basic Password")
        choice = input("Enter your desired level of password security now!\n\t-->")

    if safety_net == 3:
        print("Defaulting to Basic Password")
        choice = 1

    _sec_level = int(choice)

    # TODO:  Fetch words from API
    def fetch_words():
        """"""
        return ["ball", "Four", "test"]

    def _replace_char(char_list, replacement_map):
        """
            Choose a random character from char_list that has a valid replacement present in the replacement_map, and
            then replace a random instance of that character with the chosen replacement character.

        :param list[str] char_list: List of characters to choose a replacement character from.
        :param dict replacement_map: Dictionary of replacement characters and valid replacements.
        :return: List of characters where one instance from the input char_list is replaced with a value from the input
        replacement_map.
        :rtype: list[str]
        """
        _replacement_list = deepcopy(char_list)
        _replaceable = []
        for _char in _replacement_list:
            if _char in replacement_map.keys() and _char not in _replaceable:
                _replaceable.append(_char)

        _replacement_char = secrets.choice(_replaceable)
        _replacement_instances = [idx for idx, val in enumerate(_replacement_list) if val == _replacement_char]
        _replacement_index = secrets.choice(_replacement_instances)

        _replacement_list[_replacement_index] = replacement_map[_replacement_char]
        return _replacement_list

    # TODO:  Misspell one word in order to introduce security

    password = ""
    while not password:
        _sep = secrets.choice(seperators)
        _words = fetch_words()
        _words_raw = deepcopy([x.lower() for x in _words])
        _words_combined = _sep.join(_words_raw)
        _char_list = list(_words_combined)
        _raw_pass = _replace_char(_char_list, int_replacement_map)
        if _raw_pass == _char_list:
            continue
        _char_list = _raw_pass

        # Replace random character w/ a special character
        if _sec_level >= 2:
            _raw_lvl_2 = _replace_char(_char_list, special_char_replacement_map)
            if _raw_lvl_2 == _char_list:
                continue
            _char_list = _raw_lvl_2

        # Concat the final password together
        password = "".join(_char_list)

    return password

if __name__ == "__main__":
    generated_password = generate_password()
    print(f"Generated Password:\n\t{generated_password}")
    exit(0)