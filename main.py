import json
import secrets
import string
import urllib.request

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
    """"""

    _sec_level = 3

    def fetch_words():
        """"""
        _api_url = "https://random-word-api.herokuapp.com/word?number=3&length=6"
        try:
            with urllib.request.urlopen(_api_url) as response:
                if response.getcode() != 200:
                    raise Exception(f"Got an invalid response from API: {response.get_code()}")
                resp_data = json.loads(response.read().decode("utf-8"))
                print(f"here is data: {resp_data}")
                response.close()
        except urllib.error.URLError as e:
            print(f"An error occurred: {e.reason}")
            return None
        return resp_data

    def _misspell(char_list):
        """
            Misspell a word to further increase security.  Replace a random character from the char_list with a random
            letter.

        :param list[str] char_list:
        :return: List of characters where one letter has been randomly replaced with a different randomly chosen letter.
        :rtype: list[str]
        """
        _valid_characters = string.ascii_lowercase
        _misspell_list = deepcopy(char_list)
        replacement_index = 0
        while not replacement_index:
            _replacement = secrets.randbelow(len(_misspell_list))
            if _misspell_list[_replacement] not in _valid_characters:
                continue

            _replacement_instances = [idx for idx, val in enumerate(_misspell_list) if val == _misspell_list[_replacement]]
            replacement_index = secrets.choice(_replacement_instances)

        replacement_character = ""
        while not replacement_character:
            _replacement_character_candidate = secrets.choice(_valid_characters)
            if _replacement_character_candidate == _misspell_list[replacement_index]:
                continue
            replacement_character = _replacement_character_candidate

        _misspell_list[replacement_index] = replacement_character

        return _misspell_list

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

    password = ""
    while not password:
        _sep = secrets.choice(seperators)
        _words = fetch_words()
        _words_raw = deepcopy([x.lower() for x in _words])
        _words_combined = _sep.join(_words_raw)
        _char_list = list(_words_combined)

        # Replace random character w/ an integer
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

        # "misspell" a word to further increase security
        if _sec_level == 3:
            _char_list = _misspell(_char_list)

        # Capitalize random letter to ensure it meets general required password parameters
        random_capitalization = ""
        while not random_capitalization:
            random_capitalization = secrets.randbelow(len(_char_list))
            if _char_list[random_capitalization] in seperators:
                random_capitalization = ""
                continue
            if _char_list[random_capitalization] in special_char_replacement_map.values():
                random_capitalization = ""
                continue
            if _char_list[random_capitalization] in int_replacement_map.values():
                random_capitalization = ""
                continue

            _char_list[random_capitalization] = _char_list[random_capitalization].upper()

        # Concat the final password together
        password = "".join(_char_list)

    return password

if __name__ == "__main__":
    generated_password = generate_password()
    print(f"Generated Password:\n\t{generated_password}")
    exit(0)