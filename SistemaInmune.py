import tkinter as tk
import random
import numpy as np

NUM_ANTIBODIES = 20  
NUM_GENERATIONS = 50  
MUTATION_RATE = 0.1  
TARGET = np.array([1, 2, 3])  

def evaluate(antibody):
    return -np.sum(np.abs(antibody - TARGET))  

def generate_antibody():
    return np.random.randint(0, 5, size=TARGET.shape)  

def create_initial_population():
    return [generate_antibody() for _ in range(NUM_ANTIBODIES)]

def mutate(antibody):
    for i in range(len(antibody)):
        if random.random() < MUTATION_RATE:
            antibody[i] = random.randint(0, 4) 
    return antibody

def immune_system(canvas, generation_label):
    population = create_initial_population()
    
    for generation in range(NUM_GENERATIONS):
        scores = [evaluate(antibody) for antibody in population]
        
        best_antibodies = [population[i] for i in np.argsort(scores)[-5:]]  
            
        new_population = []
        for antibody in best_antibodies:
            new_population.append(antibody)  
            new_population.append(mutate(antibody.copy()))  
        
        while len(new_population) < NUM_ANTIBODIES:
            new_population.append(generate_antibody())
        
        population = new_population
        
        canvas.delete("all")
        draw_axes(canvas)
        draw_population(canvas, population, generation)
        generation_label.config(text=f"Generación: {generation + 1}")
        canvas.update()
        canvas.after(200)  

    final_scores = [evaluate(antibody) for antibody in population]
    best_solution = population[np.argmax(final_scores)]
    print("Mejor solución encontrada:", best_solution)
    print("Evaluación:", evaluate(best_solution))

def draw_population(canvas, population, generation):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    target_x = TARGET[0] * (canvas_width // 5)
    target_y = canvas_height - TARGET[1] * (canvas_height // 5)
    
    canvas.create_oval(target_x - 5, target_y - 5, target_x + 5, target_y + 5, fill="red", outline="black")
    canvas.create_text(target_x, target_y - 10, text="Objetivo", fill="red", font=("Arial", 10))

    for i, antibody in enumerate(population):
        x = antibody[0] * (canvas_width // 5)
        y = canvas_height - antibody[1] * (canvas_height // 5)
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="black")
        canvas.create_text(x, y - 10, text=f"Anticuerpo: {evaluate(antibody):.2f}", fill="blue", font=("Arial", 8))

def draw_axes(canvas):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    canvas.create_line(0, canvas_height, canvas_width, canvas_height, fill="black")
    for i in range(5):
        x = i * (canvas_width // 5)
        canvas.create_line(x, canvas_height - 5, x, canvas_height + 5, fill="black")
        canvas.create_text(x, canvas_height + 15, text=str(i), fill="black", font=("Arial", 10))

    canvas.create_line(0, 0, 0, canvas_height, fill="black")
    for i in range(5):
        y = canvas_height - i * (canvas_height // 5)
        canvas.create_line(-5, y, 5, y, fill="black")
        canvas.create_text(-20, y, text=str(i), fill="black", font=("Arial", 10))

root = tk.Tk()
root.title("Algoritmo de Sistema Inmune")
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

generation_label = tk.Label(root, text="Generación: 0")
generation_label.pack()

start_button = tk.Button(root, text="Iniciar", command=lambda: immune_system(canvas, generation_label))
start_button.pack()

root.mainloop()
