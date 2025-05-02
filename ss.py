# Import necessary libraries
import tkinter as tk  # For creating the GUI
from tkinter import messagebox  # For displaying message boxes
import random  # For random operations (used in fallback AI move selection)

# Define the Board class to manage the game state
class Board:
    def __init__(self, rows=3, cols=3):
        """Initialize the board with rows, columns, and an empty grid."""
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.n_to_win = min(3, rows, cols)  # Number of consecutive symbols needed to win

    def place_move(self, row, col, symbol):
        """Place a move on the board if the cell is valid and empty."""
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def is_valid_move(self, row, col):
        """Check if the given move is within bounds and on an empty cell."""
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] == ' '

    def get_empty_cells(self):
        """Return all empty cells as (row, col) tuples."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] == ' ']

    def check_win(self, symbol):
        """Check if the given symbol has won the game."""
        def check_line(line):
            count = 0
            for cell in line:
                if cell == symbol:
                    count += 1
                    if count == self.n_to_win:
                        return True
                else:
                    count = 0
            return False

        for row in self.grid:
            if check_line(row):
                return True

        for col in range(self.cols):
            col_vals = [self.grid[r][col] for r in range(self.rows)]
            if check_line(col_vals):
                return True

        for r in range(self.rows - self.n_to_win + 1):
            for c in range(self.cols - self.n_to_win + 1):
                diag = [self.grid[r + i][c + i] for i in range(self.n_to_win)]
                if check_line(diag):
                    return True

        for r in range(self.rows - self.n_to_win + 1):
            for c in range(self.n_to_win - 1, self.cols):
                diag = [self.grid[r + i][c - i] for i in range(self.n_to_win)]
                if check_line(diag):
                    return True

        return False

# Define the TicTacToeGUI class for the graphical interface
class TicTacToeGUI:
    def __init__(self):
        """Initialize the GUI components."""
        self.board = Board()  # Create a new game board
        self.current_symbol = 'X'  # Player's symbol
        self.ai_symbol = 'O'  # AI's symbol
        self.player_symbol = 'X'  # Player's symbol
        self.is_human_vs_human = True  # Track mode (Human vs Human or Human vs AI)
        self.scores = {"Player 1": 0, "Player 2": 0, "AI": 0}  # Initialize scores
        self.root = tk.Tk()  # Create the root window
        self.root.title("🎮 Tic-Tac-Toe Battle")  # Set the window title
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Create a 3x3 grid of buttons
        self.build_grid()  # Build the game grid
        self.status_label = tk.Label(self.root, text="Player 1's turn (X)", font=("Arial", 18))
        self.status_label.grid(row=3, column=0, columnspan=3)  # Add the status label
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.grid(row=4, column=0, columnspan=3)  # Add the score label
        self.mode_button = tk.Button(self.root, text="Switch to Human vs AI", command=self.switch_mode, font=("Arial", 12))
        self.mode_button.grid(row=5, column=0, columnspan=3, pady=5)  # Add the mode switch button
        self.reset_board()  # Reset the board for a new game
        self.root.mainloop()  # Start the main event loop

    def build_grid(self):
        """Build the game grid with buttons."""
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.root, text='', width=8, height=4, font=("Arial", 32, "bold"),
                                bg="#0000FF",  # Blue background color for buttons
                                command=lambda row=r, col=c: self.player_move(row, col))  # Bind player move to button
                btn.grid(row=r, column=c, padx=10, pady=10)  # Place the button in the grid
                self.buttons[r][c] = btn  # Store the button reference

    def switch_mode(self):
        """Switch between Human vs Human and Human vs AI modes."""
        self.is_human_vs_human = not self.is_human_vs_human  # Toggle the mode
        mode = "Human vs Human" if self.is_human_vs_human else "Human vs AI"
        self.mode_button.config(text=f"Switch to {'Human vs AI' if self.is_human_vs_human else 'Human vs Human'}")
        self.status_label.config(text=f"{mode}: Player 1's turn (X)")
        self.reset_board()  # Reset the board when switching modes

    def player_move(self, row, col):
        """Handle the player's move."""
        if self.board.place_move(row, col, self.current_symbol):  # Place the player's move
            self.update_button(row, col)  # Update the button
            if self.check_game_over():  # Check if the game is over
                return
            if self.is_human_vs_human:  # Switch turns in Human vs Human mode
                self.current_symbol = 'O' if self.current_symbol == 'X' else 'X'
                self.status_label.config(text=f"Player {'1' if self.current_symbol == 'X' else '2'}'s turn ({self.current_symbol})")
            else:  # AI's turn in Human vs AI mode
                self.current_symbol = self.ai_symbol
                self.status_label.config(text="AI's turn (O)")
                self.root.after(500, self.ai_move)  # Delay AI move by 500ms

    def ai_move(self):
        """Handle the AI's move."""
        row, col = get_minimax_ai_move(self.board, self.ai_symbol, self.player_symbol)  # Get the AI's move
        self.board.place_move(row, col, self.current_symbol)  # Place the AI's move
        self.update_button(row, col)  # Update the button
        if self.check_game_over():  # Check if the game is over
            return
        self.current_symbol = self.player_symbol  # Switch back to the player's turn
        self.status_label.config(text="Player's turn (X)")

    def update_button(self, row, col):
        """Update the button text and color."""
        symbol = self.board.grid[row][col]  # Get the symbol (X or O) for the cell
        self.buttons[row][col].config(
            text=symbol,  # Set the text to the symbol
            fg="red",  # Set the text color to red
            state='disabled'  # Disable the button after the move
        )

    def check_game_over(self):
        """Check if the game is over."""
        if self.board.check_win(self.current_symbol):  # Check if the current player has won
            winner = "Player 1" if self.current_symbol == 'X' else ("Player 2" if self.is_human_vs_human else "AI")
            self.scores[winner] += 3  # Award 3 points for a win
            self.update_scores()  # Update the score label
            self.show_end_prompt(f"{winner} wins!")  # Show the winner
            return True
        elif not self.board.get_empty_cells():  # Check if the board is full
            # Award 2 points to both players for a tie
            self.scores["Player 1"] += 2
            if self.is_human_vs_human:
                self.scores["Player 2"] += 2
            else:
                self.scores["AI"] += 2
            self.update_scores()  # Update the score label
            self.show_end_prompt("It's a tie!")  # Show a tie message
            return True
        return False  # Return False if the game is not over

    def show_end_prompt(self, message):
        """Show the end game prompt."""
        play_again = messagebox.askyesno("Game Over", f"{message}\n\nScores:\n{self.get_score_text()}\n\nDo you want to play again?")
        if play_again:
            self.reset_board()  # Reset the board if the player wants to play again
        else:
            self.root.quit()  # Quit the game

    def reset_board(self):
        """Reset the board for a new game."""
        self.board = Board()  # Create a new board
        self.current_symbol = 'X'  # Reset the current symbol to X
        for r in range(3):  # Reset all buttons
            for c in range(3):
                self.buttons[r][c].config(text='', state='normal', bg="#0000FF")  # Reset button properties with blue background
        mode = "Player 1's turn (X)" if self.is_human_vs_human else "Player's turn (X)"
        self.status_label.config(text=mode)  # Update the status label

    def update_scores(self):
        """Update the score label."""
        self.score_label.config(text=self.get_score_text())  # Update the score label with the latest scores

    def get_score_text(self):
        """Generate the score text for the score label."""
        if self.is_human_vs_human:
            return f"Player 1: {self.scores['Player 1']}   Player 2: {self.scores['Player 2']}"
        else:
            return f"Player: {self.scores['Player 1']}   AI: {self.scores['AI']}"

