from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time, math
import numpy as np
import serial, serial.tools.list_ports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import kconvert
import tkinter.filedialog as filedialog
from customtkinter import CTkComboBox

"""
CONFIGURE SERIAL PORT
"""
"""
ser = serial.Serial(
port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()
"""
""""
COLORSCHEME
"""
# Light White: #FFEBEB
# Dark Pink: #EE7C9A
# Reddish Pink: #C30130
# Maroon: #32000C
# Grey Pink: #D996A8

class MainApp:
    def __init__(self, window):
        # Setting up the window
        self.window = window
        self.window.title('SBFFs: Temperature Monitor')
        self.window.geometry('1300x700')
        self.window.configure(bg='gray13')
        self.window.minsize(1300, 700)
        self.window.maxsize(1300, 700)

        self.temp_type = StringVar(value = "C") #set temperature initially in celcius

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
        self.dial_display_img = ctk.CTkImage(Image.open("dial-display.png"), size=(450,320))
        self.dial_img = ctk.CTkImage(Image.open("dial.png"), size=(150,150))

    #The whole Microwave
    def setup_microwave(self):
        self.main_frame = ctk.CTkFrame(self.window, width=1300, height=700, fg_color="red", corner_radius=0)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.main_frame.pack_propagate(False)

    def setup_leftframe(self):
        self.left_frame = ctk.CTkFrame(self.main_frame, width= 850, height = 700, fg_color="white", corner_radius=0)
        self.left_frame.pack(side =LEFT, fill =X)
        self.left_frame.pack_propagate(False)
        
        self.top_frame = ctk.CTkFrame(self.left_frame, width=850, height = 100, fg_color="#FFEBEB", corner_radius=0)
        self.top_frame.pack(side = TOP, fill=X)
        self.top_frame.pack_propagate(False)
        
        self.middle_frame = ctk.CTkFrame(self.left_frame, width=850, height=500, fg_color="#FFEBEB", corner_radius=0)
        self.middle_frame.pack(side = TOP, fill=BOTH)
        self.middle_frame.pack_propagate(False)
        
        self.bottom_frame = ctk.CTkFrame(self.left_frame, width=850, height = 100, fg_color="#FFEBEB", corner_radius=0)
        self.bottom_frame.pack(side = TOP, fill=X)
        self.bottom_frame.pack_propagate(False)

        self.middle_left_frame = ctk.CTkFrame(self.middle_frame, width = 50, height = 500, fg_color="#FFEBEB", corner_radius=0)
        self.middle_left_frame.pack(side=LEFT, fill=X)
        self.middle_left_frame.pack_propagate(False)
        
        self.middle_graph_frame = ctk.CTkFrame(self.middle_frame, width = 750, height = 500, fg_color="pink", border_width=5,
                                               border_color="#32000C", corner_radius=0)
        self.middle_graph_frame.pack(side=LEFT, fill=Y)
        self.middle_graph_frame.pack_propagate(False)

        self.middle_right_frame = ctk.CTkFrame(self.middle_frame, width = 50, height = 500, fg_color="#FFEBEB", corner_radius=0)
        self.middle_right_frame.pack(side=LEFT, fill=X)
        self.middle_right_frame.pack_propagate(False)

        self.setup_graph()  
        
    # Right Microwave Panel
    def setup_rightframe(self):
        # Setting up main right frame
        self.right_frame = ctk.CTkFrame(self.main_frame, width=450, height=700, 
                                        fg_color="#EE7C9A", corner_radius=0)
        self.right_frame.pack(side=TOP, fill=Y)
        self.right_frame.pack_propagate(False)

        # Frame to be used to display the current status
        self.status_frame = ctk.CTkFrame(self.right_frame, width=500, height=100, fg_color="#EE7C9A", corner_radius=0)
        self.status_frame.pack(side=TOP, fill=X)
        self.status_frame.pack_propagate(False)

        # Frame to be used to display the current stage (knob)
        self.stage_frame = ctk.CTkFrame(self.right_frame, width=500, height=400, fg_color="#EE7C9A", corner_radius=0)
        self.stage_frame.pack(side=TOP, fill=X)
        self.stage_frame.pack_propagate(False)

        # Frame to be used to display the option buttons
        self.option_frame = ctk.CTkFrame(self.right_frame, width=500, height=150, fg_color="#EE7C9A", corner_radius=0)
        self.option_frame.pack(side=TOP, fill=X)
        self.option_frame.pack_propagate(False)
        
        """
        CODE FOR THE OPTION BUTTONS
        """
        self.information_button = ctk.CTkButton(self.option_frame, image=self.info_img, width=30, 
                                                height=70, fg_color="#FFEBEB", hover_color="#D996A8", corner_radius=100,
                                                border_width=5, border_color="black")
        self.information_button.configure(fg_color='white', text="")
        self.information_button.pack(side=LEFT, padx=(30,0))

        self.temperature_button = ctk.CTkButton(self.option_frame, image=self.temperature_img, width=30, 
                                          height=90, fg_color="#FFEBEB", hover_color="#D996A8", corner_radius=100,
                                          border_width=5, border_color="#32000C", command=self.toggle_temp)
        self.temperature_button.configure(fg_color='white', text="")
        self.temperature_button.pack(side=LEFT, padx=30)

        self.export_button = ctk.CTkButton(self.option_frame, 
                                          image=self.export_img, width=30, height=70, 
                                          corner_radius=100, 
                                          border_width=5, border_color="black",
                                          fg_color="#FFEBEB", hover_color="#D996A8", command = self.open_export)
        self.export_button.configure(fg_color='white', text="")
        self.export_button.pack(side=LEFT, padx=(0,20))

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
        self.stage_title = ctk.CTkLabel(self.stage_frame, text="STAGE", font=("Arial", 40, "bold"), text_color="#32000C")
        self.stage_title.pack(side=TOP, fill=X, anchor="center", pady=(27))

        # Set dial_display (background image)
        self.dial_display = ctk.CTkLabel(self.stage_frame, image=self.dial_display_img, text="")
        self.dial_display.place(relx=0.5, rely=0.585, anchor="center")

        # Set dial (foreground image, on top of display)
        self.dial = ctk.CTkLabel(self.stage_frame, image=self.dial_img, text="")
        self.dial.place(relx=0.5, rely=0.585, anchor="center")
    """
    EXPORT DATA WINDOW
    """
    def open_export(self):
        #centre later !!!!!! :(((((
        # Create Export Window
        self.export_window = ctk.CTkToplevel(self.window)
        self.export_window.title("Export Options")
        self.export_window.geometry("500x290")
        self.export_window.configure(bg= "#D996A8")
        self.export_window.attributes("-topmost", 1)

        self.export_top_frame = ctk.CTkFrame(self.export_window, width = 500, height = 70, fg_color="#32000C", corner_radius = 0)
        self.export_top_frame.pack(side = TOP, fill=BOTH, expand=True)
        self.export_top_frame.pack_propagate(True)

        self.export_bottom_frame = ctk.CTkFrame(self.export_window, width = 500, height = 220, fg_color="#FFEBEB", corner_radius = 0)
        self.export_bottom_frame.pack(side = TOP, fill=X, expand=True)
        self.export_bottom_frame.pack_propagate(False)

        self.export_format_frame = ctk.CTkFrame(self.export_bottom_frame, width = 500, height = 100, fg_color="#FFEBEB", corner_radius=0)
        self.export_format_frame.pack(side = TOP, fill=X, anchor="center",expand=True)
        self.export_format_frame.pack_propagate(False)

        # Label
        self.export_title = ctk.CTkLabel(self.export_top_frame, text="Select Export Options:", font=("Helvetica", 30, "bold"), text_color="white")
        self.export_title.pack(side=TOP, fill=BOTH, anchor="center", padx=10, pady=(10,0))

        self.seperator_frame = ctk.CTkFrame(self.export_top_frame, width=600, height=10, fg_color="white", corner_radius=0)
        self.seperator_frame.pack(side=BOTTOM, fill=X, expand=False)
        self.seperator_frame.pack_propagate(False)

        # Multi-Select Listbox
        self.export_format = ctk.CTkComboBox(self.export_format_frame, values = ["CSV", "PNG", "Excel", "PDF"], width = 300, height=100, font=("Helvetica", 25, "bold"), 
                                             dropdown_font=("Helvetica", 20, "bold"), fg_color="#D996A8", dropdown_fg_color="#FFEBEB", button_color="#32000C", text_color="black", 
                                             dropdown_text_color="black", dropdown_hover_color="#D996A8")
        self.export_format.pack(side=BOTTOM, expand=True, fill=BOTH, padx=30, pady=10)
        self.export_format.set("---")

        # Confirm Button
        confirm_button = ctk.CTkButton(self.export_bottom_frame, text="Export", fg_color="#D996A8", hover_color="#EE7C9A", command=self.export_data, font=("Helvetica", 20, "bold"), 
        text_color="black", height=60, width=300)
        confirm_button.pack(pady=30, padx=50)

    def export_data(self): #average every 10 values since the serial port updates every 10s
        #Fetch selected export format and save data accordingly.
        export_type = self.export_format.get()  # Get selected format from combobox

        if not export_type:
            print("No export format selected")
            return

        # Ask the user where to save the file
        filetypes = {
            "CSV": [("CSV files", "*.csv")],
            "PNG": [("PNG image", "*.png")],
            "Excel": [("Excel files", "*.xlsx")],
            "PDF": [("PDF files", "*.pdf")]
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=filetypes[export_type][0][1], 
            filetypes=filetypes[export_type]
        )

        if not file_path:
            print("No file selected")
            return  # User canceled save
        
        # Handle export logic
        if export_type == "CSV":
            import csv
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time (s)", f"Temperature (°{self.temp_type.get()})"])
                writer.writerows(zip(self.xdata, self.ydata))
        
        elif export_type == "PNG":
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight")

        elif export_type == "Excel":
            import pandas as pd
            df = pd.DataFrame({"Time (s)": self.xdata, f"Temperature (°{self.temp_type.get()})": self.ydata})
            df.to_excel(file_path, index=False)

        elif export_type == "PDF":
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight", format="pdf")

        print(f"File saved: {file_path}")

    """
    TEMPERATURE C/F BUTTON CONFIGURATION
    """

    def toggle_temp(self):
        if self.temp_type.get() == "C":
            self.temp_type.set("F")
            print(f"Current temp type: {self.temp_type.get()}")  # Debugging print statement
        else:
            self.temp_type.set("C")
            print(f"Current temp type: {self.temp_type.get()}")  # Debugging print statement
        # Update the graph y-axis label based on the temperature type
        self.ax.set_ylabel(f"TEMPERATURE (°{self.temp_type.get()})", fontsize=25, color='white')
        self.fig.canvas.draw_idle()  # Redraw the graph to reflect the changes
    
    """"
    GRAPH
    """

    """
    GENERATE DATA VALUES TO PLOT
    """

    def data_gen(self):
        t = self.data_gen.t  # Initialize time
        while True:
            t += 1
            temp = np.sin(0.1*t)*100 +100
            #temp = np.exp(-0.05 * t) * 100  # Example: Decaying exponential for temperature simulation
            #temp = self.ser.readline().decode('utf-8').strip()
            #values = string.split(",")
            #hj, cj = map(lambda x: float(x.strip()), values) #get hot and cold junction voltage readings 
            #temp=round(kconvert.mV_to_C(hj, cj),1) #convert mv to C
            #if temp_type is F, convert to fahrienheit
            if self.temp_type.get() == "F":
                temp *= float(9/5)
                temp += 32
            #print(temp)
            yield t, temp

    data_gen.t = -1
    """
    SCROLLING FUNCTION
    """
    def run(self, data):
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)

        if t > self.xsize:  # Scroll to the left
            self.ax.set_xlim(t - self.xsize, t)

        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def on_close_figure(self, event):
        sys.exit(0)

    """
    GRAPH SETUP
    """
    def setup_graph(self):
        self.xsize = 100  # Define X-axis size
        self.fig, self.ax = plt.subplots(figsize=(15, 10))  # Adjust width and height

        # change colour 

        self.ax.set_facecolor("black")  # Change background color of the graph
        self.fig.patch.set_facecolor("black")  # Change outer figure background

        # Initialize line plot
        self.line, = self.ax.plot([], [], lw=2, label = "Temperature", color = 'red')
        self.ax.set_ylim(0, 250)
        self.ax.set_xlim(0, self.xsize)
        self.ax.grid(color='grey', linewidth=0.5, )
        self.ax.tick_params(axis='both', labelsize=18, colors='white')  

        # Increase Number of Gridlines
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Grid every 5 seconds
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(10))  # Grid every 10°C

        # Add Minor Gridlines
        self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Minor grid every 1s
        self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))  # Minor grid every 5°C

        self.ax.grid(True, which='major', color='gray', linewidth=1)
        self.ax.grid(True, which='minor', color='gray', linestyle=':', linewidth=0.5)

        hfont = {'font':'Arial', 'fontweight':'bold'}

        # Set labels
        self.ax.set_xlabel("TIME (s)", **hfont, fontsize=25, color='white')
        self.ax.set_ylabel(f"TEMPERATURE (°{self.temp_type.get()})", **hfont, fontsize=25, color='white')
        self.ax.set_title("REFLOW OVEN TEMPERATURE READINGS", **hfont, fontsize=30, color='white')

        # Initialize data list
        self.xdata, self.ydata = [], []

        # Create an annotation (cursor temperature display)
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(25, 25),
                                    textcoords="offset points",
                                    bbox=dict(boxstyle="round,pad=0.5", fc="pink", ec="black", lw=2),
                                    arrowprops=dict(arrowstyle="->", color="white"), **hfont,
                                    fontsize=18)
        self.annot.set_visible(False)  # Hide initially

        # Start graph animation
        self.ani = animation.FuncAnimation(
            self.fig, 
            self.run, 
            self.data_gen, 
            blit=False, 
            interval=100, 
            repeat=False,
            save_count=100  # Add this line to specify max frames to cache
        )
        # Connect hover event
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)

        # Embed Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.middle_graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    """
    CODE FOR THE CURSOR HOVER DISPLAY
    """
    def on_hover(self, event):
        if event.inaxes == self.ax:  # Check if mouse is inside the graph area
            x_cursor = event.xdata  # Get x-coordinate of cursor
            if x_cursor is None or len(self.xdata) == 0:
                return

            # Find the nearest x-value in self.xdata
            nearest_idx = min(range(len(self.xdata)), key=lambda i: abs(self.xdata[i] - x_cursor))
            x_nearest, y_nearest = self.xdata[nearest_idx], self.ydata[nearest_idx]

            # Update annotation position and text
            self.annot.xy = (x_nearest, y_nearest)
            self.annot.set_text(f"Time: {x_nearest:.1f}s\nTemp: {y_nearest:.1f}°°{self.temp_type.get()}")
            self.annot.set_visible(True)

            self.fig.canvas.draw_idle()  # Redraw to show annotation
        else:
            self.annot.set_visible(False)
            self.fig.canvas.draw_idle()


if __name__ == "__main__": 
    window = ctk.CTk()
    app = MainApp(window)
    window.mainloop()
