from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import time, serial, serial.tools.list_ports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

#import kconvert

class MainApp:
    def __init__(self, window):
        # Setting up the window
        self.window = window
        self.window.title('SBFFs: Temperature Monitor')
        self.window.geometry('1300x700')
        self.window.configure(bg='gray13')
        self.window.minsize(1300, 700)
        self.window.maxsize(1300, 700)

        # Load Images
        self.load_images()
        
        # Main windows
        self.setup_microwave()
        self.setup_leftframe()
        self.setup_rightframe()

    # Loading in Images
    def load_images(self):
        self.export_img = ctk.CTkImage(Image.open("export-icon.png"), size=(25,25))
        self.info_img = ctk.CTkImage(Image.open("info-icon.png"), size=(25,25))
        self.temperature_img = ctk.CTkImage(Image.open("temperature-icon.png"), size=(30,30))

    #The whole Microwave
    def setup_microwave(self):
        self.main_frame = ctk.CTkFrame(self.window, width=1300, height=700, fg_color="red", corner_radius=0)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.main_frame.pack_propagate(False)

    def setup_leftframe(self):
        self.left_frame = ctk.CTkFrame(self.main_frame, width= 850, height = 700, fg_color="white", corner_radius=0)
        self.left_frame.pack(side =LEFT, fill =X)
        self.left_frame.pack_propagate(False)
        
        self.top_frame = ctk.CTkFrame(self.left_frame, width=850, height = 100, fg_color="yellow", corner_radius=0)
        self.top_frame.pack(side = TOP, fill=X)
        self.top_frame.pack_propagate(False)
        
        self.middle_frame = ctk.CTkFrame(self.left_frame, width=850, height=500, fg_color="blue", corner_radius=0)
        self.middle_frame.pack(side = TOP, fill=BOTH)
        self.middle_frame.pack_propagate(False)
        
        self.bottom_frame = ctk.CTkFrame(self.left_frame, width=850, height = 100, fg_color="yellow", corner_radius=0)
        self.bottom_frame.pack(side = TOP, fill=X)
        self.bottom_frame.pack_propagate(False)

        self.middle_left_frame = ctk.CTkFrame(self.middle_frame, width = 50, height = 500, fg_color="green", corner_radius=0)
        self.middle_left_frame.pack(side=LEFT, fill=X)
        self.middle_left_frame.pack_propagate(False)
        
        self.middle_graph_frame = ctk.CTkFrame(self.middle_frame, width = 750, height = 500, fg_color="pink", corner_radius=0)
        self.middle_graph_frame.pack(side=LEFT, fill=Y)
        self.middle_graph_frame.pack_propagate(False)

        self.middle_right_frame = ctk.CTkFrame(self.middle_frame, width = 50, height = 500, fg_color="white", corner_radius=0)
        self.middle_right_frame.pack(side=LEFT, fill=X)
        self.middle_right_frame.pack_propagate(False)
        
    # Right Microwave Panel
    def setup_rightframe(self):
        # Setting up main right frame
        self.right_frame = ctk.CTkFrame(self.main_frame, width=450, height=700, fg_color="pink", corner_radius=0)
        self.right_frame.pack(side=TOP, fill=Y)
        self.right_frame.pack_propagate(False)

        # Frame to be used to display the current status
        self.status_frame = ctk.CTkFrame(self.right_frame, width=500, height=100, fg_color="blue", corner_radius=0)
        self.status_frame.pack(side=TOP, fill=X)
        self.status_frame.pack_propagate(False)

        # Frame to be used to display the current stage (knob)
        self.stage_frame = ctk.CTkFrame(self.right_frame, width=500, height=350, fg_color="purple", corner_radius=0)
        self.stage_frame.pack(side=TOP, fill=X)
        self.stage_frame.pack_propagate(False)

        # Frame to be used to display the option buttons
        self.option_frame = ctk.CTkFrame(self.right_frame, width=500, height=150, fg_color="green", corner_radius=0)
        self.option_frame.pack(side=TOP, fill=X)
        self.option_frame.pack_propagate(False)
        
        """
        CODE FOR THE OPTION BUTTONS
        """
        self.information_button = ctk.CTkButton(self.option_frame, image=self.info_img, width=30, 
                                                height=70, hover_color='blue', corner_radius=100,
                                                border_width=5, border_color="black")
        self.information_button.configure(fg_color='white', text="")
        self.information_button.pack(side=LEFT, padx=(30,0))

        self.test_button1 = ctk.CTkButton(self.option_frame, image=self.temperature_img, width=30, 
                                          height=90, hover_color='blue', corner_radius=100,
                                          border_width=5, border_color="black")
        self.test_button1.configure(fg_color='white', text="")
        self.test_button1.pack(side=LEFT, padx=30)

        self.test_button2 = ctk.CTkButton(self.option_frame, 
                                          image=self.export_img, width=30, height=70, 
                                          hover_color='blue', corner_radius=100, 
                                          border_width=5, border_color="black")
        self.test_button2.configure(fg_color='white', text="")
        self.test_button2.pack(side=LEFT, padx=(0,20))

        """
        CODE FOR THE STATUS DISPLAY
        """
        self.status_border = ctk.CTkFrame(self.status_frame, width=370, height=75, 
                                          fg_color="pink", corner_radius=20,
                                          border_color="black", border_width=5)
        self.status_border.pack(side=TOP, fill=Y, pady=(10,5))
        self.status_border.pack_propagate(False)

        """
        CODE FOR THE STAGE DISPLAY 
        """
        
        """"
        CODE FOR THE GRAPH
        """
    def setup_graph(self):
        # Create a figure and axis
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Generate sample data (sine wave)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, label="Sine Wave")
        
        # Customize graph appearance
        ax.set_title("Temperature vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°C)")
        ax.legend()
        
        # Embed the Matplotlib figure in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.middle_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

if __name__ == "__main__": 
    window = ctk.CTk()
    app = MainApp(window)
    window.mainloop()