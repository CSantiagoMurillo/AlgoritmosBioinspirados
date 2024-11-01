import tkinter as tk
import random
import math

def objective_function(x):
    return math.sin(x)

def genetic_algorithm():
    population = [random.uniform(0, 10) for _ in range(10)]
    for _ in range(100):  
        scores = [(x, objective_function(x)) for x in population]
        scores.sort(key=lambda x: x[1], reverse=True)

        best = scores[:5]
        best_values = [b[0] for b in best]

        population = best_values + [random.uniform(0, 10) for _ in range(5)]
        population = [x + random.uniform(-0.1, 0.1) for x in population]

        canvas.delete("all")
        for x, y in scores:
            canvas.create_oval(50 + x * 40 - 2, 250 - y * 100 - 2, 50 + x * 40 + 2, 250 - y * 100 + 2, fill="blue")
        root.update()

root = tk.Tk()
root.title("Algoritmo Genético")
canvas = tk.Canvas(root, width=500, height=300, bg="white")
canvas.pack()

canvas.create_line(50, 250, 450, 250, fill="black")
canvas.create_line(50, 50, 50, 250, fill="black")

start_button = tk.Button(root, text="Iniciar", command=genetic_algorithm)
start_button.pack()

root.mainloop()
