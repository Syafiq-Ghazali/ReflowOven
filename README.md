# Reflow Oven Controller (8051 Assembly)

## Overview
This project implements a **multi-stage reflow oven controller** written in **8051 Assembly**. The oven cycles through temperature stages used in PCB soldering. The system monitors temperature and switches between stages automatically. Transitions are based on time and temperature thresholds.

## Features
- Multi-stage reflow process (Preheat, Soak, Reflow, Cool)
- Real-time temperature monitoring
- Implemented fully in 8051 Assembly
- Custom **Tkinter interface** for monitoring and control developed in Python
- Developed collaboratively in a team environment

## How It Works
The 8051 assembly code handles temperature reading and stage control directly on the microcontroller. A Python Tkinter interface displays the current temperature, stage, and process status in real time. The oven’s heater is regulated through a PWM channel
