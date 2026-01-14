# esp32s3sense-and-max30102-project
A hybrid health monitoring system combining real-time AI emotion analysis with biometric data (BPM &amp; SpO2) using ESP32S3 Sense and MAX30102.

# AI-Powered Physiological & Emotional Health Monitor

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Hardware](https://img.shields.io/badge/Hardware-ESP32--S3-red)
![AI](https://img.shields.io/badge/AI-Roboflow-purple)

## About the Project

Bu proje,NabD1z & SpO2 ve yapay zeka destekli duygu analizini birleEtiren hibrit bir saDlD1k izleme sistemidir.

Sistem, Seeed Studio XIAO ESP32S3 Sense kartD1 kullanarak Wi-Fi C<zerinden gC6rC<ntC< aktarD1mD1 yapar ve aynD1 anda MAX30102 sensC6rC< ile parmaktan nabD1z verisi okur. Bilgisayarda C'alD1Ean Python yazD1lD1mD1, bu verileri iEler, Roboflow tabanlD1 yapay zeka modeli ile yC<z ifadesinden duygu analizi yapar ve fiziksel + duygusal stresi C6lC'erek modern bir arayC<zde sunar.

This project is a hybrid health monitoring system that combines biometric data (BPM & SpO2) with AI-powered emotion analysis.

## Features

* ** GerC'ek ZamanlD1 Fizyolojik Takip
    * NabD1z (BPM) C6lC'C<mC<.
    * Kandaki Oksijen (SpO2) C6lC'C<mC<.
* ** Yapay Zeka Duygu Analizi:
    * YC<z ifadelerinden anlD1k duygu tespiti (Mutlu, CzgC<n, KD1zgD1n, Korku, EaEkD1n, NC6tr).
    * **Roboflow Inference motoru entegrasyonu.
* ** Kablosuz GC6rC<ntC< AktarD1mD1:
    * ESP32-S3 Sense C<zerinden MJPEG video akD1ED1.
* ** Modern ArayC<z (Medical HUD):
    * OpenCV tabanlD1 "Glassmorphism" tasarD1mD1.
    * Dinamik ilerleme C'ubuklarD1 (Progress Bars).
    * Anti-Flicker (GC6rC<ntC< Sabitleme) teknolojisi.
* ** Hibrit Stres Analizi:
    * YC<ksek nabD1z ve negatif yC<z ifadelerini birleEtirerek stres seviyesi tahmini.


## Hardware Requirements

1.  **Seeed Studio XIAO ESP32S3 Sense (Kamera ModC<lC< Dahil)
2.  **MAX30102 (NabD1z ve Oksijen SensC6rC<)
3.  **SSD1306 OLED Ekran (0.96 inch - I2C)
4.  BaDlantD1 KablolarD1 (Jumper Wires)
5.  Breadboard


## Installation

### 1. Arduino (ESP32) 
1.  `Arduino IDE` C<zerinden gerekli kC<tC<phaneleri yC<kleyin:
    * `SparkFun MAX3010x Pulse and Proximity Sensor Library`
    * `Adafruit SSD1306` & `Adafruit GFX`
2.  `kutuphaneli_final.ino` dosyasD1nD1 aC'D1n.
3.  Wi-Fi bilgilerinizi (`ssid`, `password`) gC<ncelleyin.
4.  Kodu **XIAO ESP32S3** kartD1na yC<kleyin.
   * *Not: PSRAM: "OPI PSRAM" seC'ili olmalD1dD1r.

### 2. Python (PC) 
1.  Python 3.10 veya daha yeni bir sC<rC<m yC<kleyin.
2.  Gerekli kC<tC<phaneleri terminalden yC<kleyin:
    ```bash
    pip install opencv-python numpy pyserial inference roboflow
    ```
3.  `script.py` dosyasD1nD1 aC'D1n.
4.  `URL` kD1smD1na OLED ekranda yazan IP adresini girin.
5.  `ROBOFLOW_API_KEY` kD1smD1na kendi API anahtarD1nD1zD1 girin.
6.  Kodu C'alD1EtD1rD1n:
    ```bash
    python script.py
    ```
## Screenshots

<img width="962" height="753" alt="Ekran gC6rC<ntC<sC< 2026-01-14 180242" src="https://github.com/user-attachments/assets/bb481c7c-4906-49d4-adec-4a8332ec3c8f" />

<img width="974" height="758" alt="Ekran gC6rC<ntC<sC< 2026-01-14 180146" src="https://github.com/user-attachments/assets/965f81b9-d641-4b5c-9531-09ec938f9fd2" />

## Disclaimer

Bu proje eDitim ve hobi amaC'lD1dD1r. TD1bbi bir cihaz deDildir. GerC'ek tD1bbi teEhis ve tedavi iC'in kullanD1lmamalD1dD1r.
This project is for educational purposes only. It is not a medical device.


## Author

**[Yasir GCNEY / Kagan HACIOSMANODgLU]**
Github:url{https://github.com/kagannhoo}
