import tkinter as tk
import numpy as np
import random

GRID_SIZE = 20  
NUM_ANTS = 10  
EVAPORATION_RATE = 0.1 
INITIAL_PHEROMONE = 1.0  
PHEROMONE_INFLUENCE = 1.0  
DISTANCE_INFLUENCE = 2.0  

class Grid:
    def __init__(self, size):
        self.size = size
        self.pheromones = np.zeros((size, size)) + INITIAL_PHEROMONE  
        self.grid = np.zeros((size, size)) 
        self.start = (0, 0)  
        self.goal = (size - 1, size - 1) 
        self.init_obstacles() 

    def init_obstacles(self):
        for _ in range(int(self.size ** 2 * 0.2)): 
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) != self.start and (x, y) != self.goal:
                self.grid[x][y] = 1  

    def is_valid_move(self, pos):
        return 0 <= pos[0] < self.size and 0 <= pos[1] < self.size and self.grid[pos] == 0

    def update_pheromones(self, paths):
        self.pheromones *= (1 - EVAPORATION_RATE)
        for path in paths:
            for pos in path:
                self.pheromones[pos] += 1.0 / len(path) 

class Ant:
    def __init__(self, grid, start_pos):
        self.grid = grid
        self.path = []  
        self.current_pos = start_pos  

    def move(self):
        if self.current_pos == self.grid.goal:
            return True  

        moves = [(self.current_pos[0] + dx, self.current_pos[1] + dy)
                 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                 if self.grid.is_valid_move((self.current_pos[0] + dx, self.current_pos[1] + dy))]

        if not moves:
            return False 

        probabilities = []
        for move in moves:
            pheromone = self.grid.pheromones[move]
            distance = 1 / (1 + np.linalg.norm(np.array(move) - np.array(self.grid.goal)))
            probabilities.append((pheromone ** PHEROMONE_INFLUENCE) * (distance ** DISTANCE_INFLUENCE))

        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        self.current_pos = random.choices(moves, probabilities)[0]
        self.path.append(self.current_pos)

        return False 

class AntColony:
    def __init__(self, canvas):
        self.canvas = canvas
        self.grid = Grid(GRID_SIZE)
        self.ants = [Ant(self.grid, (0, i)) for i in range(NUM_ANTS)]  
        self.paths = []
        self.running = False  

    def start_simulation(self):
        self.running = True
        self.paths.clear()  
        self.update()  

    def update(self):
        if not self.running:
            return  

        for ant in self.ants:
            if not ant.move():
                continue
            self.paths.append(ant.path)  
            ant.current_pos = self.grid.start 

        self.grid.update_pheromones(self.paths)
        self.draw()

        if len(self.paths) < NUM_ANTS * 10: 
            self.canvas.after(200, self.update) 

    def draw(self):
        self.canvas.delete("all")

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid.grid[i][j] == 1:
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill="black")

        for path in self.paths:
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                self.canvas.create_line(y1 * 30 + 15, x1 * 30 + 15, y2 * 30 + 15, x2 * 30 + 15, fill="blue", width=3)

        self.canvas.create_oval(0 * 30 + 5, 0 * 30 + 5, 0 * 30 + 25, 0 * 30 + 25, fill="green")  # Inicio
        self.canvas.create_oval((GRID_SIZE - 1) * 30 + 5, (GRID_SIZE - 1) * 30 + 5, (GRID_SIZE - 1) * 30 + 25, (GRID_SIZE - 1) * 30 + 25, fill="red")  # Objetivo

root = tk.Tk()
root.title("Optimización por Colonia de Hormigas (ACO)")

canvas = tk.Canvas(root, width=GRID_SIZE * 30, height=GRID_SIZE * 30, bg="white")
canvas.pack()

ant_colony = AntColony(canvas)

start_button = tk.Button(root, text="Iniciar Simulación", command=ant_colony.start_simulation)
start_button.pack()

root.mainloop()
