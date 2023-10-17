import math

# Constants for representing players
EMPTY = 0
AI = 1
HUMAN = -1

def print_board(board):
    symbols = [' ', 'X', 'O']
    for row in board:
        print(" | ".join([symbols[p] for p in row]))
        print("-" * 9)

def evaluate(board):
    # Check rows, columns, and diagonals for a win
    for player in [AI, HUMAN]:
        for i in range(3):
            # Rows and columns
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return player
        # Diagonals
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2 - i] == player for i in range(3)):
            return player
    return EMPTY  # No winner, it's a tie

def minimax(board, depth, maximizing_player, alpha, beta):
    result = evaluate(board)

    if result != EMPTY:
        return result

    if maximizing_player:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = None
    alpha = -math.inf
    beta = math.inf

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False, alpha, beta)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

def main():
    board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player_move = input("Enter your move (row, col) as two space-separated integers: ")
        row, col = map(int, player_move.split())
        if board[row][col] == EMPTY:
            board[row][col] = HUMAN
        else:
            print("Invalid move! Try again.")
            continue

        print_board(board)

        if evaluate(board) == HUMAN:
            print("You win!")
            break

        if all(all(cell != EMPTY for cell in row) for row in board):
            print("It's a tie!")
            break

        ai_move = best_move(board)
        board[ai_move[0]][ai_move[1]] = AI
        print("AI's move:")
        print_board(board)

        if evaluate(board) == AI:
            print("AI wins!")
            break

if __name__ == "__main__":
    main()