# Define helper functions for AI
def evaluate(board, ai_symbol, player_symbol):
    """Evaluate the board state for the minimax algorithm."""
    if board.check_win(ai_symbol):
        return 10
    elif board.check_win(player_symbol):
        return -10
    else:
        return 0

def minimax(board, depth, is_maximizing, ai_symbol, player_symbol):
    """Recursive minimax function with depth limit."""
    score = evaluate(board, ai_symbol, player_symbol)
    if abs(score) == 10 or depth == 0 or not board.get_empty_cells():
        return score
    if is_maximizing:
        best_score = -float('inf')
        for (r, c) in board.get_empty_cells():
            board.grid[r][c] = ai_symbol
            current_score = minimax(board, depth - 1, False, ai_symbol, player_symbol)
            board.grid[r][c] = ' '
            best_score = max(best_score, current_score)
        return best_score
    else:
        best_score = float('inf')
        for (r, c) in board.get_empty_cells():
            board.grid[r][c] = player_symbol
            current_score = minimax(board, depth - 1, True, ai_symbol, player_symbol)
            board.grid[r][c] = ' '
            best_score = min(best_score, current_score)
        return best_score

def get_minimax_ai_move(board, ai_symbol='O', player_symbol='X', depth=9):
    """AI chooses the best move using minimax algorithm."""
    best_score = -float('inf')
    best_move = None
    for (r, c) in board.get_empty_cells():
        board.grid[r][c] = ai_symbol
        score = minimax(board, depth - 1, False, ai_symbol, player_symbol)
        board.grid[r][c] = ' '
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move if best_move else random.choice(board.get_empty_cells())

# Run the GUI
if __name__ == "__main__":
    TicTacToeGUI()