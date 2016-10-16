import random

class TicTacToe():
    def __init__(self):
        self.board = [
                ' ', ' ', ' ',
                ' ', ' ', ' ',
                ' ', ' ', ' '
        ]
        self.combinations = (
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        )

    def print_board(self):
        board = "{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}".format(*self.board)
        print(board)

    def open_spots(self):
        open_spots = []
        for c, i in enumerate(self.board):
            if i == ' ':
                open_spots.append(c)
        return open_spots

    def mark_spot(self, player, spot):
        self.board[spot] = player

    def grab_player_marked(self, player):
        marked = []
        for c, i in enumerate(self.board):
            if i == player:
                marked.append(c)
        return marked

    def potentials(self, player):
        return self.open_spots() + self.grab_player_marked(player)

    def who_won(self):
        for player in ('x', 'o'):
            player_marks = self.grab_player_marked(player)
            for combination in self.combinations:
                won = True
                for position in combination:
                    if position not in player_marks:
                        won = False
                if won:
                    return player
        return None

    def finished(self):
        if ' ' not in self.board:
            return True
        if self.who_won() != None:
            return True
        return False

    def check_if_tied(self):
        if self.finished() and self.who_won() == None:
            return True
        return False

    def who(self, player):
        return 'o' if player == 'x' else 'x'

    def prune(self, branch, player, alpha, beta):
        if branch.finished():
            if branch.who_won() == 'o':
                return 1
            elif branch.who_won() == 'x':
                return -1
            else:
                return 0
        for move in self.open_spots():
            branch.mark_spot(player, move)
            score = self.prune(branch, self.who(player), alpha, beta)
            branch.mark_spot(' ', move)
            if player == 'o':
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return beta
            else:
                if score < beta:
                    beta = score
                if beta <= alpha:
                    return alpha
        if player == 'o':
            return alpha
        else:
            return beta

def plan(board, player):
    a = -2
    paths = []
    if len(board.open_spots()) == 9:
        return 4
    for move in board.open_spots():
        board.mark_spot(player, move)
        score = board.prune(board, board.who(player), -2, 2)
        board.mark_spot(' ', move)
        if score > a:
            a = score
            paths = [move]
        elif score == a:
            paths.append(move)
    return random.choice(paths)

if __name__ == '__main__':
    t = TicTacToe()
    t.print_board()

    while not t.finished():
        player = 'x'
        print('\n')
        your_move = int(input("Select your cell: ")) -1
        if not your_move in t.open_spots():
            continue
        t.mark_spot(player, your_move)
        t.print_board()
        print('\n')

        if t.finished():
            break

        comp = t.who(player)
        comp_move = plan(t, comp)
        t.mark_spot(comp, comp_move)
        t.print_board()
    print("Winner: {}".format(t.who_won()))
