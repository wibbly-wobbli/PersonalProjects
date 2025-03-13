import tkinter as tk
import random

class BattleshipGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Battleship Game")
        self.board_size = 5
        self.buttons = []
        self.ship_row, self.ship_col = self.place_ship()
        self.turns = 0
        self.high_score = None  # No high score initially
        self.first_guess = True  # Track if it's the first guess
        self.max_turns = 15  # Default to Easy difficulty

        # Set the window size and position it in the center
        self.master.geometry("400x600")
        self.center_window()

        # Set a background color for the window
        self.master.config(bg="#87CEEB")

        # Create difficulty selection
        self.create_difficulty_selector()

        # Configure grid rows and columns to expand
        for i in range(self.board_size):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def center_window(self):
        """Center the window on the screen"""
        window_width = 400
        window_height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        self.master.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    def create_difficulty_selector(self):
        """Create the difficulty selector window"""
        self.difficulty_label = tk.Label(self.master, text="Select Difficulty", font=('Helvetica', 14), bg="#87CEEB")
        self.difficulty_label.pack(pady=20)

        self.easy_button = tk.Button(self.master, text="Baby (20 turns)", font=('Helvetica', 12), command=lambda: self.set_difficulty(20))
        self.easy_button.pack(pady=5)

        self.medium_button = tk.Button(self.master, text="Easy (15 turns)", font=('Helvetica', 12), command=lambda: self.set_difficulty(15))
        self.medium_button.pack(pady=5)

        self.hard_button = tk.Button(self.master, text="Medium (10 turns)", font=('Helvetica', 12), command=lambda: self.set_difficulty(10))
        self.hard_button.pack(pady=5)

        self.expert_button = tk.Button(self.master, text="Hard (5 turns)", font=('Helvetica', 12), command=lambda: self.set_difficulty(5))
        self.expert_button.pack(pady=5)

        self.expert_button = tk.Button(self.master, text="God (1 turn)", font=('Helvetica', 12), command=lambda: self.set_difficulty(5))
        self.expert_button.pack(pady=5)

    def set_difficulty(self, max_turns):
        """Set the difficulty and start the game"""
        self.max_turns = max_turns
        self.difficulty_label.pack_forget()  # Hide the difficulty selector
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.hard_button.pack_forget()
        self.expert_button.pack_forget()

        # Initialize game elements
        self.create_grid()

        # Create status label for game messages
        self.status_label = tk.Label(self.master, text="Welcome to Battleship!", font=('Helvetica', 12), bg="#87CEEB")
        self.status_label.grid(row=self.board_size, column=0, columnspan=self.board_size, pady=10)

        # Display high score
        self.high_score_label = tk.Label(self.master, text="High Score: None", font=('Helvetica', 12), bg="#87CEEB")
        self.high_score_label.grid(row=self.board_size + 1, column=0, columnspan=self.board_size, pady=5)

        # Restart and Close buttons
        self.restart_button = tk.Button(self.master, text="Restart", font=('Helvetica', 12), command=self.restart_game, state=tk.DISABLED)
        self.restart_button.grid(row=self.board_size + 2, column=0, columnspan=2, pady=10)

        self.close_button = tk.Button(self.master, text="Close", font=('Helvetica', 12), command=self.master.quit)
        self.close_button.grid(row=self.board_size + 2, column=2, columnspan=2, pady=10)

    def create_grid(self):
        """Create the game grid of buttons"""
        self.buttons = []
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                button = tk.Button(self.master, text="~", width=6, height=3, font=('Helvetica', 12),
                                   relief="solid", bd=2, command=lambda r=row, c=col: self.make_guess(r, c),
                                   bg="#B0E0E6")
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                button_row.append(button)
            self.buttons.append(button_row)

        # Place the ship at a random location for the game
        self.ship_row, self.ship_col = self.place_ship()

    def place_ship(self):
        """Place the ship at a random location"""
        ship_row = random.randint(0, self.board_size - 1)
        ship_col = random.randint(0, self.board_size - 1)
        return ship_row, ship_col

    def make_guess(self, row, col):
        """Process a player's guess"""
        self.turns += 1

        # Check if the guess is correct
        if (row == self.ship_row) and (col == self.ship_col):
            self.buttons[row][col].config(text="HIT", bg="red", fg="white")
            self.status_label.config(text=f"Congratulations! You've hit the ship in {self.turns} turns!")
            self.update_high_score()
            self.enable_restart()

            # Check if it's the first guess and show the secret message
            if self.turns <= self.max_turns:
                self.show_secret_message()
        else:
            self.buttons[row][col].config(text="MISS", bg="lightblue", fg="white")

    def show_secret_message(self):
        """Show the secret message in a note-style popup"""
        secret_message = tk.Toplevel(self.master)
        secret_message.title("Secret Message")

        # Create a text widget for the message with a scrollbar
        text_area = tk.Text(secret_message, height=10, width=40, wrap=tk.WORD, font=('Helvetica', 12))
        text_area.pack(padx=20, pady=20)

        # Insert the message into the text area
        message = "Hey Dad.\n\nYou are the best dad ever! I love you so much.\n\nThank you for being there for me always.\n\nI want you to know that I am so grateful for everything you have done for me.\n\n As well as everything you continue to do."
        text_area.insert(tk.END, message)

        # Make the text area read-only
        text_area.config(state=tk.DISABLED)

        # Create a button to close the popup
        button = tk.Button(secret_message, text="Close", command=secret_message.destroy, font=('Helvetica', 12))
        button.pack(pady=10)

    def update_high_score(self):
        """Update the high score if the player wins in fewer turns"""
        if self.high_score is None or self.turns < self.high_score:
            self.high_score = self.turns
            self.high_score_label.config(text=f"High Score: {self.high_score} turns")

    def enable_restart(self):
        """Enable the restart button after the game is over"""
        self.restart_button.config(state=tk.NORMAL)

    def restart_game(self):
        """Restart the game with a new ship and reset the board"""
        # Reset all buttons
        for row in self.buttons:
            for button in row:
                button.config(text="~", bg="#B0E0E6", fg="black")

        # Reset the game variables
        self.ship_row, self.ship_col = self.place_ship()
        self.turns = 0
        self.status_label.config(text="Game Restarted! Good luck!")
        self.restart_button.config(state=tk.DISABLED)

    def close_game(self):
        """Close the game"""
        self.master.quit()

# Create the main window
root = tk.Tk()
game = BattleshipGame(root)

# Start the game
root.mainloop()
