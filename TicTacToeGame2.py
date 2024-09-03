# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 15:29:00 2024

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:32:32 2024

@author: User
"""
# Import tkinter for creating the GUI
import tkinter as tk

# Import NumPy for array handling
import numpy as np

# Import random for generating random computer moves
import random

# Function to create an empty Tic-Tac-Toe board
def create_board():
    return np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

# Function to find all available spaces on the board
def possibilities(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == 0]

# Function for the computer to place its mark based on the selected difficulty
def computer_move(board, player, level):
    if level == "easy":
        return random_place(board, player)
    elif level == "normal":
        for move in possibilities(board):
            board_copy = board.copy()
            board_copy[move] = player
            if evaluate(board_copy) == player:
                board[move] = player
                return board
        return random_place(board, player)
    elif level == "hard":
        for move in possibilities(board):
            board_copy = board.copy()
            board_copy[move] = player
            if evaluate(board_copy) == player:
                board[move] = player
                return board
        opponent = 1 if player == 2 else 2
        for move in possibilities(board):
            board_copy = board.copy()
            board_copy[move] = opponent
            if evaluate(board_copy) == opponent:
                board[move] = player
                return board
        return random_place(board, player)

# Function to randomly place the computer's mark on the board
def random_place(board, player):
    selection = possibilities(board)
    if selection:
        current_loc = random.choice(selection)
        board[current_loc] = player
        return board
    return None

# Function to check if a player has won by filling a row
def row_win(board, player):
    return any(np.all(row == player) for row in board)

# Function to check if a player has won by filling a column
def col_win(board, player):
    return any(np.all(col == player) for col in board.T)

# Function to check if a player has won by filling a diagonal
def diag_win(board, player):
    return np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player)

# Function to evaluate if there's a winner or if the game is a tie
def evaluate(board):
    for player in [1, 2]:
        if row_win(board, player) or col_win(board, player) or diag_win(board, player):
            return player
    if np.all(board != 0):
        return -1
    return 0

# Function to handle the player's move
def player_move(row, col):
    global board, difficulty_level
    if board[row, col] == 0:
        board[row, col] = 1
        buttons[row][col].config(text="X", state=tk.DISABLED)
        winner = evaluate(board)
        if winner == 0:
            board = computer_move(board, 2, difficulty_level)
            update_buttons()
            winner = evaluate(board)
        if winner != 0:
            end_game(winner)

# Function to update the buttons after each move
def update_buttons():
    for i in range(3):
        for j in range(3):
            if board[i, j] == 2:
                buttons[i][j].config(text="O", state=tk.DISABLED)

# Function to end the game and display the result
def end_game(winner):
    if winner == 1:
        result_label.config(text="You Win!")
    elif winner == 2:
        result_label.config(text="Computer Wins!")
    else:
        result_label.config(text="It's a Tie!")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

# Function to restart the game
def restart_game():
    global board
    board = create_board()
    update_buttons()
    result_label.config(text="")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.NORMAL, text="")

# Function to set the difficulty level
def set_difficulty(level):
    global difficulty_level
    difficulty_level = level
    restart_game()

# Initialize the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Initialize the board and difficulty level
board = create_board()
difficulty_level = "easy"

# Set the window size and center it
window_width = 550
window_height = 880
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Set the background color of the window
root.configure(bg='purple')

# Add a title label
title_label = tk.Label(root, text="Tic-Tac-Toe Game", font=('Times New Roman', 24), bg='white')
title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

# Create buttons for the 3x3 grid with a new style
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=('Times New Roman', 40), width=5, height=2,
                                  bg='white', fg='black', 
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i+1, column=j, padx=10, pady=10)

# Label to display the result
result_label = tk.Label(root, text="", font=('Times New Roman', 20), bg='purple', fg='darkblue')
result_label.grid(row=4, column=0, columnspan=3, pady=(10, 20))

# Create radio buttons for difficulty levels
difficulty_var = tk.StringVar(value="easy")
tk.Radiobutton(root, text="LEVEL1", variable=difficulty_var, value="easy", command=lambda: set_difficulty("easy"),
               bg='white', font=('Times New Roman', 12)).grid(row=5, column=0)
tk.Radiobutton(root, text="LEVEL2", variable=difficulty_var, value="normal", command=lambda: set_difficulty("normal"),
               bg='white', font=('Times New Roman', 12)).grid(row=5, column=1)
tk.Radiobutton(root, text="LEVEL3", variable=difficulty_var, value="hard", command=lambda: set_difficulty("hard"),
               bg='white', font=('Times New Roman', 12)).grid(row=5, column=2)

# Create restart button with new style
restart_button = tk.Button(root, text="Restart", command=restart_game, bg='red', fg='white', font=('normal', 16))
restart_button.grid(row=6, column=0, columnspan=3, pady=(10, 20))

# Start the main loop
root.mainloop()
