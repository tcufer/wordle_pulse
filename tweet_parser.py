import re

PUZZLE_ID = r"\d{1,3}"
ATTEMPTS  = r"(?:[1-6]\/6|X\/6)"
HEADER    = rf"Wordle\s{PUZZLE_ID}\s{ATTEMPTS}"

WHITE     = r"\u2b1c"
DARK      = r"\u2b1b"
EMPTY     = rf"({WHITE}|{DARK})"

YELLOW    = r"\ud83d\udfe8"
GREEN     = r"\ud83d\udfe9"
SQUARE    = rf"({EMPTY}|{YELLOW}|{GREEN})"
ROW       = rf"{SQUARE}{SQUARE}{SQUARE}{SQUARE}{SQUARE}"


class TweetParser():

    def __init__(self, *args):
        self.text = args[0]

    def _number_of_attempts(self, text):
        m = re.findall(r"(.)/6", text)[0]
        if m == 'x':
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

    def wordle_result_exist(self):  # better like a function that returns true/false?
        num_of_attempts = 0
        m = re.match(HEADER, self.text)
        if m is None:
            return False

        num_of_attempts = self._number_of_attempts(m[0])
        grid = rf"{ROW}\n"*num_of_attempts
        grid = grid[:-2] + ''
        m = re.search(grid, self.text)
        if m is None:
            return False
        else:
            self._parse_attempts(m.group(0))
            print("Grid found:" + str(self._parse_attempts(m.group(0))))

        full_result = rf"{HEADER}\n\n{grid}"
        m = re.search(full_result, self.text)
        if m is None:
            return False

        return True


# def __main__():
tweet_msg = "Wordle 231 4/6\n\n\u2b1c\ud83d\udfe8\u2b1c\u2b1c\u2b1c\n\u2b1c\u2b1c\ud83d\udfe9\u2b1c\u2b1c\n\ud83d\udfe8\ud83d\udfe9\ud83d\udfe9\ud83d\udfe8\ud83d\udfe9\n\ud83d\udfe9\ud83d\udfe9\ud83d\udfe9\ud83d\udfe9\ud83d\udfe9"
TweetParser(tweet_msg).wordle_result_exist()
