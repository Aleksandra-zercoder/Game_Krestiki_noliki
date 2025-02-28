import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("300x400")  # увеличена высота для размещения дополнительных меток

current_player = "X"
buttons = []

# Счётчики побед и ничьих
score_X = 0
score_0 = 0
draws = 0

def check_winner():
    # Проверяем строки и столбцы
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    # Проверяем диагонали
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]
    return None

def highlight_winner():
    # Подсвечиваем выигрышную комбинацию
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            for j in range(3):
                buttons[i][j].config(bg="lightgreen")
            return
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            for j in range(3):
                buttons[j][i].config(bg="lightgreen")
            return
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        for i in range(3):
            buttons[i][i].config(bg="lightgreen")
        return
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        buttons[0][2].config(bg="lightgreen")
        buttons[1][1].config(bg="lightgreen")
        buttons[2][0].config(bg="lightgreen")
        return

def update_score(winner):
    global score_X, score_0
    if winner == "X":
        score_X += 1
    elif winner == "0":
        score_0 += 1
    update_scoreboard()

def update_draw():
    global draws
    draws += 1
    update_scoreboard()

def update_scoreboard():
    scoreboard_label.config(text=f"X: {score_X}    0: {score_0}    Ничья: {draws}")

def reset_game():
    global current_player
    current_player = "X"
    current_player_label.config(text=f"Ходит: {current_player}")
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="SystemButtonFace")

def on_click(row, col):
    global current_player

    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player

    winner = check_winner()
    if winner:
        highlight_winner()
        update_score(winner)
        messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
        return

    # Проверка на ничью: если все кнопки заполнены и победителя нет
    if all(button['text'] != "" for row in buttons for button in row):
        update_draw()
        messagebox.showinfo("Игра окончена", "Ничья!")
        return

    current_player = "0" if current_player == "X" else "X"
    current_player_label.config(text=f"Ходит: {current_player}")

# Создание игрового поля (3x3 кнопок)
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

# Метка для отображения текущего игрока
current_player_label = tk.Label(window, text=f"Ходит: {current_player}", font=("Arial", 14))
current_player_label.grid(row=3, column=0, columnspan=3)

# Метка для отображения счёта
scoreboard_label = tk.Label(window, text=f"X: {score_X}    0: {score_0}    Ничья: {draws}", font=("Arial", 12))
scoreboard_label.grid(row=4, column=0, columnspan=3)

# Кнопка сброса игры
reset_button = tk.Button(window, text="Сброс", font=("Arial", 14), command=reset_game)
reset_button.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)

window.mainloop()
