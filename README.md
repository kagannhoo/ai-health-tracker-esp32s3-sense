<div align="center">
Physio-Emotion Monitor
Image & Sensor-Based Status Detection System
<p align="center">
<b>Integrated Health Monitoring System</b>


Combining AI-powered Computer Vision with Embedded Biometric Sensors.


<i>Developed for Computer Hardware & Operating Systems Course</i>
</p>
About • Core Logic • Hardware • Installation
</div>
 About the Project
Physio-Emotion Monitor analyzes the user's emotional state via facial expression recognition while simultaneously measuring heart rate (BPM) and blood oxygen saturation (SpO2). The primary objective is to fuse physiological and psychological data on a single dashboard for real-time status detection.
Key Features
Face & Emotion Analysis: Real-time emotion detection (Happy, Sad, Fear, Angry, etc.) using OpenCV and Roboflow inference models.
 Physiological Tracking: Non-invasive monitoring of Heart Rate (BPM) and SpO2 levels via fingertip sensor using MAX30102.
 Wireless Video Streaming: Low-latency MJPEG video streaming over Wi-Fi using the ESP32-S3.
Modern Dashboard: A Python-based GUI featuring a "Glassmorphism" design aesthetic for data visualization.
 Core Logic Highlights
The system relies on asynchronous communication to merge data streams. Here is the actual logic behind the fusion:
 Python: Async Serial & AI Fusion
We use threading to prevent the UI from freezing while waiting for sensor data packets.
import threading
import serial

# Thread function to read biometric data asynchronously
def read_serial_data():
    global bpm, spo2
    while running:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("DATA:"):
                # Protocol: "DATA:BPM,SpO2" -> e.g., "DATA:75,98"
                parts = line.split(":")[1].split(",")
                bpm = int(parts[0])
                spo2 = int(parts[1])
        except Exception as e:
            print(f"Serial Error: {e}")

# Main Loop: Roboflow Inference
if frame_count % 3 == 0:  # Optimization: Skip frames
    results = model.infer(frame)[0]
    emotion = results.predictions[0].class_name
    confidence = results.predictions[0].confidence
    
    # Update UI based on Emotion + Biometric Data
    update_dashboard(emotion, bpm, spo2)


 ESP32 (C++): Sensor Processing & Streaming
The ESP32 reads raw IR data, detects heartbeats, and sends formatted packets to the PC.
void loop() {
  // 1. Read Raw Sensor Data
  long irValue = particleSensor.getIR();

  // 2. Heart Beat Detection Algorithm
  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);
    
    // Smooth the value using average array
    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++) beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }

  // 3. Send Data Packet (Serialized)
  if (currentMillis - previousMillis >= 100) {
    Serial.print("DATA:");
    Serial.print(beatAvg);
    Serial.print(",");
    Serial.println(spo2);
    previousMillis = currentMillis;
  }
}


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
1. Firmware Setup (ESP32)
Open the .ino file located in arduino_code using Arduino IDE.
Install libraries via Library Manager:
ESP32 Board Manager (Seeed Studio XIAO ESP32S3)
SparkFun MAX3010x Pulse and Proximity Sensor
Adafruit SSD1306 & Adafruit GFX
Update Wi-Fi credentials:
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASS";


Upload and open Serial Monitor (115200 baud) to get the IP Address.
2. Client Setup (Python)
Ensure Python 3.x is installed. Install dependencies:
pip install opencv-python numpy pyserial inference


3. Usage
Open python_app/main.py.
Update configuration:
URL = "[http://192.168.1.](http://192.168.1.)XXX/stream"  # Your ESP32 IP
SERIAL_PORT = "COM3"                  # Your USB Port


Run the dashboard:
python main.py


 Screenshots & Results
<div align="center">
<table>
<tr>
<td align="center"><b>System Prototype</b></td>
<td align="center"><b>Dashboard (Angry State)</b></td>
</tr>
<tr>
<td><img src="images/donanim.jpg" width="400" alt="Prototype"></td>
<td><img src="images/sonuc2.jpeg" width="400" alt="Angry Result"></td>
</tr>
<tr>
<td align="center"><b>Disgust State</b></td>
<td align="center"><b>Dashboard Interface</b></td>
</tr>
<tr>
<td><img src="images/sonuc1.jpeg" width="400" alt="Disgust Result"></td>
<td><img src="images/sonuc3.jpeg" width="400" alt="Dashboard"></td>
</tr>
</table>
<p><i>Note: Heart rate values may fluctuate in correlation with instantaneous emotional changes.</i></p>
</div>
Directory Structure
Physio-Emotion-Monitor/
├── arduino_code/       # C++ source code for ESP32 firmware
├── python_app/         # Python scripts for PC interface and AI inference
├── images/             # Project assets, diagrams, and screenshots
└── README.md           # Project documentation


Disclaimer
This project is intended for educational and research purposes only. It is not a medical device. The measurements provided are for reference and should not be used for medical diagnosis or treatment.
Security Note: Ensure your Roboflow API Key is kept private and not committed to public repositories.
<div align="center">
 Developers
Kağan Hacıosmanoğlu   |   İsmail Yasir Güney
GitHub: @kagannhoo



Bilecik Sheikh Edebali University - Management Information Systems
</div>
