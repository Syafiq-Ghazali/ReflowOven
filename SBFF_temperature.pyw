from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MainApp:
    def __init__(self, window):
        # Setting up the window
        self.window = window
        self.window.title('SBFFs: Temperature Monitor')
        self.window.geometry('1000x600')
        self.window.configure(bg='gray13')
        self.window.minsize(1000, 600)
        self.window.maxsize(1920, 1080)

        self.setup_microwave()
        self.setup_leftframe()
        self.setup_rightframe()
    
    def setup_microwave(self):
        self.main_frame = ctk.CTkFrame(self.window, width=1000, height=600, corner_radius=0)
        self.main_frame.pack(side=TOP, fill=BOTH)
        self.main_frame.pack_propagate(False)
    
    def setup_leftframe(self):
        self.left_frame = ctk.CTkFrame(self.main_frame, width=650, height=600, fg_color="blue", corner_radius=0)
        self.left_frame.pack(side=LEFT, fill=BOTH)
        self.left_frame.pack_propagate(False)

    def setup_rightframe(self):
        self.right_frame = ctk.CTkFrame(self.main_frame, width=350, height=600, fg_color="red", corner_radius=0)
        self.right_frame.pack(side=LEFT, fill=BOTH)
        self.right_frame.pack_propagate(False)

if __name__ == "__main__":
    window = Tk()
    app = MainApp(window)
    window.mainloop()