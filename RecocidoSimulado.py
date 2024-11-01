import tkinter as tk
import random
import math

def objective_function(x):
    return x ** 2

def simulated_annealing():
    temperature = 1000
    cooling_rate = 0.99
    current_x = random.uniform(-10, 10)
    current_score = objective_function(current_x)
    
    while temperature > 0.1:
        next_x = current_x + random.uniform(-1, 1)
        next_score = objective_function(next_x)
        
        if next_score < current_score or random.random() < math.exp((current_score - next_score) / temperature):
            current_x, current_score = next_x, next_score
            
        temperature *= cooling_rate

        x_canvas = 250 + current_x * 20
        y_canvas = 250 - current_score / 5
        canvas.coords(marker, x_canvas - 5, y_canvas - 5, x_canvas + 5, y_canvas + 5)

        root.update()

root = tk.Tk()
root.title("Simulated Annealing")
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

for x in range(-10, 11):
    y = objective_function(x)
    canvas.create_oval(250 + x * 20 - 2, 250 - y / 5 - 2, 250 + x * 20 + 2, 250 - y / 5 + 2, fill="black")

marker = canvas.create_oval(250, 250, 250, 250, fill="red", outline="red")

start_button = tk.Button(root, text="Iniciar", command=simulated_annealing)
start_button.pack()

root.mainloop()
