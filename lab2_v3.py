class Nim(object):
    def __init__(self, board):
        self.board = board

    # Implement any additional functions needed here

    # -1 -> Error
    # 0 -> Regular move done
    # 1 -> No sticks, so current player loses
    # 2 -> Last stick left, so current player wins
    def makeAMoveWithEndHandling(self, pile_nr, sticks_amount, isPlayer):
        if(pile_nr < 0 or pile_nr >= len(game.board)):
            if(not isPlayer):
                raise "ERROR! Problem with agent!"
            print("Pile with number " + str(pile_nr) + " doesn't exist, pick another")
            return -1
        if(sticks_amount < 1):
            if(not isPlayer):
                raise "ERROR! Problem with agent!"
            print("You need to take at least one stick (you wanted to take " + str(sticks_amount) + ")!")
            return -1
        if(game.board[pile_nr] < sticks_amount):
            if(not isPlayer):
                raise "ERROR! Problem with agent!"
            print("You can take at most " + str(game.board[pile_nr]) + " sticks from pile " + str(pile_nr) + ", while you wanted to take " + str(sticks_amount) + "!")
            return -1
        
        if not isPlayer:
            print("Agent's move: pile chosen = " + str(pile_nr) + ", sticks taken =" + str(sticks_amount))
        self.board[pile_nr] -= sticks_amount
        if(sum(self.board) == 0):
            if(isPlayer):
                print("You lose")
            else:
                print("You win")
            return 1
        elif(sum(self.board) == 1):
            if(isPlayer):
                print("You win")
            else:
                print("You lose")
            return 1
        return 0
    
    def agentDecision(self):
        """
        TODO
        Temporary functionality to test ui
        """
        pile_nr, sticks_amount = 0, 1
        for i in range(len(self.board)):
            if(self.board[i] > 0):
                pile_nr = i
                break
        return pile_nr, sticks_amount

    def minimax(self, board, depth, maximizing_player, alpha, beta):
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
        while(True):
            pile_nr, sticks_amount = None, None

            if(isPlayersTurn):
                user_input = input("Your move (<pile_nr> <sticks_amount>): ")
                a = [int(x) for x in user_input.split()]
                pile_nr, sticks_amount = a[0], a[1]
            else:
                ## Agent's turn
                pile_nr, sticks_amount = game.agentDecision()

            move_result = game.makeAMoveWithEndHandling(pile_nr, sticks_amount, isPlayersTurn)

            if(move_result == -1):
                continue
            elif(move_result == 1):
                hasGameEnded = True
            break

        isPlayersTurn = not isPlayersTurn