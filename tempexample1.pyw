import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime

class ModernTemperatureMonitor:
    def __init__(self):
        # Setup window
        self.window = ctk.CTk()
        self.window.title("Temperature Monitor")
        self.window.geometry("1000x600")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main layout
        self.create_layout()
        
        # Initialize data
        self.temperatures = []
        self.times = []
        self.recording = False

    def create_layout(self):
        # Create main containers
        left_panel = ctk.CTkFrame(self.window, width=200)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        right_panel = ctk.CTkFrame(self.window)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Temperature display
        self.temp_label = ctk.CTkLabel(
            left_panel,
            text="25.0°C",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.temp_label.pack(pady=20)

        # Status indicator
        self.status_frame = ctk.CTkFrame(left_panel, fg_color="#1f538d")
        self.status_frame.pack(fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="NORMAL",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.status_label.pack(pady=10)

        # Control buttons
        self.start_button = ctk.CTkButton(
            left_panel,
            text="Start Recording",
            command=self.toggle_recording,
            font=ctk.CTkFont(size=14)
        )
        self.start_button.pack(pady=5)

        self.export_button = ctk.CTkButton(
            left_panel,
            text="Export Data",
            command=self.export_data,
            font=ctk.CTkFont(size=14)
        )
        self.export_button.pack(pady=5)

        # Settings
        settings_frame = ctk.CTkFrame(left_panel)
        settings_frame.pack(fill="x", padx=10, pady=20)

        ctk.CTkLabel(
            settings_frame,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)

        # Update interval slider
        ctk.CTkLabel(
            settings_frame,
            text="Update Interval (ms):"
        ).pack()
        
        self.interval_slider = ctk.CTkSlider(
            settings_frame,
            from_=100,
            to=2000,
            number_of_steps=19
        )
        self.interval_slider.pack(padx=10, pady=5)
        self.interval_slider.set(1000)

        # Temperature range
        ctk.CTkLabel(
            settings_frame,
            text="Display Range:"
        ).pack()
        
        self.range_slider = ctk.CTkSlider(
            settings_frame,
            from_=10,
            to=100,
            number_of_steps=90
        )
        self.range_slider.pack(padx=10, pady=5)

        # Theme switcher
        theme_switch = ctk.CTkSwitch(
            settings_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        theme_switch.pack(pady=10)
        theme_switch.select()  # Default to dark mode

        # Setup matplotlib graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Style the plot
        self.ax.set_facecolor('#2B2B2B')
        self.fig.patch.set_facecolor('#2B2B2B')
        self.ax.grid(True, color='#555555')
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_color('white')

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
        # Update plot colors
        bg_color = '#2B2B2B' if new_mode == "dark" else '#FFFFFF'
        text_color = 'white' if new_mode == "dark" else 'black'
        
        self.ax.set_facecolor(bg_color)
        self.fig.patch.set_facecolor(bg_color)
        self.ax.tick_params(colors=text_color)
        for spine in self.ax.spines.values():
            spine.set_color(text_color)
        self.canvas.draw()

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            self.start_button.configure(text="Stop Recording")
            self.update_data()
        else:
            self.start_button.configure(text="Start Recording")

    def update_data(self):
        if not self.recording:
            return
            
        # Simulate temperature data (replace with serial data)
        current_time = len(self.times)
        temperature = 25 + 5 * np.sin(current_time * 0.1)
        
        self.times.append(current_time)
        self.temperatures.append(temperature)
        
        # Update display
        self.temp_label.configure(text=f"{temperature:.1f}°C")
        
        # Update status
        if temperature > 28:
            self.status_frame.configure(fg_color="#8B0000")
            self.status_label.configure(text="HIGH TEMP")
        elif temperature < 22:
            self.status_frame.configure(fg_color="#00008B")
            self.status_label.configure(text="LOW TEMP")
        else:
            self.status_frame.configure(fg_color="#1f538d")
            self.status_label.configure(text="NORMAL")

        # Update plot
        self.ax.clear()
        self.ax.plot(self.times[-int(self.range_slider.get()):], 
                    self.temperatures[-int(self.range_slider.get()):], 
                    color='#00FF00', linewidth=2)
        self.ax.grid(True, color='#555555')
        self.canvas.draw()
        
        # Schedule next update
        self.window.after(int(self.interval_slider.get()), self.update_data)

    def export_data(self):
        # Add export functionality here
        pass

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernTemperatureMonitor()
    app.run()
