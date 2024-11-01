import tkinter as tk
import numpy as np

NUM_PARTICLES = 30  
MAX_ITERATIONS = 100 
TARGET = np.array([300, 200])  

class Particle:
    def __init__(self):
        self.position = np.random.rand(2) * 400  
        self.velocity = np.random.rand(2) * 2 - 1 
        self.best_position = self.position.copy()  
        self.best_value = float('inf')  

    def evaluate(self):
        value = np.linalg.norm(self.position - TARGET)
        if value < self.best_value:
            self.best_value = value
            self.best_position = self.position.copy()

    def update(self):
        inertia_weight = 0.5  
        cognitive_weight = 1.5  
        social_weight = 1.5  

        r1 = np.random.rand()
        r2 = np.random.rand()

        self.velocity = (inertia_weight * self.velocity +
                         cognitive_weight * r1 * (self.best_position - self.position) +
                         social_weight * r2 * (TARGET - self.position))
        
        self.position += self.velocity

class PSO:
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = [Particle() for _ in range(NUM_PARTICLES)]
        self.iteration = 0

    def update(self):
        for particle in self.particles:
            particle.evaluate()
            particle.update()

        self.draw()
        self.iteration += 1

        if self.iteration < MAX_ITERATIONS:
            self.canvas.after(100, self.update) 

    def draw(self):
        self.canvas.delete("all")

        self.canvas.create_oval(TARGET[0] - 5, TARGET[1] - 5, TARGET[0] + 5, TARGET[1] + 5, fill="red", outline="black")

        for particle in self.particles:
            x, y = particle.position
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

        best_particle = min(self.particles, key=lambda p: p.best_value)
        self.canvas.create_oval(best_particle.best_position[0] - 5, best_particle.best_position[1] - 5,
                                best_particle.best_position[0] + 5, best_particle.best_position[1] + 5,
                                fill="green", outline="black") 

root = tk.Tk()
root.title("Optimización por Partículas (PSO)")

canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

pso = PSO(canvas)
pso.update() 

root.mainloop()
