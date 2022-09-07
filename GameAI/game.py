import random
import copy
import math
import numpy

""" This class implements the game TeekoPlayer
"""
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.count = 0
        
    def succ(self, state):
        occur_list = []
        successor_list = [] #this list contains list of before piece, after_piece, and new_state_board with after piece
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    occur_list.append((i,j))    ## add all of the occurrence of my_piece of state to list
        
        ## when there is no piece on the board
        if len(occur_list) == 0:
            [row, col] = [random.randint(0, 4), random.randint(0, 4)]
            
            while state[row][col] != ' ':  ## check if there is an opponent there 
                    [row, col] = [random.randint(0, 4), random.randint(0, 4)]
                    
            before_piece = ()
            after_piece = (row, col)
            new_state_board = copy.deepcopy(state)
            row = [row, col][0]
            col = [row, col][1]
            new_state_board[row][col] = self.my_piece ## add piece to the update new_state_board
            successor_list.append([before_piece, after_piece, new_state_board])
            
         ## when still in dropping phrase
        elif len(occur_list) > 0 and len(occur_list) < 4:
            for item in occur_list:  ## check each piece on the board
                row = item[0]
                col = item[1]
                
                all_moves = [[row+1, col], [row-1, col], [row, col+1], [row, col-1], [row+1, col+1],
                             [row-1, col+1], [row+1, col-1], [row-1, col-1]] ## moves that can win the game
                
                for move in all_moves:
                    ## check if they are stay in the range of 4 * 4 board
                    if 0 <= move[0] and move[0] <= 4 and 0 <= move[1] and move[1] <= 4:
                        if  state[move[0]][move[1]] == ' ':
                            new_state_board = copy.deepcopy(state)
                            new_state_board[move[0]][move[1]] = self.my_piece
                            before_piece = (row, col)
                            after_piece = (move[0], move[1])
                            successor_list.append([before_piece, after_piece, new_state_board])
        ## when after dropping phrase
        else:
            for item in occur_list:  ## check each piece on the board
                row = item[0]
                col = item[1]
                
                all_moves = [[row+1, col], [row-1, col], [row, col+1], [row, col-1], [row+1, col+1],
                             [row-1, col+1], [row+1, col-1], [row-1, col-1]]## moves that can win the game
                
                for move in all_moves:
                    ## check if they are stay in the range of 4 * 4 board
                    if 0 <= move[0] and move[0] <= 4 and 0 <= move[1] and move[1] <= 4:
                        if state[move[0]][move[1]] == ' ':
                            new_state_board = copy.deepcopy(state)
                            new_state_board[move[0]][move[1]] = self.my_piece
                            ## delete the piece before
                            new_state_board[row][col] = ' '
                            before_piece = (row, col)
                            after_piece = (move[0], move[1])
                            successor_list.append([before_piece, after_piece, new_state_board])
        return successor_list


    

    
    def heuristic_game_value(self, state):
        new_state_board = copy.deepcopy(state)  # create a new_board

        if self.game_value(new_state_board) != 0:  ## check if the game win or not
            return self.game_value(new_state_board)

        piece_occur_list = [] 
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                     piece_occur_list.append((i,j))
        total = len(piece_occur_list)
        # calculate distance center of my_piece
        center_row = sum([p[0] for p in piece_occur_list]) / (total + 2) # in case when there is no piece on the board
        center_col = sum([p[1] for p in piece_occur_list]) / (total + 2)
        # calculate the distance of my pieces
        distance_my_piece = sum([(p[0]- center_row )**2 for p in piece_occur_list]) + sum([(p[1]- center_col)**2 for p in piece_occur_list])

        new_piece_occur_list = []
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.opp:
                     new_piece_occur_list.append((i,j))
        total_opp = len(new_piece_occur_list)
        center_row = sum([p[0] for p in new_piece_occur_list]) / (total_opp + 2)
        center_col = sum([p[1] for p in new_piece_occur_list]) / (total_opp + 2)
        distance_opp = sum([(p[0]-center_row)**2 for p in new_piece_occur_list]) + sum([(p[1]-center_col)**2 for p in new_piece_occur_list])
        
        #print(total, total_opp)
        
        ## make the result between -1 and 1
        heuristic_value = float(1 / (999 + distance_my_piece)) - float(1 / (999 + distance_opp))
        return heuristic_value


    
    
    def max_value(self, state, depth):
        successors = self.succ(state) # get successors
        for (before_piece, after_piece, new_state_board) in successors:
            if self.heuristic_game_value(new_state_board) == 1: ##reach to terminal state, my piece is winning
                alpha = 1
                return before_piece, after_piece, alpha ## terminal state and alpha is 1

        if depth > 1:
            before_piece_temp = None
            after_piece_temp = None
            alpha = float('-inf')
            for (before_piece, after_piece, new_state_board) in successors:
                if self.heuristic_game_value(new_state_board) > alpha:
                    before_piece_temp = before_piece
                    after_piece_temp = after_piece
                    new_state_board = new_state_board
                    alpha = self.heuristic_game_value(new_state_board)
            return before_piece_temp, after_piece_temp, alpha

        alpha = float('-inf')
        after_temp = None
        state_temp = None
         # get beta from min_value()
        for (before_piece, after_piece, new_state_board) in successors:
            current_state, next_state, beta = self.min_value(new_state_board, depth + 1)
            if beta > alpha: #if beta greater than alpha, update the state and new alpha
                alpha = beta
                after_temp = before_piece
                state_temp = after_piece
        #print(alpha)
        return after_temp, state_temp, alpha

   
    def min_value(self, state, depth):
        successors = self.succ(state) # get successors
        for (before_piece, after_piece, new_state_board) in successors:
            if self.heuristic_game_value(new_state_board) == -1: ##reach to terminal state, opponate is winning
                beta = -1
                return before_piece, after_piece, beta ## terminal state and beta is -1


        if depth > 1:
            before_piece_temp = None
            after_piece_temp = None
            beta = float('inf')
            for (before_piece, after_piece, new_state_board) in successors:
                if self.heuristic_game_value(new_state_board) < beta:
                    before_piece_temp = before_piece
                    after_piece_temp = after_piece
                    new_state_board = new_state_board
                    beta = self.heuristic_game_value(new_state_board)
            return before_piece_temp, after_piece_temp, beta
            
        
        
        after_temp = None
        state_temp = None
        beta = float('inf')
        for (before_piece, after_piece, new_state_board) in successors:
            current_state, next_state, alpha = self.max_value(new_state_board, depth + 1)
            if alpha < beta:  
                beta = alpha 
                after_temp = before_piece
                state_temp = after_piece
        #print(beta)
        return after_temp, state_temp, beta

    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True   # TODO: detect drop phase
        move = []  #a list of move tuples such that its format is [(row, col), (source_row, source_col)]
        
        piece_occur_list = []  # track piece_occurrence
        
        new_state_board = copy.deepcopy(state) #create a new state board
        
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                     piece_occur_list.append((i,j))  
        ##print(piece_occur_list)
                    
                    
        
        if len(piece_occur_list) == 4:
            drop_phase = False  
        
         
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            before_piece, after_piece, board = self.max_value(new_state_board, 0)
            move.append(after_piece) 
            move.append(before_piece)  
            return move

        # TODO: implement a minimax algorithm to play better
        before_piece, after_piece, board = self.max_value(new_state_board, 0)
        move.insert(0, (after_piece[0], after_piece[1]))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
         # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
                
         # TODO: check \ diagonal wins
        
        for row in range(2):
            for col in range(2, 4):
                if state[row][col+1] != ' ':
                    if state[row][col+1] == state[row+1][col] and state[row][col+1] == state[row+2][col-1] and state[row][col+1]== state[row+3][col-2]:
                        return 1 if state[row][col] == self.my_piece else -1

        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ':
                    if state[row][col] == state[row+1][col+1] and state[row][col] == state[row+2][col+2] and state[row][col] == state[row+3][col+3]:
                        return 1 if state[row][col] == self.my_piece else -1
               
                
        # TODO: check box wins
        
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ':
                    ##check if it is a square
                    if state[row][col] == state[row][col+1] and state[row][col]== state[row+1][col] and state[row][col] == state[row+1][col+1]:
                        return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet
    
############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

