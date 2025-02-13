import numpy as np
import sys, time, math
import pandas as pd
import serial
import os
from tkinter import Tk, filedialog

# Initialize the Tkinter root window (hidden)
root = Tk()
root.withdraw()

# Configure the serial port
ser = serial.Serial(
    port='COM5',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

# Buffer for averaging temperature values
buffer = []
buffer_size = 9

# Global variables
excel_file = None
current_second = 0

def choose_save_location():
    global excel_file
    file_path = filedialog.asksaveasfilename(
        defaultextension='.xlsx',
        filetypes=[("Excel files", "*.xlsx")],
        title="Choose location to save temperature log"
    )
    if file_path:  # If user didn't cancel the dialog
        excel_file = file_path
        start_logging()

def start_logging():
    # Initialize the Excel file with headers if it doesn't exist
    if not os.path.exists(excel_file):
        df = pd.DataFrame(columns=["Time (s)", "Temperature (°C)", "Timestamp"])
        df.to_excel(excel_file, index=False)
    
    # Start reading from the serial port
    read_serial()

def read_serial():
    global current_second, buffer
    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(",")

            if len(parts) == 3:
                temp_c = float(parts[0].strip())
                new_state = float(parts[1].strip())
                t = float(parts[2].strip())

                # Take the average of 9 values
                buffer.append(temp_c)
                if len(buffer) == buffer_size:
                    temp_c_avg = sum(buffer) / buffer_size
                    buffer = []  # Reset buffer after using it

                    print(f"temp: {temp_c_avg}, state: {new_state}, time: {t}")
                    log_to_excel(temp_c_avg)

            time.sleep(1)  # Adjust the sleep time as needed

    except KeyboardInterrupt:
        print("Logging stopped by user.")
    finally:
        ser.close()

def log_to_excel(temperature):
    """
    Logs the timestamp (in seconds) and temperature to an Excel file.
    """
    global current_second
    current_second += 1  # Increment the second counter
    
    data = {
        "Time (s)": [current_second],
        "Temperature (°C)": [temperature],
        "Timestamp": [time.strftime("%Y-%m-%d %H:%M:%S")]
    }
    df = pd.DataFrame(data)

    try:
        # Append to the existing file
        existing_df = pd.read_excel(excel_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(excel_file, index=False)
    except Exception as e:
        print(f"Error saving to Excel: {e}")

# Ask the user where to save the file
choose_save_location()