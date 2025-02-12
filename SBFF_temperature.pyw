from tkinter import *
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk
from customtkinter import CTkComboBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time, math
import numpy as np
import serial, serial.tools.list_ports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import tkinter.filedialog as filedialog

"""
CONFIGURE SERIAL PORT 
"""
ser = serial.Serial(
port='COM5',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

"""COLOR SCHEME"""
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

        self.state=0.0

        self.temp_type = StringVar(value = "C") #set temperature initially in celcius

        # Cleanup after closing the window
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # Load Images
        self.load_images()
        
        # Main windows
        self.setup_microwave()
        self.setup_leftframe()
        self.setup_rightframe()
        self.dial_logic()

    """
    window closing cleanup function
    """
    def close_window(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        plt.close('all')
        self.window.quit()
        self.window.destroy()

    """GENERATE DATA VALUES TO PLOT"""
    
    def data_gen(self):
        """
        t = self.data_gen.t
        while True:
            t+=1
            temp_c= np.sin(0.1*t)*100
            temp_f = (temp_c * 9/5)+32

            yield t, temp_c, temp_f

    data_gen.t = -1
        """
    
        while True:
            line = ser.readline().decode('utf-8').strip()
            parts= line.split(",")

            if len(parts) == 3:
                try:
                    temp_c = float(parts[0].strip())
                    new_state = float(parts[1].strip())
                    t = float(parts[2].strip())
                    self.buffer.append(temp_c)
                    if len(self.buffer) == 9:
                        temp_c = sum(self.buffer) / 9

                    print(f"temp:{temp_c}, state:{self.state}, time:{t}")
                    temp_f = (temp_c * 9/5)+32

                    if new_state != self.state:
                        self.state = new_state
                        self.window.after(0, self.dial_logic)

                    yield temp_c, temp_f, t
                except ValueError:
                    print(f"Non numeric data recieved: {line}")
        

    # Loading in Images
    def load_images(self):
        self.export_img = ctk.CTkImage(Image.open("export-icon.png"), size=(25,25))
        self.info_img = ctk.CTkImage(Image.open("info-icon.png"), size=(25,25))
        self.temperature_img = ctk.CTkImage(Image.open("temperature-icon.png"), size=(30,30))
        self.dial_display_img = ctk.CTkImage(Image.open("dial-display.png"), size=(450,320))
        self.stage0_img = ctk.CTkImage(Image.open("stage0.png"), size=(120,120))
        self.stage1_img = ctk.CTkImage(Image.open("stage1.png"), size=(180,180))
        self.stage2_img = ctk.CTkImage(Image.open("stage2.png"), size=(120,120))
        self.stage3_img = ctk.CTkImage(Image.open("stage3.png"), size=(180,180))
        self.stage4_img = ctk.CTkImage(Image.open("stage4.png"), size=(180,180))
        self.stage5_img = ctk.CTkImage(Image.open("stage5.png"), size=(120,120))
        self.stage6_img = ctk.CTkImage(Image.open("stage6.png"), size=(180,180))
        self.back_img = ctk.CTkImage(Image.open("back.png"), size=(18,25))
        self.stages_img = ctk.CTkImage(Image.open("stages.png"), size=(25,22))
        self.voltage_img = ctk.CTkImage(Image.open("voltage.png"), size=(25,22))
        self.gangski_img = ctk.CTkImage(Image.open("gangski.jpg"), size=(800,600))

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
                                                border_width=5, border_color="#32000C",
                                                command=self.open_information)
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
                                          border_width=5, border_color="#32000C",
                                          fg_color="#FFEBEB", hover_color="#D996A8", command = self.open_export)
        self.export_button.configure(fg_color='white', text="")
        self.export_button.pack(side=LEFT, padx=(0,20))

        """
        CODE FOR THE STATUS DISPLAY
        """
        self.status_border = ctk.CTkFrame(self.status_frame, width=370, height=75, 
                                          fg_color="pink", corner_radius=20,
                                          border_color="#32000C", border_width=5)
        self.status_border.pack(side=TOP, fill=Y, pady=(10,5))
        self.status_border.pack_propagate(False)

        self.stage_title = ctk.CTkLabel(self.stage_frame, text="STAGE", font=("Arial", 40, "bold"), text_color="#32000C")
        self.stage_title.pack(side=TOP, fill=X, anchor="center", pady=(27))

        # Set dial_display (background image)
        self.dial_display = ctk.CTkLabel(self.stage_frame, image=self.dial_display_img, text="")
        self.dial_display.place(relx=0.5, rely=0.585, anchor="center")

    def dial_logic(self):
        """ Updates the dial display and status label based on the current state. """
        for widget in self.status_border.winfo_children():
            widget.destroy()

        # Define mapping of states to images and text
        state_mapping = {
            1.0: (self.stage1_img, "IN PROGRESS...", "#32000C"),
            2.0: (self.stage2_img, "IN PROGRESS...", "#32000C"),
            3.0: (self.stage3_img, "IN PROGRESS...", "#32000C"),
            4.0: (self.stage4_img, "IN PROGRESS...", "#32000C"),
            5.0: (self.stage5_img, "COOLING...", "#32000C"),
            6.0: (self.stage6_img, "DONE!", "#0B3D2E")
        }

        # Get the image and text for the current state, default to stage 0
        image, text, color = state_mapping.get(self.state, (self.stage0_img, "OVEN OFF", "#32000C"))

        # Update dial image
        self.dial = ctk.CTkLabel(self.stage_frame, image=image, text="")
        self.dial.place(relx=0.5, rely=0.585, anchor="center")

        # Update status label
        self.status = ctk.CTkLabel(
        self.status_border, font=("Arial", 25, "bold"), 
        text_color=color, text=text
        )
        self.status.pack(side=LEFT, padx=(20, 0))

    def open_information(self):
        self.info_window = ctk.CTkToplevel(self.window)  # Creates a new top-level window
        self.info_window.title("Information Page")
        self.info_window.geometry("800x700")  # Adjust the size as needed
        self.info_window.configure(bg="#32000C")  
        self.info_window.attributes("-topmost", 1)

        self.information_top()
        self.sidebar_menu()
        self.stage_content()

    def information_top(self):
        # Top Frame
        self.info_top_frame = ctk.CTkFrame(self.info_window, width=800, height=70, fg_color="#32000C", corner_radius=0)
        self.info_top_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.info_top_frame.pack_propagate(False)

        # Close Button
        self.close_button = ctk.CTkButton(self.info_top_frame, text="", image=self.back_img, 
                                            command=self.info_window.destroy, 
                                            width=25, height=50, fg_color="#32000C", hover_color="#800020")
        self.close_button.pack(side=LEFT, padx=(10,0), pady=5)

        self.info_title = ctk.CTkLabel(self.info_top_frame, text="Information", font=("Helvetica", 30, "bold"))
        self.info_title.pack(side=LEFT, padx=20, pady=5)
        
        # Main Frame
        self.info_main_frame = ctk.CTkFrame(self.info_window, width=800, height=630, fg_color="#32000C", corner_radius=0)
        self.info_main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.info_main_frame.pack_propagate(False)

    def sidebar_menu(self):
        # Left Side Bar
        self.info_side_menu_frame = ctk.CTkFrame(self.info_main_frame, width=150, height=630, fg_color="#32000C", corner_radius=0)
        self.info_side_menu_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.info_side_menu_frame.pack_propagate(False)

        self.stage_button = ctk.CTkButton(self.info_side_menu_frame, text="Stages", font=("Helvetica", 20, "bold"), 
                                            image=self.stages_img, 
                                            corner_radius=0, 
                                            width=100, height=50, 
                                            fg_color="#32000C", hover_color="#800020",
                                            anchor="w",
                                            command=self.open_stages)
        self.stage_button.pack(side=TOP, pady=(0,0), fill=X)
        self.stage_button.pack_propagate(False)

        self.voltage_button = ctk.CTkButton(self.info_side_menu_frame, text="SBFFS", font=("Helvetica", 20, "bold"), 
                                            image=self.voltage_img, 
                                            corner_radius=0, 
                                            width=100, height=50, 
                                            fg_color="#32000C", hover_color="#800020",
                                            anchor="w",
                                            command=self.open_voltages)
        self.voltage_button.pack(side=TOP, pady=(5,0), fill=X)
        self.voltage_button.pack_propagate(False)

        # Main content Frame
        self.main_content_frame = ctk.CTkFrame(self.info_main_frame, width=650, height = 630, fg_color="#D996A8", corner_radius=0)
        self.main_content_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.main_content_frame.pack_propagate(False)

    def stage_content(self):

        self.info_main_frame_top = ctk.CTkFrame(self.main_content_frame, width=650, height=110, fg_color="#7D3C4A", corner_radius=0)
        self.info_main_frame_top.pack(side=TOP, fill=BOTH, expand=True)
        self.info_main_frame_top.pack_propagate(False)

        self.seperator_frame = ctk.CTkFrame(self.main_content_frame, width=650, height=20, fg_color="white", corner_radius=0)
        self.seperator_frame.pack(side=TOP, fill=BOTH, expand=False)
        self.seperator_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self.main_content_frame, width=650, height=500, fg_color="#D996A8", corner_radius=0)
        self.content_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.content_frame.pack_propagate(False)

        self.setting_title = ctk.CTkLabel(self.info_main_frame_top, text="Stages", font=("Helvetica", 40, "bold"))
        self.setting_title.pack(side=LEFT, padx=25, pady=10)

        self.s1f = ctk.CTkFrame(self.content_frame, width=650, height=70, fg_color="#FFEBEB", corner_radius=30, border_color="#32000C", border_width=5)
        self.s1f.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=20)
        self.s1f.pack_propagate(False)

        self.s2f = ctk.CTkFrame(self.content_frame, width=650, height=70, fg_color="#FFEBEB", 
                         corner_radius=30, border_color="#32000C", border_width=5)
        self.s2f.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=20)
        self.s2f.pack_propagate(False)

        self.s3f = ctk.CTkFrame(self.content_frame, width=650, height=70, fg_color="#FFEBEB", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s3f.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=20)
        self.s3f.pack_propagate(False)

        self.s4f = ctk.CTkFrame(self.content_frame, width=650, height=70, fg_color="#FFEBEB", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s4f.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=20)
        self.s4f.pack_propagate(False)

        self.s5f = ctk.CTkFrame(self.content_frame, width=650, height=70, fg_color="#FFEBEB", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s5f.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=20)
        self.s5f.pack_propagate(False)

        # Stage 1
        self.s1_title = ctk.CTkLabel(
            self.s1f, 
            text="Stage 1: Preheat",
            font=("Helvetica", 24, "bold"),
            text_color="#32000C"
        )
        self.s1_title.pack(side=LEFT, padx=20, pady=10)

        self.s1if = ctk.CTkFrame(self.s1f, width=150, height=50, fg_color="#7D3C4A", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s1if.pack(anchor="e", fill=NONE, expand=True, pady=10, padx=20)
        self.s1if.pack_propagate(False)

        self.s1i_title = ctk.CTkLabel(
            self.s1if, 
            text="00:00",
            font=("Helvetica", 24, "bold"),
            text_color="#FFEBEB"
        )
        self.s1i_title.pack(anchor="center", padx=20, pady=10)

        # Stage 2
        self.s2_title = ctk.CTkLabel(
            self.s2f,
            text="Stage 2: Soak",
            font=("Helvetica", 24, "bold"),
            text_color="#32000C"
        )
        self.s2_title.pack(side=LEFT, padx=20, pady=10)

        self.s2if = ctk.CTkFrame(self.s2f, width=150, height=50, fg_color="#7D3C4A", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s2if.pack(anchor="e", fill=NONE, expand=True, pady=10, padx=20)
        self.s2if.pack_propagate(False)

        self.s2i_title = ctk.CTkLabel(
            self.s2if, 
            text="00:00",
            font=("Helvetica", 24, "bold"),
            text_color="#FFEBEB"
        )
        self.s2i_title.pack(anchor="center", padx=20, pady=10)

        # Stage 3
        self.s3_title = ctk.CTkLabel(
            self.s3f,
            text="Stage 3: Reflow",
            font=("Helvetica", 24, "bold"),
            text_color="#32000C"
        )
        self.s3_title.pack(side=LEFT, padx=20, pady=10)

        self.s3if = ctk.CTkFrame(self.s3f, width=150, height=50, fg_color="#7D3C4A", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s3if.pack(anchor="e", fill=NONE, expand=True, pady=10, padx=20)
        self.s3if.pack_propagate(False)

        self.s3i_title = ctk.CTkLabel(
            self.s3if, 
            text="00:00",
            font=("Helvetica", 24, "bold"),
            text_color="#FFEBEB"
        )
        self.s3i_title.pack(anchor="center", padx=20, pady=10)

        # Stage 4
        self.s4_title = ctk.CTkLabel(
            self.s4f,
            text="Stage 4: Cool",
            font=("Helvetica", 24, "bold"),
            text_color="#32000C"
        )
        self.s4_title.pack(side=LEFT, padx=20, pady=10)

        self.s4if = ctk.CTkFrame(self.s4f, width=150, height=50, fg_color="#7D3C4A", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s4if.pack(anchor="e", fill=NONE, expand=True, pady=10, padx=20)
        self.s4if.pack_propagate(False)

        self.s4i_title = ctk.CTkLabel(
            self.s4if, 
            text="00:00",
            font=("Helvetica", 24, "bold"),
            text_color="#FFEBEB"
        )
        self.s4i_title.pack(anchor="center", padx=20, pady=10)

        # Stage 5
        self.s5_title = ctk.CTkLabel(
            self.s5f,
            text="Stage 5: Complete",
            font=("Helvetica", 24, "bold"),
            text_color="#32000C"
        )
        self.s5_title.pack(side=LEFT, padx=20, pady=10)

        self.s5if = ctk.CTkFrame(self.s5f, width=150, height=50, fg_color="#7D3C4A", 
                                corner_radius=30, border_color="#32000C", border_width=5)
        self.s5if.pack(anchor="e", fill=NONE, expand=True, pady=10, padx=20)
        self.s5if.pack_propagate(False)

        self.s5i_title = ctk.CTkLabel(
            self.s5if, 
            text="00:00",
            font=("Helvetica", 24, "bold"),
            text_color="#FFEBEB"
        )
        self.s5i_title.pack(anchor="center", padx=20, pady=10)

    def voltage_content(self):
        self.info_main_frame_top = ctk.CTkFrame(self.main_content_frame, width=650, height=110, fg_color="#7D3C4A", corner_radius=0)
        self.info_main_frame_top.pack(side=TOP, fill=BOTH, expand=True)
        self.info_main_frame_top.pack_propagate(False)

        self.seperator_frame = ctk.CTkFrame(self.main_content_frame, width=650, height=20, fg_color="white", corner_radius=0)
        self.seperator_frame.pack(side=TOP, fill=BOTH, expand=False)
        self.seperator_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self.main_content_frame, width=650, height=500, fg_color="#D996A8", corner_radius=0)
        self.content_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.content_frame.pack_propagate(False)

        self.setting_title = ctk.CTkLabel(self.info_main_frame_top, text="SBFF's", font=("Helvetica", 40, "bold"))
        self.setting_title.pack(side=LEFT, padx=25, pady=10)

        #self.voltage_frame = ctk.CTkFrame(self.content_frame, width=650, height=300, fg_color="#FFEBEB", corner_radius=50, border_color="#32000C", border_width=5)
        #self.voltage_frame.pack(anchor="center", fill=X, expand=True, pady=10, padx=20)
        #self.voltage_frame.pack_propagate(False)

        self.voltage_formula = ctk.CTkLabel(self.content_frame, text="", image=self.gangski_img)
        self.voltage_formula.pack(anchor="center")

    def open_stages(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        self.stage_content()
    
    def open_voltages(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        self.voltage_content()

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
        self.export_top_frame.pack(side = TOP, fill=X, expand=True)
        self.export_top_frame.pack_propagate(True)

        self.export_bottom_frame = ctk.CTkFrame(self.export_window, width = 500, height = 220, fg_color="#D996A8", corner_radius = 0)
        self.export_bottom_frame.pack(side = TOP, fill=X, expand=True)
        self.export_bottom_frame.pack_propagate(False)

        self.export_format_frame = ctk.CTkFrame(self.export_bottom_frame, width = 500, height = 100, fg_color="#D996A8", corner_radius=0)
        self.export_format_frame.pack(side = TOP, fill=X, anchor="center",expand=True)
        self.export_format_frame.pack_propagate(False)

        # Label
        self.export_title = ctk.CTkLabel(self.export_top_frame, text="Select Export Options:", font=("Helvetica", 30, "bold"), text_color="white")
        self.export_title.pack(side=TOP, fill=BOTH, anchor="center", padx=10, pady=(20,15))
        
        """
        # Close Button 
        self.export_close_button = ctk.CTkButton(self.export_top_frame, text="", image=self.back_img, 
                                            command=self.info_window.destroy, 
                                            width=5, height=5, fg_color="#32000C", hover_color="#800020")
        self.export_close_button.pack(side=LEFT, padx=(0,0), pady=0)
        """
        self.seperator_frame = ctk.CTkFrame(self.export_top_frame, width=600, height=10, fg_color="white", corner_radius=0)
        self.seperator_frame.pack(side=BOTTOM, fill=X, expand=False)
        self.seperator_frame.pack_propagate(False)

        # Multi-Select Listbox
        self.export_format = ctk.CTkComboBox(self.export_format_frame, values = ["CSV", "PNG", "Excel", "PDF"], width = 300, height=100, font=("Helvetica", 25, "bold"), 
                                             dropdown_font=("Helvetica", 20, "bold"), fg_color="#7D3C4A", dropdown_fg_color="#FFEBEB", button_color="#32000C", text_color="white", 
                                             dropdown_text_color="black", dropdown_hover_color="#D996A8", corner_radius=15, border_color="#32000C", border_width=5)
        self.export_format.pack(side=BOTTOM, expand=True, fill=BOTH, padx=30, pady=(20,5))
        self.export_format.set("---")

        # Confirm Button
        confirm_button = ctk.CTkButton(self.export_bottom_frame, text="Export", fg_color="#FFEBEB", hover_color="#EE7C9A", command=self.export_data, font=("Helvetica", 20, "bold"), 
                        text_color="#32000C", height=60, width=300, border_color="#32000C", border_width=5, corner_radius=15)
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
                if self.temp_type.get() == "C":
                    writer.writerows(zip(self.xdata, self.ydata_c))
                elif self.temp_type.get() == "F":
                    writer.writerows(zip(self.xdata, self.ydata_f))

        elif export_type == "PNG":
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight")

        elif export_type == "Excel":
            import pandas as pd
            if self.temp_type.get() == "C":
                df = pd.DataFrame({"Time (s)": self.xdata, f"Temperature (°{self.temp_type.get()})": self.ydata_c})
            elif self.temp_type.get() == "F":
                df = pd.DataFrame({"Time (s)": self.xdata, f"Temperature (°{self.temp_type.get()})": self.ydata_f})
            df.to_excel(file_path, index=False)

        elif export_type == "PDF":
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight", format="pdf")

        print(f"File saved: {file_path}")

    """
    TEMPERATURE C/F BUTTON CONFIGURATION
    """

    def toggle_temp(self):
        hfont = {'font':'Arial', 'fontweight':'bold'}

        if self.temp_type.get() == "C":
            self.temp_type.set("F")
            self.line_c.set_visible(False)
            self.line_f.set_visible(True)
            print(f"Current temp type: {self.temp_type.get()}")  # Debugging print statement
            self.ax.set_ylabel(f"TEMPERATURE (°{self.temp_type.get()})", **hfont, fontsize=25, color='white')

        else:
            self.temp_type.set("C")
            self.line_f.set_visible(False)
            self.line_c.set_visible(True)
            print(f"Current temp type: {self.temp_type.get()}")  # Debugging print statement
            self.ax.set_ylabel(f"TEMPERATURE (°{self.temp_type.get()})", **hfont, fontsize=25, color='white')
        # Update the graph y-axis label based on the temperature type
        self.fig.canvas.draw_idle()  # Redraw the graph to reflect the changes
        self.update_axes()
    
    """GRAPH"""

    """SCROLLING"""

    def run(self, data):
        #if data is None:
        #    return self.line_c, self.line_f
        
        temp_c, temp_f, t = data
        self.xdata.append(t)
        self.ydata_c.append(temp_c)
        self.ydata_f.append(temp_f)

        if t > self.xsize:  # Scroll to the left
            self.ax.set_xlim(t - self.xsize, t)

        self.line_c.set_data(self.xdata, self.ydata_c)
        self.line_f.set_data(self.xdata, self.ydata_f)

        return self.line_c, self.line_f,

    def on_close_figure(self, event):
        sys.exit(0)

    """GRAPH SETUP"""

    def update_axes(self):
        # Update y-axis limits and grid settings based on the temp_type
        if self.temp_type.get() == "C":
            self.ax.set_ylim(0, 250)
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(10))  # Grid every 10°C
            self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))   # Minor grid every 5°C
        elif self.temp_type.get() == "F":
            self.ax.set_ylim(0, 500)
            self.ax.yaxis.set_major_locator(ticker.MultipleLocator(20))  # Grid every 20°F
            self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))  # Minor grid every 10°F
        
        hfont = {'font':'Arial', 'fontweight':'bold'}
        # Update the label with the correct temperature unit
        self.ax.set_ylabel(f"TEMPERATURE (°{self.temp_type.get()})", **hfont, fontsize=25, color='white')

        # Redraw the canvas to apply the changes
        self.fig.canvas.draw_idle()

    def setup_graph(self):
        #plt.close('all')

        self.xsize = 250  # Define X-axis size
        self.fig, self.ax = plt.subplots(figsize=(15, 10))  # Adjust width and height

        # change colour 

        self.ax.set_facecolor("black")  # Change background color of the graph
        self.fig.patch.set_facecolor("black")  # Change outer figure background

        # Initialize line plot
        self.line_c, = self.ax.plot([], [], lw=2, label = "Temperature (°C)", color = 'red')
        self.line_f, = self.ax.plot([], [], lw=2, label= "Temperature(°F)", color="#73e6ff", visible=False)
    
        self.ax.set_ylim(0, 250)
        self.ax.set_xlim(0, self.xsize)
        self.ax.grid(color='grey', linewidth=0.5, )
        self.ax.tick_params(axis='both', labelsize=5, colors='white')  

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
        self.ax.set_ylabel(f"TEMPERATURE (°C)", **hfont, fontsize=25, color='white')

        self.ax.set_title("REFLOW OVEN TEMPERATURE READINGS", **hfont, fontsize=30, color='white')

        # Initialize data list
        self.xdata, self.ydata_c, self.ydata_f = [], [], []

        # Create an annotation (cursor temperature display)
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(25, 25),
                                    textcoords="offset points",
                                    bbox=dict(boxstyle="round,pad=0.5", fc="#FFEBEB", ec="black", lw=2),
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

    """HOVER DISPLAY"""

    def on_hover(self, event):
        if event.inaxes == self.ax:  # Check if mouse is inside the graph area
            x_cursor = event.xdata  # Get x-coordinate of cursor
            if x_cursor is None or len(self.xdata) == 0:
                return

            # Find the nearest x-value in self.xdata
            nearest_idx = min(range(len(self.xdata)), key=lambda i: abs(self.xdata[i] - x_cursor))
            
            if self.temp_type.get() =="C":
                x_nearest, y_nearest = self.xdata[nearest_idx], self.ydata_c[nearest_idx]
            elif self.temp_type.get() == "F":
                x_nearest, y_nearest = self.xdata[nearest_idx], self.ydata_f[nearest_idx]

            # Update annotation position and text
            self.annot.xy = (x_nearest, y_nearest)
            self.annot.set_text(f"Time: {x_nearest:.1f}s\nTemp: {y_nearest:.1f}°{self.temp_type.get()}")
            self.annot.set_visible(True)

            self.fig.canvas.draw_idle()  # Redraw to show annotation
        else:
            self.annot.set_visible(False)
            self.fig.canvas.draw_idle()

if __name__ == "__main__": 
    window = ctk.CTk()
    app = MainApp(window)
    window.mainloop()