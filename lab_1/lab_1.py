import tkinter as tk
import random

zero = list("111101101101111")
one = list("001001001001001")
two = list("111001111100111")
three = list("111001111001111")
four = list("101101111001001")
five = list("111100111001111")
six = list("111100111101111")
seven = list("111001001001001")
eight = list("111101111101111")
nine = list("111101111001111")

digits = [zero, one, two, three, four, five, six, seven, eight, nine]

weights = [[0 for _ in range(15)] for _ in range(10)]
bias = 7

def proceed(number, correct_num=5):
    net = sum(int(number[i]) * weights[correct_num][i] for i in range(15))
    return net >= bias

def decrease(number, correct_num=5):
    for i in range(15):
        if int(number[i]) == 1:
            weights[correct_num][i] -= 1

def increase(number, correct_num=5):
    for i in range(15):
        if int(number[i]) == 1:
            weights[correct_num][i] += 1

def train():
    for correct_num in range(10):
        for _ in range(10000):
            option = random.randint(0, 9)
            if option != correct_num:
                if proceed(digits[option], correct_num):
                    decrease(digits[option], correct_num)
            else:
                if not proceed(digits[correct_num], correct_num):
                    increase(digits[correct_num], correct_num)

def recognize(num):
    scores = []
    for i in range(10):
        score = sum(int(num[j]) == int(digits[i][j]) for j in range(15))
        scores.append((score, str(i)))

    scores.sort(reverse=True, key=lambda x: x[0])

    if scores[0][0] == 15:
        return scores[0][1]

    if scores[0][0] >= 5:
        if len(scores) > 1 and scores[1][0] >= 5:
            return f"Скорее {scores[0][1]}"
        return scores[0][1]

    return "Не знаю, что за число"

class RecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание цифр 3x5")

        self.exit_button = tk.Button(root, text="Выход", command=root.quit)
        self.exit_button.grid(row=0, column=0)

        self.matrices = []

        self.create_matrices()

    def create_matrices(self):
        for matrix in self.matrices:
            for widget in matrix["widgets"]:
                widget.destroy()
        self.matrices.clear()

        for m in range(10):
            matrix_frame = tk.Frame(self.root)
            matrix_frame.grid(row=1, column=m, padx=5, pady=10)

            grid = [[0 for _ in range(3)] for _ in range(5)]
            buttons = []
            for row in range(5):
                button_row = []
                for col in range(3):
                    btn = tk.Button(matrix_frame, bg="white", width=2, height=1, command=lambda r=row, c=col, m=m: self.toggle(m, r, c))
                    btn.grid(row=row, column=col, padx=1, pady=1)
                    button_row.append(btn)
                buttons.append(button_row)

            recognize_button = tk.Button(matrix_frame, text="Узнать число", command=lambda m=m: self.on_recognize(m))
            recognize_button.grid(row=5, column=0, columnspan=3, pady=5)

            result_label = tk.Label(matrix_frame, text="Результат:", font=("Arial", 10), width=20, anchor="w")
            result_label.grid(row=6, column=0, columnspan=3, pady=5)

            self.matrices.append({
                "frame": matrix_frame,
                "grid": grid,
                "buttons": buttons,
                "recognize_button": recognize_button,
                "result_label": result_label,
                "widgets": buttons + [recognize_button, result_label]
            })

    def toggle(self, m, row, col):
        current_color = self.matrices[m]["buttons"][row][col].cget("bg")
        new_color = "black" if current_color == "white" else "white"
        self.matrices[m]["buttons"][row][col].config(bg=new_color)
        self.matrices[m]["grid"][row][col] = 1 if new_color == "black" else 0

    def on_recognize(self, m):
        num = "".join(str(self.matrices[m]["grid"][row][col]) for row in range(5) for col in range(3))
        result = recognize(num)
        self.matrices[m]["result_label"].config(text=f"Результат:\n{result}")

train()
root = tk.Tk()
root.geometry("1550x350")
app = RecognizerApp(root)
root.mainloop()
