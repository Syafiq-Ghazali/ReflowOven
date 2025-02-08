from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ctk

class CameraSettings:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Set up UI components here
        self.setup_main_frame_top()
        self.setup_title_frame()
        self.setup_switch_frame()
        self.setup_divider()
        self.setup_camera_connection_frame()
        self.setup_camera_live_frame()

    def load_images(self):
        self.back_img = ctk.CTkImage(Image.open("back-img.png"))
        self.help_button_img = ctk.CTkImage(Image.open("help-button.png"))
        self.user_settings_img = ctk.CTkImage(Image.open("user-settings.png"))
        self.video_camera_settings_img = ctk.CTkImage(Image.open("video-camera.png"))
        self.on_photo_img = ctk.CTkImage(Image.open("power-on.png"))
        self.off_photo_img = ctk.CTkImage(Image.open("power-off.png"))

    def setup_main_frame_top(self):
        self.main_frame_top = ctk.CTkFrame(self.master, fg_color='#161616', height=200, corner_radius=0)
        self.main_frame_top.pack(side=TOP, fill=X)
        self.main_frame_top.pack_propagate(False)

    def setup_title_frame(self):
        self.title_frame = ctk.CTkFrame(self.main_frame_top, width=320, fg_color='#151615', corner_radius=0)
        self.title_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.title_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(self.title_frame, text='Camera\nConnection', font=('Bold',40), justify=LEFT, text_color='white')
        self.title_label.pack(side=TOP, fill=Y, padx=30, anchor='nw', expand=TRUE)

    def switcher(self):
        current_value = self.connection_switch_var.get()
        print(f"Switch toggled: {current_value}")

        if current_value == "off":
            print("Switch is now off")

        else:
            print("Switch is now on")

    def setup_switch_frame(self):
        self.switch_frame = ctk.CTkFrame(self.main_frame_top, width=320, fg_color='#151615', corner_radius=0)
        self.switch_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.switch_frame.pack_propagate(False)

        self.connection_switch_var = ctk.StringVar(value="off")

        self.connection_switch = ctk.CTkSwitch(
            self.switch_frame, 
            text='', 
            switch_width=200, 
            switch_height=80, 
            command=self.switcher, 
            variable=self.connection_switch_var, 
            onvalue="on", 
            offvalue="off", 
            border_color='grey93',
            fg_color='#ab3130',
            progress_color='#7a9163', 
            border_width=5,
        )
        self.connection_switch.pack(expand=TRUE, side=TOP, pady=(20, 10))

    def setup_divider(self):
        self.divider = ctk.CTkFrame(self.master, fg_color='grey93', height=5, width=300, corner_radius=0)
        self.divider.pack(side=TOP, fill=X)

    def setup_camera_connection_frame(self):
        self.connection_large_frame = ctk.CTkFrame(self.master, fg_color='#202120', width=320, corner_radius=0)
        self.connection_large_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.connection_large_frame.pack_propagate(False)

        self.connection_small_frame = ctk.CTkFrame(self.connection_large_frame, fg_color='#202020', width=300, height=150, 
                                                   corner_radius=20, border_color='grey93', border_width=2)
        self.connection_small_frame.pack(side=TOP, expand=TRUE, padx=15, pady=15)
        self.connection_small_frame.pack_propagate(False)

        self.connection_title_frame = ctk.CTkFrame(self.connection_small_frame, width=280, height=20, fg_color='#202020')
        self.connection_title_frame.pack(side=TOP, expand=TRUE, pady=5)
        self.connection_title_frame.pack_propagate(False)

        self.connection_label = ctk.CTkLabel(self.connection_title_frame, text='Connection Status', font=('Bold',18), text_color='white')
        self.connection_label.pack(side=LEFT, anchor='nw', padx=20)

        self.connection_status_image = ctk.CTkButton(self.connection_title_frame, text='', width=15, height=15, fg_color='red')
        self.connection_status_image.pack(side=RIGHT, padx=20)

        self.connection_status_data_frame = ctk.CTkFrame(self.connection_small_frame, width=250, height=70, 
                                                         corner_radius=20, fg_color='grey93')
        self.connection_status_data_frame.pack(side=TOP, fill=X, padx=15, pady=5, expand=TRUE)
        self.connection_status_data_frame.pack_propagate(False)

        self.connection_status_data = ctk.CTkLabel(self.connection_status_data_frame, text='Not Connected', font=("Bold", 15), 
                                                   text_color='#161515')
        self.connection_status_data.pack(side=LEFT, anchor='w', padx=20, fill=Y)

    def setup_camera_live_frame(self):
        self.live_large_frame = ctk.CTkFrame(self.master, fg_color='#202120', width=320, corner_radius=0)
        self.live_large_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.live_large_frame.pack_propagate(False)

        self.live_small_frame = ctk.CTkFrame(self.live_large_frame, fg_color='#202020', width=300, height=150, 
                                             corner_radius=20, border_color='grey93', border_width=2)
        self.live_small_frame.pack(side=TOP, expand=TRUE, padx=15, pady=15)
        self.live_small_frame.pack_propagate(False)

        self.live_title_frame = ctk.CTkFrame(self.live_small_frame, width=280, height=20, fg_color='#202020')
        self.live_title_frame.pack(side=TOP, expand=TRUE, pady=5)
        self.live_title_frame.pack_propagate(False)

        self.live_label = ctk.CTkLabel(self.live_title_frame, text='Live Status', font=('Bold',18), text_color='white')
        self.live_label.pack(side=LEFT, anchor='nw', padx=20)

        self.live_status_image = ctk.CTkButton(self.live_title_frame, text='', width=15, height=15, fg_color='red')
        self.live_status_image.pack(side=RIGHT, padx=20)

        self.live_status_data_frame = ctk.CTkFrame(self.live_small_frame, width=250, height=70, corner_radius=20, fg_color='grey93')
        self.live_status_data_frame.pack(side=TOP, fill=X, padx=15, pady=5, expand=TRUE)
        self.live_status_data_frame.pack_propagate(False)

        self.live_status_data = ctk.CTkLabel(self.live_status_data_frame, text='Not Live', font=("Bold", 15), text_color='#161515')
        self.live_status_data.pack(side=LEFT, anchor='w', padx=20, fill=Y)