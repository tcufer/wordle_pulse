MAP_TO_SQUARE = {'0': '⬜', '1': '🟨', '2': '🟩'}


def parse_wordle_result(data):
    '''
    Transforms wordle result to grid of emoticons
    '''

    row_numbers = ['1', '2', '3', '4', '5', '6']
    row = data
    new_row = []
    for row_num in row_numbers:
        if row_num in row:
            row_in_squares = list(map(lambda x: MAP_TO_SQUARE[x], row[row_num]))
            row_in_squares = "".join(map(str, row_in_squares))
            new_row.append(row_in_squares)
    return "   \n   ".join(new_row)
