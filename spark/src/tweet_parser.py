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
        attempts = re.findall(r"(.)/6", text)[0]
        if attempts == 'X':
            return 6
        else:
            return int(attempts)

    def _parse_attempts(self, grid):
        replacements = [
            (EMPTY, '0'),
            (YELLOW, '1'),
            (GREEN, '2')
        ]
        numericized_grid = []

        for char, number in replacements:
            grid = re.sub(char, number, grid)

        grid = grid.split()
        [numericized_grid.append(list(map(int, row))) for row in grid]

        return numericized_grid

    def prepare_result(self, result, num_of_attempts, puzzle_id):
        result_dict = {}
        result_dict["attempts_count"] = num_of_attempts
        result_dict["wordle_id"] = puzzle_id
        result_dict["attempts"] = {}
        for i, row in enumerate(result, start=1):
            result_dict["attempts"][i] = row

        return json.dumps(result_dict)

    def perform(self):
        header_text = re.search(HEADER, self.text)
        if header_text is None:
            return json.dumps({})

        num_of_attempts = self._number_of_attempts(header_text[0])
        puzzle_id = re.search(PUZZLE_ID, header_text[0])[0]
        grid_regex = rf"{ROW}\n"*num_of_attempts
        grid_regex = grid_regex[:-2] + ''
        grid = re.search(grid_regex, self.text)
        if grid is None:
            return json.dumps({})

        attempts_arr = self._parse_attempts(grid.group(0))
        full_result_regex = rf"{HEADER}\n\n{grid_regex}"
        full_result = re.search(full_result_regex, self.text)
        if full_result is None:
            return json.dumps({})

        return self.prepare_result(attempts_arr, num_of_attempts, puzzle_id)
