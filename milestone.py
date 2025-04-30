
#Names: Acquah Yaw, Cephas Asamoah, Blake Bothmer
import random  # Import the random module for AI move selection

class Board:
    def __init__(self, rows=4, cols=4):
        """Represents a dynamic Tic-Tac-Toe board for any rows × columns."""
        self.rows = rows  # Number of rows in the board
        self.cols = cols  # Number of columns in the board
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]  # Initialize the board as a grid of empty spaces
        self.n_to_win = min(4, rows, cols)  # Number of consecutive symbols needed to win

    def display(self):
        """Displays the board with column numbers and row labels."""
        print("    " + "   ".join(str(c) for c in range(self.cols)))  # Print column numbers
        print("  +" + "---+" * self.cols)  # Print the top border of the board
        for r in range(self.rows):  # Loop through each row
            row_str = " | ".join(self.grid[r])  # Join the row elements with vertical bars
            print(f"{r} | {row_str} |")  # Print the row with its label
            print("  +" + "---+" * self.cols)  # Print the row separator

    def place_move(self, row, col, symbol):
        """Place a move if the cell is valid and empty."""
        if self.is_valid_move(row, col):  # Check if the move is valid
            self.grid[row][col] = symbol  # Place the symbol in the specified cell
            return True  # Return True if the move was successful
        return False  # Return False if the move was invalid

    def is_valid_move(self, row, col):
        """Check if the given move is within bounds and on an empty cell."""
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == ' '  # Ensure the cell is within bounds and empty

    def get_empty_cells(self):
        """Return all empty cells as (row, col) tuples."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] == ' ']  # Find all empty cells

    def check_win(self, symbol):
        """Check if the given symbol has won the game."""

        def check_line(line):
            count = 0  # Initialize a counter for consecutive symbols
            for cell in line:  # Loop through each cell in the line
                if cell == symbol:  # Check if the cell matches the symbol
                    count += 1  # Increment the counter
                    if count == self.n_to_win:  # Check if the required number of symbols is reached
                        return True  # Return True if the player has won
                else:
                    count = 0  # Reset the counter if the cell does not match
            return False  # Return False if no winning line is found

        for row in self.grid:  # Check each row for a win
            if check_line(row):
                return True

        for col in range(self.cols):  # Check each column for a win
            col_vals = [self.grid[r][col] for r in range(self.rows)]  # Extract the column values
            if check_line(col_vals):
                return True

        for r in range(self.rows - self.n_to_win + 1):  # Check diagonals (top-left to bottom-right)
            for c in range(self.cols - self.n_to_win + 1):
                diag = [self.grid[r + i][c + i] for i in range(self.n_to_win)]  # Extract diagonal values
                if check_line(diag):
                    return True

        for r in range(self.rows - self.n_to_win + 1):  # Check diagonals (top-right to bottom-left)
            for c in range(self.n_to_win - 1, self.cols):
                diag = [self.grid[r + i][c - i] for i in range(self.n_to_win)]  # Extract diagonal values
                if check_line(diag):
                    return True

        return False  # Return False if no win is detected


def get_player_move(board):
    """Ask the player to enter a valid move."""
    while True:  # Keep prompting until a valid move is entered
        try:
            move = input("Enter your move as 'row,col': ").strip()  # Get the player's input
            row, col = map(int, move.split(','))  # Parse the input into row and column
            if board.is_valid_move(row, col):  # Check if the move is valid
                return row, col  # Return the move
            else:
                print("❌ That cell is already taken or out of bounds.")  # Inform the player of an invalid move
        except (ValueError, IndexError):  # Handle invalid input
            print("⚠️ Please enter row and column as two numbers, like: 1,2")  # Prompt the player to try again


# --- BEGINNER-FRIENDLY MINIMAX SECTION ---

def evaluate(board, ai_symbol, player_symbol):
    """Score the board: +10 for AI win, -10 for player win, 0 otherwise."""
    if board.check_win(ai_symbol):  # Check if the AI has won
        return 10  # Return a positive score for an AI win
    elif board.check_win(player_symbol):  # Check if the player has won
        return -10  # Return a negative score for a player win
    else:
        return 0  # Return 0 if no one has won


def minimax(board, depth, is_maximizing, ai_symbol, player_symbol):
    """Recursive minimax function with depth limit."""
    score = evaluate(board, ai_symbol, player_symbol)  # Evaluate the board

    if abs(score) == 10 or depth == 0 or not board.get_empty_cells():  # Stop if game is over or depth limit is reached
        return score  # Return the score

    if is_maximizing:  # If it's the AI's turn
        best_score = -float('inf')  # Initialize the best score to negative infinity
        for (r, c) in board.get_empty_cells():  # Loop through all empty cells
            board.grid[r][c] = ai_symbol  # Try the move
            current_score = minimax(board, depth - 1, False, ai_symbol, player_symbol)  # Recursively evaluate
            board.grid[r][c] = ' '  # Undo the move
            best_score = max(best_score, current_score)  # Update the best score
        return best_score  # Return the best score
    else:  # If it's the player's turn
        best_score = float('inf')  # Initialize the best score to positive infinity
        for (r, c) in board.get_empty_cells():  # Loop through all empty cells
            board.grid[r][c] = player_symbol  # Try the move
            current_score = minimax(board, depth - 1, True, ai_symbol, player_symbol)  # Recursively evaluate
            board.grid[r][c] = ' '  # Undo the move
            best_score = min(best_score, current_score)  # Update the best score
        return best_score  # Return the best score


def get_minimax_ai_move(board, ai_symbol='O', player_symbol='X', depth=2):
    """AI chooses the best move using minimax algorithm."""
    best_score = -float('inf')  # Initialize the best score to negative infinity
    best_move = None  # Initialize the best move

    for (r, c) in board.get_empty_cells():  # Loop through all empty cells
        board.grid[r][c] = ai_symbol  # Try the move
        score = minimax(board, depth - 1, False, ai_symbol, player_symbol)  # Evaluate the move
        board.grid[r][c] = ' '  # Undo the move
        if score > best_score:  # Update the best move if the score is better
            best_score = score
            best_move = (r, c)

    return best_move if best_move else random.choice(board.get_empty_cells())  # Fallback to random move if no best move

# --- END MINIMAX SECTION ---


def play_one_round(scores):
    board = Board(3, 3)  # Create a 3x3 board
    current_symbol = 'X'  # Player's symbol
    ai_symbol = 'O'  # AI's symbol
    
    
   

    print(f"🎮 Welcome to {board.rows}x{board.cols} Tic-Tac-Toe! Get {board.n_to_win}-in-a-row to win.")  # Welcome message
    print("You are X. The AI is O.\n")  # Inform the player of their symbol
    board.display()  # Display the initial board

    while True:  # Game loop
        if current_symbol == 'X':  # If it's the player's turn
            row, col = get_player_move(board)  # Get the player's move
        else:  # If it's the AI's turn
            row, col = get_minimax_ai_move(board, ai_symbol, 'X', depth=9)  # Get the AI's move with depth=9
            print(f"🤖 AI chooses: {row},{col}")  # Inform the player of the AI's move

        board.place_move(row, col, current_symbol)  # Place the move on the board
        board.display()  # Display the updated board

        if board.check_win(current_symbol):  # Check if the current player has won
            if current_symbol == 'X':  # If the player has won
                print("🎉 You win! Congrats!")  # Congratulate the player
                scores['Player']+=3
            else:  # If the AI has won
                print("💀 AI wins! Better luck next time.")  # Inform the player of their loss
                scores['AI']+=3
            break  # End the game

        if not board.get_empty_cells():  # Check if the board is full
            print("Game Over – it's a tie! 😐")  # Inform the player of a tie
            scores['Player']+=1
            scores['AI']+=1
            break  # End the game
        
        
        current_symbol = 'O' if current_symbol == 'X' else 'X'  # Switch turns
    print(f"\nScores => Player: {scores["Player"]}, AI: {scores["AI"]}")

def main():
    scores ={'Player':0, 'AI':0}
    while True:
        play_one_round(scores)
        response = input("\n🔁 Do you want to play again? (yes/no): ").strip().lower()
        if response != 'yes':
            print("👋 Thanks for playing! Final scores:")
            print(f"Player: {scores['Player']} | AI: {scores['AI']}")
            break

if __name__ == "__main__":
    main()  # Start the game

