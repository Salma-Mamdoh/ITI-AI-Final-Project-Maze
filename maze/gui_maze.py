import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from maze_solver import Maze

class MazeSolverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Solver")
        self.master.geometry("800x600")
        self.master.configure(bg="#f5f5f5")

        # Main frame
        self.main_frame = tk.Frame(master, bg="#ffffff", bd=5, relief=tk.RAISED)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(self.main_frame, text="Maze Solver", font=("Helvetica", 24, 'bold'), bg="#ffffff")
        title_label.pack(pady=(10, 20))

        # Frame for options
        self.options_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.options_frame.pack(side=tk.LEFT, padx=20)

        self.algorithm_var = tk.StringVar(value="BFS")
        algorithms = ["BFS", "DFS", "Heuristic Search", "Optimal Path"]

        # Algorithm selection
        alg_label = tk.Label(self.options_frame, text="Select Algorithm", font=("Helvetica", 16), bg="#ffffff")
        alg_label.pack(pady=(0, 10))

        self.algorithm_menu = ttk.Combobox(self.options_frame, textvariable=self.algorithm_var, values=algorithms, state='readonly', font=("Helvetica", 12))
        self.algorithm_menu.pack(pady=(0, 20))

        # Buttons
        select_button = tk.Button(self.options_frame, text="Select Maze", command=self.select_maze,
                                  font=("Helvetica", 12), bg="#4CAF50", fg="white")
        select_button.pack(pady=(10, 5))

        self.solve_button = tk.Button(self.options_frame, text="Solve Maze", command=self.solve_maze, 
                                       state=tk.DISABLED, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.solve_button.pack(pady=(5, 20))

        # Frame for canvas and scrollbars
        self.canvas_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create scrollbars
        self.canvas_scroll_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.canvas_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_scroll_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.canvas_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightbackground="#4CAF50",
                                yscrollcommand=self.canvas_scroll_y.set, xscrollcommand=self.canvas_scroll_x.set)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbars
        self.canvas_scroll_y.config(command=self.canvas.yview)
        self.canvas_scroll_x.config(command=self.canvas.xview)

        # Footer label
        footer_label = tk.Label(self.main_frame, text="© 2024 Maze Solver Inc.", font=("Helvetica", 10), bg="#ffffff")
        footer_label.pack(side=tk.BOTTOM, pady=(10, 0))

    def select_maze(self):
        maze_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if maze_file:
            try:
                self.maze = Maze(maze_file)
                self.load_maze_to_canvas()
                self.solve_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No maze file selected.")

    def load_maze_to_canvas(self):
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # Reset scroll region
        for i, row in enumerate(self.maze.walls):
            for j, col in enumerate(row):
                color = "white" if not col else "black"
                self.canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color)

        # Mark the start point
        start_row, start_col = self.maze.start  # Assuming self.maze.start returns a tuple (row, col)
        self.canvas.create_oval(start_col * 20 + 5, start_row * 20 + 5, 
                                start_col * 20 + 15, start_row * 20 + 15, fill="green", outline="")

        # Mark the end point
        end_row, end_col = self.maze.goal  # Assuming self.maze.end returns a tuple (row, col)
        self.canvas.create_oval(end_col * 20 + 5, end_row * 20 + 5, 
                                end_col * 20 + 15, end_row * 20 + 15, fill="red", outline="")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # Update scroll region to fit maze

    def solve_maze(self):
        try:
            selected_algorithm = self.algorithm_var.get()
            if selected_algorithm == "BFS":
                self.maze.solve_bfs()
            elif selected_algorithm == "DFS":
                self.maze.solve_dfs()
            elif selected_algorithm == "Heuristic Search":
                self.maze.solve_a_star()
            elif selected_algorithm == "Optimal Path":
                self.maze.solve_a_star()  # A* also serves as optimal path
            self.load_solution_to_canvas()
            messagebox.showinfo("Solved", f"States Explored: {self.maze.num_explored}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_solution_to_canvas(self):
        if self.maze.solution is not None:
            solution_cells = self.maze.solution[1]
            for cell in solution_cells:
                row, col = cell
                self.canvas.create_rectangle(col * 20, row * 20, (col + 1) * 20, (row + 1) * 20, fill="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()
