import random

class TicTacToe():
    def __init__(self):
        self.board = ['.' for i in range(9)]
        self.combinations = (
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        )
        self.human = 'x'
        self.computer = 'o'

    def print_board(self):
        board = "{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}\n".format(*self.board)
        print(board)

    def open_spots(self):
        """
        Returns all currently non-marked spots on the board
        """
        open_spots = []
        for c, i in enumerate(self.board):
            if i == '.':
                open_spots.append(c)
        return open_spots

    def mark_spot(self, player, spot):
        self.board[spot] = player

    def grab_player_marked(self, player):
        """
        Iterate over the board and return those marked by the
        given player
        """
        marked = []
        for c, i in enumerate(self.board):
            if i == player:
                marked.append(c)
        return marked

    def who_won(self):
        """
        Iterate over the game winning combinations and determine
        if the marks made by the player match up with any of
        the combinations.

        If a player has been found to have won, return the player.
        Else, return none.
        """

        for player in (self.human, self.computer):
            player_marks = self.grab_player_marked(player)
            for combination in self.combinations:
                won = True
                for position in combination:
                    if position not in player_marks:
                        won = False
                if won:
                    self.winner = player
                    return player
        self.winner = None
        return None

    def finished(self):
        """
        If there are no more empty spots or if 'who_won()'
        returns something other than None, the game is over.
        """
        if '.' not in self.board or self.who_won() != None:
            return True
        return False

    def who(self, player):
        return self.computer if player == self.human else self.human

    def ab_minmax(self, branch, player, alpha, beta):
        """
        Main logic for the minmax algorithm.

        First check the base case to determine if the game is finished.
        Depending on the result of the game, return a value signifying
        the result of that particular branch. The higher number signifies
        the computer will ultimately end up winning whereas the negative
        is a human win.

        If passes the base case, dive into iterating over all available
        spots and gathering the score.

        Since the computer is the entity for whom we want to maximize its
        score, and thus win, we return the beta value whenever alpha is greater
        than or equal to its beta, and the inverse is true in regards to when
        the player is a person; we want them to lose.
        """
        if branch.finished():
            if branch.who_won() == self.computer:
                return 100
            elif branch.who_won() == self.human:
                return -100
            else:
                return 0
        for move in self.open_spots():
            branch.mark_spot(player, move)
            score = self.ab_minmax(branch, self.who(player), alpha, beta)
            branch.mark_spot('.', move)
            if player == self.computer: # maximize
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return beta
            elif player == self.human: # minimize
                if score < beta:
                    beta = score
                if beta <= alpha:
                    return alpha
        if player == self.computer:
            return alpha
        else:
            return beta

    def get_best_step(self, board, player):
        """
        Determine the best score given the available spaces
        and randomly select a step from the ones collected.
        """
        a = -100
        paths = []
        for move in board.open_spots():
            board.mark_spot(player, move)
            score = board.ab_minmax(board, board.who(player), -100, 100)
            board.mark_spot('.', move)
            if score > a:
                a = score
                paths = [move]
            elif score == a:
                paths.append(move)
        return paths[random.randint(0, len(paths) - 1)]

if __name__ == '__main__':
    t = TicTacToe()
    t.print_board()

    while not t.finished():
        your_move = int(input("Select your cell (1->9): ")) -1
        if not your_move in t.open_spots():
            continue
        t.mark_spot(t.human, your_move)
        t.print_board()

        if t.finished():
            break

        comp_move = t.get_best_step(t, t.computer)
        t.mark_spot(t.computer, comp_move)
        t.print_board()
    print("Winner: {}".format(t.who_won()))
