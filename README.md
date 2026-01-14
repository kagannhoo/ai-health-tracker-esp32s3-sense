# ai-health-tracker-esp32s3-sense
"Real-time health monitoring system combining facial emotion analysis (AI) and physiological sensor data (BPM/SpO2) using ESP32 and Python."
 Physio-Emotion Monitor: Image & Sensor-Based Status Detection
This project is an integrated health monitoring system developed within the scope of the Computer Hardware and Operating Systems course. It combines AI-powered computer vision with embedded sensor data to provide a holistic view of a user's state.
 About the Project
The system analyzes the user's emotional state via facial expression recognition while simultaneously measuring heart rate (BPM) and blood oxygen saturation (SpO2). The primary objective is to fuse physiological and psychological data on a single dashboard for real-time status detection.
Key Features
Face & Emotion Analysis: Real-time emotion detection (Happy, Sad, Fear, Angry, etc.) using OpenCV and Roboflow inference models.
Physiological Tracking: Non-invasive monitoring of Heart Rate (BPM) and SpO2 levels via fingertip sensor.
Wireless Video Streaming: Low-latency MJPEG video streaming over Wi-Fi using the ESP32-S3.
Modern Dashboard: A Python-based GUI featuring a "Glassmorphism" design aesthetic for data visualization.
 Hardware Requirements
The following hardware components are required to replicate this project:
Component
Model / Description
Microcontroller
Seeed Studio XIAO ESP32S3 Sense
Biometric Sensor
MAX30102 (Pulse Oximeter & Heart-Rate Sensor)
Display
0.96" I2C OLED Display (SSD1306)
Camera Module
OV2640 (Integrated with ESP32 Sense)
Misc
Breadboard, Jumper Wires

 Installation & Setup
Follow the steps below to set up the environment on your local machine.
1. Firmware Setup (ESP32)
Open the .ino file located in the arduino_code directory using the Arduino IDE.
Ensure the following libraries are installed via the Library Manager:
ESP32 Board Manager (Select Seeed Studio XIAO ESP32S3 or your specific board)
SparkFun MAX3010x Pulse and Proximity Sensor Library
Adafruit SSD1306 & Adafruit GFX Library
Update the ssid and password variables in the code with your Wi-Fi credentials.
Upload the code to the board and open the Serial Monitor (Baud Rate: 115200) to note the assigned IP Address.
2. Client Setup (Python)
Ensure Python 3.x is installed on your computer. Install the required dependencies using pip:
pip install opencv-python numpy pyserial inference


3. Usage
Open the python_app/main.py file in your preferred IDE.
Update the configuration variables with the IP address obtained from the ESP32:
URL = "[http://192.168.1.](http://192.168.1.)XXX/stream"  # Replace with your ESP32 IP
SERIAL_PORT = "COM3"                  # Check your device manager for the correct port


Run the application:
python main.py


 Screenshots & Results
System Prototype
Test Results
Emotion: Angry
<img width="1113" height="862" alt="Ekran görüntüsü 2026-01-14 184614" src="https://github.com/user-attachments/assets/295ab1d2-b2f6-4a84-bc11-137c4e1ee89a" />

Emotion: Disgust
<img width="1110" height="869" alt="Ekran görüntüsü 2026-01-14 184600" src="https://github.com/user-attachments/assets/5c855b8d-01f1-4586-8a27-2ad99613949c" />



> Note: Heart rate values may fluctuate in correlation with instantaneous emotional changes.
Directory Structure
├── arduino_code/       # C++ source code for ESP32 firmware
├── python_app/         # Python scripts for PC interface and AI inference
├── images/             # Project assets, diagrams, and screenshots
└── README.md           # Project documentation


 Disclaimer
This project is intended for educational and research purposes only. It is not a medical device. The measurements provided are for reference and should not be used for medical diagnosis or treatment.
> Security Note: Ensure your Roboflow API Key is kept private and not committed to public repositories.
 Developers
Kağan Hacıosmanoğlu
İsmail Yasir Güney
GitHub: https://github.com/kagannhoo
Institution: Bilecik Sheikh Edebali University - Management Information Systems

