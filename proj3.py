"""
File:    proj3.py
Author:  Nicholas Perry
Date:    11/26/2019
Section: 25
E-mail:  nperry2@umbc.edu
Description: This is a scoring program for the game go. The program prompts the user for the file that is wanted
to be opened and then it outputs the score to a file. The program prints "Done" when finished.
"""

# The pieces going to be on any given board
EMPTY_PIECE = '+'
X_PIECE = 'X'
O_PIECE = 'O'


def read_file_to_2D_list(file_name):
    """
    reads a file and returns a 2D list of the elements
    :param file_name: the file being read
    :return: 2D list of each char in the file
    """
    with open(file_name, "r") as file_in:
        lines = file_in.read()
        section = lines.split()
        temp = []
        final = []
        for i in range(len(section)):
            for j in range(len(section[i])):
                temp.append(section[i][j])
            final.append(temp)
            temp = []
    return final


def recursive_filler(marking_board, partial_board, x, y):
    """
    recursively finds whos point is on the board
    :param marking_board: a board the same length dimensions as partial board
    :param partial_board: a board being used to find the coordinates piece type
    :param x: x-position of the point being found
    :param y: y-position of the point being found
    :return: whos point is in the board
    """

    # looks left
    if x != 0 and partial_board[y][x - 1] != EMPTY_PIECE:
        return partial_board[y][x - 1]
    # looks right
    elif x != len(partial_board[y]) - 1 and partial_board[y][x + 1] != EMPTY_PIECE:
        return partial_board[y][x + 1]
    # looks up
    elif y != 0 and partial_board[y - 1][x] != EMPTY_PIECE:
        return partial_board[y - 1][x]
    # looks down
    elif y != len(partial_board) and partial_board[y + 1][x] != EMPTY_PIECE:
        return partial_board[y + 1][x]
    else:
        marking_board[y][x] = 1
        # recursive left
        if x != 0 and marking_board[y][x - 1] != 1:
            return recursive_filler(marking_board, partial_board, (x - 1), y)
        # recursive right
        elif x != (len(partial_board[y]) - 1) and marking_board[y][x + 1] != 1:
            return recursive_filler(marking_board, partial_board, (x + 1), y)
        # recursive up
        elif y != 0 and marking_board[y - 1][x] != 1:
            return recursive_filler(marking_board, partial_board, x, (y - 1))
        # recursive down
        elif y != len(partial_board) and marking_board[y + 1][x] != 1:
            return recursive_filler(marking_board, partial_board, x, (y + 1))


def return_filled_board(incomplete_board):
    """
    runs a loop that checks to see if all the pieces have been filled in.
    if not, it will be filled with the correct piece
    :param incomplete_board: the board being completed
    :return: the new complete board
    """
    mark_board = []
    for i in range(len(incomplete_board)):
        temp_list = []
        for j in range(len(incomplete_board[i])):
            temp_list.append(0)
        mark_board.append(temp_list)

    for i in range(len(incomplete_board)):
        for j in range(len(incomplete_board[i])):
            if incomplete_board[i][j] == EMPTY_PIECE:
                incomplete_board[i][j] = recursive_filler(mark_board, incomplete_board, j, i)

    return incomplete_board


def find_points(selected_piece, board):
    """
    loops through and counts how many pieces are in a 2D list
    :param selected_piece: the character being counted
    :param board: a 2D list
    :return: total number of pieces
    """
    num = 0

    for i in range(len(board)):
        for j in range(len((board[i]))):
            if selected_piece == board[i][j]:
                num += 1

    return num


def append_board_and_points(file_name, incomplete_board, complete_board, black_score, white_score):
    """
    opens, appends and saves the new board and points to the file
    :param incomplete_board: the original game board
    :param file_name: the file name
    :param complete_board: the complete board
    :param black_score: the black (X) pieces end score
    :param white_score: the white (O) pieces end score
    :return: nothing
    """
    with open(file_name, "w") as file_out:
        file_out.write("We are scoring this board\n")
        for i in range(len(incomplete_board)):
            for j in range(len(incomplete_board[i])):
                file_out.write("%s" % incomplete_board[i][j])
            file_out.write("\n")

        file_out.write("\nHere is the colored board:\n")
        for i in range(len(complete_board)):
            for j in range(len(complete_board[i])):
                file_out.write("%s" % complete_board[i][j])
            file_out.write("\n")
        file_out.write("Black scored: %d\n" % black_score)
        file_out.write("White scored: %d" % white_score)
    print("Done")


if __name__ == "__main__":
    file = input("What is the file name?")
    mixed_board = read_file_to_2D_list(file)
    mixed_copy = []

    for i in range(len(mixed_board)):
        mixed_temp = []
        for j in range(len(mixed_board[i])):
            mixed_temp.append(mixed_board[i][j])
        mixed_copy.append(mixed_temp)

    filled_board = return_filled_board(mixed_board)

    x_points = find_points(X_PIECE, filled_board)
    o_points = find_points(O_PIECE, filled_board)

    append_board_and_points(file, mixed_copy, filled_board, x_points, o_points)
