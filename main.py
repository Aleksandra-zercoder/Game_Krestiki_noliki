import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")

# Глобальные переменные
board_size = 3          # Размер игрового поля (будет выбран игроком)
starting_symbol = "X"   # Символ, которым играет игрок (выбирается)
current_player = "X"    # Текущий игрок (устанавливается после выбора символа)
buttons = []            # Список кнопок для игрового поля

# Счётчики побед и ничьих
score_X = 0
score_O = 0
draws = 0

def check_winner():
    """Проверяет строки, столбцы и диагонали для определения победителя."""
    # Проверяем строки
    for i in range(board_size):
        row_values = [buttons[i][j]["text"] for j in range(board_size)]
        if row_values[0] != "" and row_values.count(row_values[0]) == board_size:
            return row_values[0]
    # Проверяем столбцы
    for j in range(board_size):
        col_values = [buttons[i][j]["text"] for i in range(board_size)]
        if col_values[0] != "" and col_values.count(col_values[0]) == board_size:
            return col_values[0]
    # Главная диагональ
    diag = [buttons[i][i]["text"] for i in range(board_size)]
    if diag[0] != "" and diag.count(diag[0]) == board_size:
        return diag[0]
    # Побочная диагональ
    anti_diag = [buttons[i][board_size-1-i]["text"] for i in range(board_size)]
    if anti_diag[0] != "" and anti_diag.count(anti_diag[0]) == board_size:
        return anti_diag[0]
    return None

def highlight_winner():
    """Подсвечивает выигрышную комбинацию светло-зелёным цветом."""
    # Строки
    for i in range(board_size):
        row_values = [buttons[i][j]["text"] for j in range(board_size)]
        if row_values[0] != "" and row_values.count(row_values[0]) == board_size:
            for j in range(board_size):
                buttons[i][j].config(bg="lightgreen")
            return
    # Столбцы
    for j in range(board_size):
        col_values = [buttons[i][j]["text"] for i in range(board_size)]
        if col_values[0] != "" and col_values.count(col_values[0]) == board_size:
            for i in range(board_size):
                buttons[i][j].config(bg="lightgreen")
            return
    # Главная диагональ
    diag = [buttons[i][i]["text"] for i in range(board_size)]
    if diag[0] != "" and diag.count(diag[0]) == board_size:
        for i in range(board_size):
            buttons[i][i].config(bg="lightgreen")
        return
    # Побочная диагональ
    anti_diag = [buttons[i][board_size-1-i]["text"] for i in range(board_size)]
    if anti_diag[0] != "" and anti_diag.count(anti_diag[0]) == board_size:
        for i in range(board_size):
            buttons[i][board_size-1-i].config(bg="lightgreen")
        return

def update_scoreboard():
    """Обновляет метку со счётом."""
    scoreboard_label.config(text=f"X: {score_X}    O: {score_O}    Ничья: {draws}")

def reset_board():
    """Очищает поле – сбрасывает текст и фон кнопок."""
    for i in range(board_size):
        for j in range(board_size):
            buttons[i][j].config(text="", bg="SystemButtonFace")

def reset_game():
    """Сбрасывает поле, возвращая ход к выбранному символу, но не обнуляет счёт."""
    global current_player
    current_player = starting_symbol
    current_player_label.config(text=f"Ходит: {current_player}")
    reset_board()

def on_click(row, col):
    """Обработчик клика по кнопке (ячейке)."""
    global current_player, score_X, score_O, draws

    if buttons[row][col]["text"] != "":
        return  # Ячейка уже занята

    buttons[row][col]["text"] = current_player

    winner = check_winner()
    if winner:
        highlight_winner()
        if winner == "X":
            score_X += 1
        else:
            score_O += 1
        update_scoreboard()
        messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
        reset_board()
        current_player = starting_symbol
        current_player_label.config(text=f"Ходит: {current_player}")
        # Проверка матча до 3 побед
        if score_X == 3 or score_O == 3:
            champ = "X" if score_X == 3 else "O"
            messagebox.showinfo("Матч окончен", f"Игрок {champ} выиграл матч!\nСчёт обнуляется.")
            score_X = 0
            score_O = 0
            draws = 0
            update_scoreboard()
        return

    # Если поле заполнено и победителя нет – ничья
    if all(buttons[i][j]["text"] != "" for i in range(board_size) for j in range(board_size)):
        draws += 1
        update_scoreboard()
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_board()
        current_player = starting_symbol
        current_player_label.config(text=f"Ходит: {current_player}")
        return

    current_player = "O" if current_player == "X" else "X"
    current_player_label.config(text=f"Ходит: {current_player}")

def create_board():
    """Создаёт игровое поле нужного размера."""
    global buttons
    buttons = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)

def choose_board_size():
    """Окно для выбора размера игрового поля."""
    global board_size
    size_window = tk.Toplevel(window)
    size_window.title("Выбор размера поля")
    size_window.grab_set()

    tk.Label(size_window, text="Выберите размер игрового поля:", font=("Arial", 12)).pack(pady=5)
    size_var = tk.IntVar(value=3)
    tk.Radiobutton(size_window, text="3x3", variable=size_var, value=3, font=("Arial", 12)).pack(anchor="w")
    tk.Radiobutton(size_window, text="4x4", variable=size_var, value=4, font=("Arial", 12)).pack(anchor="w")
    tk.Radiobutton(size_window, text="5x5", variable=size_var, value=5, font=("Arial", 12)).pack(anchor="w")

    def set_size():
        global board_size
        board_size = size_var.get()
        size_window.destroy()
        create_board()
        # Размещаем метки и кнопку сброса под игровым полем
        current_player_label.grid(row=board_size, column=0, columnspan=board_size)
        scoreboard_label.grid(row=board_size+1, column=0, columnspan=board_size)
        reset_button.grid(row=board_size+2, column=0, columnspan=board_size, sticky="nsew", pady=10)
        choose_symbol()  # После выбора размера запускаем окно выбора символа

    tk.Button(size_window, text="OK", font=("Arial", 12), command=set_size).pack(pady=5)

def choose_symbol():
    """Окно для выбора символа (X или O) перед началом игры."""
    global starting_symbol, current_player
    sym_window = tk.Toplevel(window)
    sym_window.title("Выбор символа")
    sym_window.grab_set()
    tk.Label(sym_window, text="Выберите символ для игры:", font=("Arial", 12)).pack(pady=5)
    sym_var = tk.StringVar(value="X")
    tk.Radiobutton(sym_window, text="X", variable=sym_var, value="X", font=("Arial", 12)).pack(anchor="w")
    tk.Radiobutton(sym_window, text="O", variable=sym_var, value="O", font=("Arial", 12)).pack(anchor="w")

    def set_symbol():
        global starting_symbol, current_player
        starting_symbol = sym_var.get()
        current_player = starting_symbol
        current_player_label.config(text=f"Ходит: {current_player}")
        sym_window.destroy()

    tk.Button(sym_window, text="OK", font=("Arial", 12), command=set_symbol).pack(pady=5)

# Метки и кнопка сброса (будут размещены под игровым полем)
current_player_label = tk.Label(window, text=f"Ходит: {current_player}", font=("Arial", 14))
scoreboard_label = tk.Label(window, text=f"X: {score_X}    O: {score_O}    Ничья: {draws}", font=("Arial", 12))
reset_button = tk.Button(window, text="Сброс", font=("Arial", 14), command=reset_game)

# Запускаем выбор размера поля (в дальнейшем после него откроется окно выбора символа)
choose_board_size()

window.mainloop()
