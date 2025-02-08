from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk

class MainApp:
    def __init__(self, window):
        # Setting up the window
        self.window = window
        self.window.title('SBFFs: Temperature Monitor')
        self.window.geometry('1000x750')
        self.window.configure(bg='gray13')
        self.window.minsize(1000, 750)
        self.window.maxsize(1000, 750)

        # Main windows
        self.setup_microwave()
        self.setup_leftframe()
        self.setup_rightframe()

    def setup_microwave(self):
        self.main_frame = ctk.CTkFrame(self.window, width=1000, height=750, fg_color="red", corner_radius=0)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.main_frame.pack_propagate(False)

    def setup_leftframe(self):
        self.left_frame = ctk.CTkFrame(self.main_frame, width=650, height=750, fg_color="black", corner_radius=0)
        self.left_frame.pack(side=LEFT, fill=Y)  # Fill only vertically
        self.left_frame.pack_propagate(False)

    def setup_rightframe(self):
        self.right_frame = ctk.CTkFrame(self.main_frame, width=350, height=750, fg_color='#161616', corner_radius=0)
        self.right_frame.pack(side=RIGHT, fill=Y)  # ✅ Fix: Make it stick to the right
        self.right_frame.pack_propagate(False)

        # Debugging label to confirm it's showing up
        debug_label = ctk.CTkLabel(self.right_frame, text="Right Frame", fg_color="white", text_color="black")
        debug_label.pack(fill=BOTH)

        self.status_frame = ctk.CTkFrame(self.right_frame, width=350, height=150, fg_color='#161616', corner_radius=0)
        self.status_frame.pack(side=TOP, fill=X)
        self.status_frame.pack_propagate(False)

        self.stage_frame = ctk.CTkFrame(self.right_frame, width=350, height=200, fg_color="green", corner_radius=0)
        self.stage_frame.pack(side=TOP, fill=X)
        self.stage_frame.pack_propagate(False)

        self.microwave_options_frame = ctk.CTkFrame(self.right_frame, width=350, height=150, fg_color="pink", corner_radius=0)
        self.microwave_options_frame.pack(side=TOP, fill=X)
        self.microwave_options_frame.pack_propagate(False)

        self.filler_frame = ctk.CTkFrame(self.right_frame, width=350, height=50, fg_color="black", corner_radius=0)
        self.filler_frame.pack(side=TOP, fill=X)
        self.filler_frame.pack_propagate(False)

if __name__ == "__main__":
    window = Tk()
    app = MainApp(window)
    window.mainloop()
