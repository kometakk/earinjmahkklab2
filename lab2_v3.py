import copy

class Nim(object):
    def __init__(self, board):
        self.board = board

    ## Nim constants
    # Will be used to set an arbitrary-high value
    # of alphas and betas
    NIM_INF = float("inf")
    # Placeholder, when move is not yet known
    NIM_EMPTY_MOVE = (-1, -1)
    # Numeric value of winning terminal node
    NIM_WIN_VALUE = 1
    # Numeric value of losing teminal node
    NIM_LOSS_VALUE = -1

    # Implement any additional functions needed here

    # When a player or agent provies move values (pile_nr
    # and amount of sticks), this function handles taking
    # sticks form a pile, checking if move is possible + 
    # provided move values are valid and if the move
    # resulted in game over (all piles are
    # empty) by printing a message and returning 1
    # -1 -> Error
    # 0 -> Regular move done
    # 1 -> No sticks, so current player loses
    def makeAMoveWithEndHandling(self, pile_nr, sticks_amount, isPlayer) -> int:
        if(pile_nr < 0 or pile_nr >= len(game.board)):
            if(not isPlayer):
                raise Exception(f"ERROR! Problem with agent! move {pile_nr}, {sticks_amount} is invalid!")
            print("Pile with number " + str(pile_nr) + " doesn't exist, pick another")
            return -1
        if(sticks_amount < 1):
            if(not isPlayer):
                raise Exception(f"ERROR! Problem with agent! move {pile_nr}, {sticks_amount} is invalid!")
            print("You need to take at least one stick (you wanted to take " + str(sticks_amount) + ")!")
            return -1
        if(game.board[pile_nr] < sticks_amount):
            if(not isPlayer):
                raise Exception(f"ERROR! Problem with agent! move {pile_nr}, {sticks_amount} is invalid!")
            print("You can take at most " + str(game.board[pile_nr]) + " sticks from pile " + str(pile_nr) + ", while you wanted to take " + str(sticks_amount) + "!")
            return -1
        
        if not isPlayer:
            print("Agent's move: pile chosen = " + str(pile_nr + 1) + ", sticks taken =" + str(sticks_amount))
        self.board[pile_nr] -= sticks_amount
        if(sum(self.board) == 0):
            print(self.board)
            if(isPlayer):
                print("You lose")
            else:
                print("You win")
            return 1
        elif(sum(self.board) == 1):
            print(self.board)
            if(isPlayer):
                print("You win")
            else:
                print("You lose")
            return 1

        return 0
    
    # Returns the move of the agent based on the
    # current board. Basically calls the minimax() function
    def agentDecision(self):
        """
        TODO
        Temporary functionality to test ui
        
        pile_nr, sticks_amount = 0, 1
        for i in range(len(self.board)):
            if(self.board[i] > 0):
                pile_nr = i
                break
        return pile_nr, sticks_amount
        """
        ##_, next_move = self.simpleminmax(self.board, sum(self.board), True)
        ##return next_move
        _, next_move = self.minimax(self.board, sum(self.board), True, -abs(self.NIM_INF), abs(self.NIM_INF))
        return next_move


    def minimax(self, board : list[int], depth : int, maximizing_player : bool,
                alpha : int, beta : int) -> tuple[int, tuple[int, int]]:
        """
        Minimax with alpha-beta pruning algorithm

        Parameters:
        - board: 1d matrix where each entry represents pile and value in the entry represents number of sticks
        - depth: depth
        - maximizing_player: boolean which is equal to True when the player tries to maximize the score
        - alpha: alpha variable for pruning
        - beta: beta variable for pruning 
        Returns:
        - Best value 
        - Everything needed to identify next move

        """
        # Your code starts here
        if(depth == 0 or sum(board) == 0):
            if(maximizing_player):
                return self.NIM_WIN_VALUE, self.NIM_EMPTY_MOVE
            else:
                return self.NIM_LOSS_VALUE, self.NIM_EMPTY_MOVE
        elif(sum(board) == 1):
            if(maximizing_player):
                return self.NIM_LOSS_VALUE, self.NIM_EMPTY_MOVE
            else:
                return self.NIM_WIN_VALUE, self.NIM_EMPTY_MOVE

        best_move = self.NIM_EMPTY_MOVE

        if(maximizing_player):
            value = -Nim.NIM_INF
            for iter_pile_index in range(0, len(board)):
                for iter_sticks_taken_from_pile in range(1, board[iter_pile_index]+1):
                    tempBoard = copy.deepcopy(board)
                    tempBoard[iter_pile_index] = tempBoard[iter_pile_index] - iter_sticks_taken_from_pile
                    value = max(value, self.minimax(tempBoard, depth-1, False, alpha, beta)[0])
                    if(value > alpha):
                        alpha = value
                        best_move = (iter_pile_index, iter_sticks_taken_from_pile)
                    if(beta <= alpha):
                        break
        else:
            value = Nim.NIM_INF
            for iter_pile_index in range(0, len(board)):
                for iter_sticks_taken_from_pile in range(1, board[iter_pile_index]+1):
                    tempBoard = copy.deepcopy(board)
                    tempBoard[iter_pile_index] = tempBoard[iter_pile_index] - iter_sticks_taken_from_pile
                    value = min(value, self.minimax(tempBoard, depth-1, True, alpha, beta)[0])
                    if(value < beta):
                        beta = value
                        best_move = (iter_pile_index, iter_sticks_taken_from_pile)
                    if(beta <= alpha):
                        break
        return value, best_move
    

if __name__ == "__main__":

    """
    Main game loop
    Firtsly, allow player to choose how many piles will be in the game and number of sticks in each pile

    Implement the game loop
    """

    print("Starting Nim!")

    # initializing size of the game board
    ele = int(input("Input the number of piles "))
    piles = []

    print("Input the number of sticks in each pile (separate with ENTER)")
    for _ in range(ele):
        piles.append(int(input()))

    game = Nim(piles)
    print("Enter the pile to remove from (starting from 0), then space followed by enter the number of sticks to remove")
    print("The person who removes the last stick loses!")
    print("Example: to remove from 2nd pile 3 sticks , enter 2 3")

    # Initial variables for handling game loop
    hasGameEnded = False
    isPlayersTurn = True
    while hasGameEnded is False:
        print("Pile state %s" % (game.board))

        # Your code starts here
        """
        Process:
        1. Get input from user
        2. Apply the move to the board
        3. If zero sticks - current player loses, if one, current player wins
        4. Make agent do its turn
        5. Apply the move to the board
        6. [3]
        """
        # Loop for providing the next move by the player
        # or an agent. It is done like that, because checking
        # the input parameters is done in the function, that
        # also handles the move and game-over-checking.
        while(True):
            pile_nr, sticks_amount = None, None

            if(isPlayersTurn):
                user_input = input("Your move (<pile_nr> <sticks_amount>): ")
                try:
                    a = [int(x) for x in user_input.split()]
                except Exception as e:
                    print("Invalid input for the move, please try again")
                    continue
                if(len(a) != 2):
                    print("Wrong number of input parameters! Provide exactly 2 integers")
                    continue
                pile_nr, sticks_amount = a[0]-1, a[1]
            else:
                ## Agent's turn
                pile_nr, sticks_amount = game.agentDecision()

            move_result = game.makeAMoveWithEndHandling(pile_nr, sticks_amount, isPlayersTurn)

            if(move_result == -1):
                continue
            elif(move_result == 1):
                hasGameEnded = True
            # if(move_result == 0):
            break
        # After move is made for current player, switch
        # the current-turn player
        isPlayersTurn = not isPlayersTurn
    