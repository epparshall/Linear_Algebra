import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.linalg import fractional_matrix_power
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Linear_Transform():
    def __init__(self, matrix, vector, num_points):
        self.A = matrix # 2x2
        self.x = vector # 2x1
        self.b = self.A @ self.x # 2x1
        self.num_points = num_points
        self.length_x = (self.x[0]**2 + self.x[1] ** 2) ** .5
        self.length_b = (self.b[0]**2 + self.b[1] ** 2) ** .5
        self.points = self.matrix_power_interpolate(self.num_points)

        # Animation Parameters

        self.root = Tk.Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.A00_Str = Tk.StringVar(self.root, str(round(self.A[0][0], 4)))
        self.A01_Str = Tk.StringVar(self.root, str(round(self.A[0][1], 4)))
        self.A10_Str = Tk.StringVar(self.root, str(round(self.A[1][0], 4)))
        self.A11_Str = Tk.StringVar(self.root, str(round(self.A[1][1], 4)))

        self.x0_Str = Tk.StringVar(self.root, str(round(self.x[0], 4)))
        self.x1_Str = Tk.StringVar(self.root, str(round(self.x[1], 4)))

        self.b0_Str = Tk.StringVar(self.root, str(round(self.b[0], 4)))
        self.b1_Str = Tk.StringVar(self.root, str(round(self.b[1], 4)))

        self.pad_entry_x = 10
        self.pad_entry_y = 10
        self.ipad_entry_x = 10
        self.ipad_entry_y = 10
        self.plot_grid_size = 10
        self.lim_factor = 1.1
        self.font_size = 20

        self.total_min = np.min([np.min([0, np.min(self.points[:,0])]), np.min([0, np.min(self.points[:,1])])])
        self.total_max = np.max([np.max([0, np.max(self.points[:,0])]), np.max([0, np.max(self.points[:,1])])])

    def matrix_power_interpolate(self, num_points):
        arr = np.zeros((num_points, 2))
        start_pause = int(.1 * num_points)
        end_pause = int(.1 * num_points)

        for i in range(start_pause):
            arr[i] = self.x

        for j in range(len(arr) - start_pause - end_pause):
            arr[j + start_pause] = fractional_matrix_power(self.A, j/(len(arr) - start_pause - end_pause)) @ self.x

        for l in range(end_pause):
            arr[l + len(arr) - end_pause] = self.b

        return arr
    
    def animate_matrix_power(self):
        fig = plt.Figure()

        def animation_function(i):
            Q.set_UVC([self.points[i][0]], [self.points[i][1]])

        self.buttonPlot = Tk.Button(self.root, text="Plot", command=self.update_animation)        
        self.buttonPlot.grid(row=2+self.plot_grid_size, column=0, padx=40, pady=20, ipadx=150, ipady=50)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(column=0,row=1, padx=40, pady=20, ipadx=150, ipady=150, rowspan=self.plot_grid_size, columnspan=self.plot_grid_size)

        self.create_gui_matrix_elements()

        self.ax = fig.add_subplot(111)
        Q = self.ax.quiver([0], [0], [self.points[0][0]], [self.points[0][1]], angles='xy', scale_units='xy', scale=1)
        anim = animation.FuncAnimation(fig, animation_function, np.arange(1, self.num_points), interval=25, blit=False)
        self.ax.grid()
        self.ax.set_axisbelow(True)

        self.ax.set_xlim(self.lim_factor*self.total_min, self.lim_factor*self.total_max)
        self.ax.set_ylim(self.lim_factor*self.total_min, self.lim_factor*self.total_max)

        plt.grid()
        Tk.mainloop()

    def create_gui_matrix_elements(self):
        Tk.Label(self.root, width=16, fg='blue', font=('Arial', self.font_size,'bold'), textvariable=Tk.StringVar(self.root, "Linear Transformation")).grid(column=0, row=0, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        Tk.Label(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=Tk.StringVar(self.root, "A = ")).grid(row=int(self.plot_grid_size/2)-1, column=self.plot_grid_size, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        Tk.Label(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=Tk.StringVar(self.root, "x = ")).grid(row=int(self.plot_grid_size/2)-4, column=self.plot_grid_size, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y) 
        Tk.Label(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=Tk.StringVar(self.root, "b = ")).grid(row=int(self.plot_grid_size/2)+1, column=self.plot_grid_size, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)          

        self.A00 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.A00_Str).grid(row=int(self.plot_grid_size/2)-1, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        self.A01 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.A01_Str).grid(row=int(self.plot_grid_size/2)-1, column=self.plot_grid_size+2, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        self.A10 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.A10_Str).grid(row=int(self.plot_grid_size/2), column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        self.A11 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.A11_Str).grid(row=int(self.plot_grid_size/2), column=self.plot_grid_size+2, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        self.X0 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.x0_Str).grid(row=int(self.plot_grid_size/2) - 4, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)
        self.X1 = Tk.Entry(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.x1_Str).grid(row=int(self.plot_grid_size/2) - 3, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y)

        Tk.Label(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.b0_Str).grid(row=int(self.plot_grid_size/2)+1, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y) 
        Tk.Label(self.root, width=16, fg='blue', font=('Arial',self.font_size,'bold'), textvariable=self.b1_Str).grid(row=int(self.plot_grid_size/2)+2, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y) 
        Tk.Label(self.root, width=16, fg='blue', font=('Arial', 2*self.font_size,'bold'), textvariable=Tk.StringVar(self.root, "Ax = b")).grid(row=int(self.plot_grid_size/2)+4, column=self.plot_grid_size+1, padx=self.pad_entry_x, pady=self.pad_entry_y, ipadx=self.ipad_entry_x, ipady=self.ipad_entry_y) 

    def update_animation(self):
        self.A[0][0] = float(self.A00_Str.get())
        self.A[0][1] = float(self.A01_Str.get())
        self.A[1][0] = float(self.A10_Str.get())
        self.A[1][1] = float(self.A11_Str.get())

        self.x[0] = float(self.x0_Str.get())
        self.x[1] = float(self.x1_Str.get())

        self.b = self.A @ self.x
        self.length_x = (self.x[0]**2 + self.x[1] ** 2) ** .5
        self.length_b = (self.b[0]**2 + self.b[1] ** 2) ** .5
        self.points = self.matrix_power_interpolate(self.num_points)

        self.b0_Str.set(str(round(self.b[0], 4)))
        self.b1_Str.set(str(round(self.b[1], 4)))

        self.total_min = np.min([np.min([0, np.min(self.points[:,0])]), np.min([0, np.min(self.points[:,1])])])
        self.total_max = np.max([np.max([0, np.max(self.points[:,0])]), np.max([0, np.max(self.points[:,1])])])

        self.ax.set_xlim(self.lim_factor*self.total_min, self.lim_factor*self.total_max)
        self.ax.set_ylim(self.lim_factor*self.total_min, self.lim_factor*self.total_max)

if __name__ == "__main__":
    theta = 95 * (np.pi / 180)
    A = 2 * np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    x = np.array([3, 2]).T

    obj = Linear_Transform(matrix=A, vector=x, num_points=175)
    obj.animate_matrix_power()