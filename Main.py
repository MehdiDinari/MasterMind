import tkinter as tk
import random

Colors = ['R', 'G', 'B', 'Y', 'C', 'W', 'Black', 'White', 'O', 'P']
Color_Names = {
    'R': 'red',
    'G': 'green',
    'B': 'blue',
    'Y': 'yellow',
    'C': 'cyan',
    'W': 'white',
    'Black': 'black',
    'White': 'white',
    'O': 'orange',
    'P': 'purple'
}
Tries = 10
Code_length = 4

class MastermindGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Mastermind Game")
        self.master.geometry("600x800")
        self.master.configure(bg='#222')

        self.secret_code = self.code_generator()
        self.attempts = 0
        self.previous_guesses = []

        self.create_widgets()

    def code_generator(self):
        return [random.choice(Colors) for _ in range(Code_length)]

    def create_widgets(self):
        tk.Label(self.master, text="Mastermind - Devinez le code !",
                 bg='#222', fg='white', font=("Arial", 16, "bold")).pack(pady=10)

        # Couleurs disponibles
        self.color_frame = tk.Frame(self.master, bg='#333', bd=3, relief="ridge")
        self.color_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(self.color_frame, text="Couleurs disponibles :", bg='#333', fg='white', font=("Arial", 12)).pack()

        self.color_buttons = []
        for color in Colors:
            button = tk.Button(self.color_frame, bg=Color_Names[color], width=4,
                               command=lambda c=color: self.add_color(c))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.color_buttons.append(button)

        self.current_guess_display = tk.Frame(self.master, bg='#444', bd=3, relief="ridge")
        self.current_guess_display.pack(pady=10)
        tk.Label(self.current_guess_display, text="Votre essai :", bg='#444', fg='white', font=("Arial", 12)).pack()

        self.guess_canvas = tk.Canvas(self.current_guess_display, width=220, height=50, bg='#555')
        self.guess_canvas.pack(pady=5)

        self.feedback_label = tk.Label(self.master, text=f"Essais restants : {Tries}",
                                       bg='#222', fg='white', font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        self.submit_button = tk.Button(self.master, text="Valider l'essai", command=self.submit_guess,
                                       font=("Arial", 12, "bold"), bg='green', fg='white')
        self.submit_button.pack(pady=10)

        self.history_frame = tk.Frame(self.master, bg='#111', bd=3, relief="ridge")
        self.history_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        tk.Label(self.history_frame, text="Historique des essais", bg='#111', fg='white', font=("Arial", 12, "bold")).pack(pady=5)

        self.history_canvas = tk.Canvas(self.history_frame, width=500, height=300, bg='#222')
        self.history_canvas.pack(pady=5)

        self.history_scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history_canvas.yview)
        self.history_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)
        self.history_inner_frame = tk.Frame(self.history_canvas, bg='#222')
        self.history_canvas.create_window((0, 0), window=self.history_inner_frame, anchor="nw")

        self.reset_button = tk.Button(self.master, text="Réinitialiser", command=self.reset_game,
                                      font=("Arial", 12, "bold"), bg='red', fg='white')
        self.reset_button.pack(pady=10)

        self.current_guess = []

    def add_color(self, color):
        if len(self.current_guess) < Code_length:
            self.current_guess.append(color)
            self.update_guess_display()

    def update_guess_display(self):
        self.guess_canvas.delete("all")
        for i, color in enumerate(self.current_guess):
            self.guess_canvas.create_oval(10 + i * 50, 10, 50 + i * 50, 50, fill=Color_Names[color], outline='black')

    def submit_guess(self):
        if len(self.current_guess) != Code_length:
            self.feedback_label.config(text=f"Veuillez choisir {Code_length} couleurs.", fg='yellow')
            return

        black_pegs, white_pegs = self.get_feedback(self.secret_code, self.current_guess)

        self.previous_guesses.append((self.current_guess[:], black_pegs, white_pegs))
        self.update_history_display()

        if black_pegs == Code_length:
            self.feedback_label.config(text="🎉 Bravo ! Vous avez trouvé le code !", fg='lime')
            self.submit_button.config(state=tk.DISABLED)
        else:
            self.attempts += 1
            attempts_left = Tries - self.attempts
            if attempts_left == 0:
                self.feedback_label.config(text=f"Game Over ! Le code était : {self.secret_code}", fg='red')
                self.submit_button.config(state=tk.DISABLED)
            else:
                self.feedback_label.config(text=f"{black_pegs} 🎯 | {white_pegs} ⚪ | {attempts_left} essais restants.",
                                           fg='white')

            self.current_guess = []
            self.guess_canvas.delete("all")

    def get_feedback(self, secret_code, guess):
        black_pegs = sum(s == g for s, g in zip(secret_code, guess))
        white_pegs = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black_pegs
        return black_pegs, white_pegs

    def update_history_display(self):
        for widget in self.history_inner_frame.winfo_children():
            widget.destroy()

        for i, (guess, black, white) in enumerate(self.previous_guesses):
            frame = tk.Frame(self.history_inner_frame, bg='#222', pady=3)
            frame.pack(fill="x")

            for color in guess:
                tk.Canvas(frame, width=30, height=30, bg=Color_Names[color]).pack(side=tk.LEFT, padx=2)

            tk.Label(frame, text=f" {black} 🎯 | {white} ⚪ ", fg="white", bg="#222", font=("Arial", 12)).pack(side=tk.RIGHT)

        self.history_canvas.update_idletasks()
        self.history_canvas.config(scrollregion=self.history_canvas.bbox("all"))

    def reset_game(self):
        self.secret_code = self.code_generator()
        self.attempts = 0
        self.previous_guesses = []
        self.current_guess = []
        self.feedback_label.config(text=f"Essais restants : {Tries}", fg='white')
        self.submit_button.config(state=tk.NORMAL)
        self.guess_canvas.delete("all")
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    game = MastermindGame(root)
    root.mainloop()
