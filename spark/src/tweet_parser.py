import re
import json

PUZZLE_ID = r"\d{1,3}"
ATTEMPTS  = r"(?:[1-6]\/6|X\/6)"
HEADER    = rf"Wordle\s{PUZZLE_ID}\s{ATTEMPTS}"

WHITE     = r"⬜"
DARK      = r"⬛"
EMPTY     = rf"({WHITE}|{DARK})"

YELLOW    = r"🟨"
GREEN     = r"🟩"
SQUARE    = rf"({EMPTY}|{YELLOW}|{GREEN})"
ROW       = rf"{SQUARE}{SQUARE}{SQUARE}{SQUARE}{SQUARE}"


class TweetParser():

    def __init__(self, *args):
        self.text = args[0]

    def _number_of_attempts(self, text):
        m = re.findall(r"(.)/6", text)[0]
        if m == 'X':
            return 6
        else:
            return int(m)

    def _parse_attempts(self, grid):
        replacements = [
            (EMPTY, '0'),
            (YELLOW, '1'),
            (GREEN, '2')
        ]
        normalised_grid = []

        for char, number in replacements:
            grid = re.sub(char, number, grid)

        grid = grid.split()
        for row in grid:
            normalised_grid.append(list(row))

        # returns nested list [['0', '1', '0', '0', '0'], ['0', '0', '2', '0', '0'],..]
        return normalised_grid

    def prepare_result(self, result, num_of_attempts, puzzle_id):
        result_dict = {}
        result_dict["attempts_count"] = num_of_attempts
        result_dict["wordle_id"] = puzzle_id
        result_dict["attempts"] = {}
        for i, row in enumerate(result, start=1):
            result_dict["attempts"][i] = row

        return json.dumps(result_dict)

    def wordle_result_exist(self):  # better like a function that returns true/false?
        attempts_arr = []
        num_of_attempts = 0
        m = re.search(HEADER, self.text)
        if m is None:
            return json.dumps({})

        num_of_attempts = self._number_of_attempts(m[0])
        puzzle_id = re.search(PUZZLE_ID, m[0])[0]
        grid = rf"{ROW}\n"*num_of_attempts
        grid = grid[:-2] + ''
        m = re.search(grid, self.text)
        if m is None:
            return json.dumps({})
        else:
            attempts_arr = self._parse_attempts(m.group(0))

        full_result = rf"{HEADER}\n\n{grid}"
        m = re.search(full_result, self.text)
        if m is None:
            return json.dumps({})

        return self.prepare_result(attempts_arr, num_of_attempts, puzzle_id)
