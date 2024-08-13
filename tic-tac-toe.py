import math


class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3 : (i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind * 3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def minimax(state, player):
    max_player = "X"
    other_player = "O" if player == "X" else "X"

    if state.current_winner == other_player:
        return {
            "position": None,
            "score": (
                1 * (state.num_empty_squares() + 1)
                if other_player == max_player
                else -1 * (state.num_empty_squares() + 1)
            ),
        }

    elif not state.empty_squares():
        return {"position": None, "score": 0}

    if player == max_player:
        best = {"position": None, "score": -math.inf}
    else:
        best = {"position": None, "score": math.inf}

    for possible_move in state.available_moves():
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player)

        state.board[possible_move] = " "
        state.current_winner = None
        sim_score["position"] = possible_move

        if player == max_player:
            if sim_score["score"] > best["score"]:
                best = sim_score
        else:
            if sim_score["score"] < best["score"]:
                best = sim_score

    return best


def play_game():
    t = TicTacToe()
    t.print_board_nums()

    letter = "X"
    while t.empty_squares():
        if letter == "O":
            square = minimax(t, letter)["position"]
        else:
            square = int(input(f"{letter}'s turn. Input move (0-8): "))

        if t.make_move(square, letter):
            print(f"{letter} makes a move to square {square}")
            t.print_board()
            print("")

            if t.current_winner:
                print(letter + " wins!")
                return

            letter = "O" if letter == "X" else "X"

        if not t.empty_squares():
            print("It's a tie!")


play_game()
