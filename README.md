esp32s3sense-and-max30102-project
A hybrid health monitoring system combining real-time AI emotion analysis with biometric data (BPM & SpO2) using ESP32S3 Sense and MAX30102.

AI-Powered Physiological & Emotional Health Monitor
Project Status Python Hardware AI

About the Project
Bu proje,Nabız & SpO2 ve yapay zeka destekli duygu analizini birleştiren hibrit bir sağlık izleme sistemidir.

Sistem, Seeed Studio XIAO ESP32S3 Sense kartı kullanarak Wi-Fi üzerinden görüntü aktarımı yapar ve aynı anda MAX30102 sensörü ile parmaktan nabız verisi okur. Bilgisayarda çalışan Python yazılımı, bu verileri işler, Roboflow tabanlı yapay zeka modeli ile yüz ifadesinden duygu analizi yapar ve fiziksel + duygusal stresi ölçerek modern bir arayüzde sunar.

This project is a hybrid health monitoring system that combines biometric data (BPM & SpO2) with AI-powered emotion analysis.

Features
** Gerçek Zamanlı Fizyolojik Takip
Nabız (BPM) ölçümü.
Kandaki Oksijen (SpO2) ölçümü.
** Yapay Zeka Duygu Analizi:
Yüz ifadelerinden anlık duygu tespiti (Mutlu, Üzgün, Kızgın, Korku, Şaşkın, Nötr).
**Roboflow Inference motoru entegrasyonu.
** Kablosuz Görüntü Aktarımı:
ESP32-S3 Sense üzerinden MJPEG video akışı.
** Modern Arayüz (Medical HUD):
OpenCV tabanlı "Glassmorphism" tasarımı.
Dinamik ilerleme çubukları (Progress Bars).
Anti-Flicker (Görüntü Sabitleme) teknolojisi.
** Hibrit Stres Analizi:
Yüksek nabız ve negatif yüz ifadelerini birleştirerek stres seviyesi tahmini.
Hardware Requirements
**Seeed Studio XIAO ESP32S3 Sense (Kamera Modülü Dahil)
**MAX30102 (Nabız ve Oksijen Sensörü)
**SSD1306 OLED Ekran (0.96 inch - I2C)
Bağlantı Kabloları (Jumper Wires)
Breadboard
Installation
1. Arduino (ESP32)
Arduino IDE üzerinden gerekli kütüphaneleri yükleyin:
SparkFun MAX3010x Pulse and Proximity Sensor Library
Adafruit SSD1306 & Adafruit GFX
kutuphaneli_final.ino dosyasını açın.
Wi-Fi bilgilerinizi (ssid, password) güncelleyin.
Kodu XIAO ESP32S3 kartına yükleyin.
*Not: PSRAM: "OPI PSRAM" seçili olmalıdır.
2. Python (PC)
Python 3.10 veya daha yeni bir sürüm yükleyin.
Gerekli kütüphaneleri terminalden yükleyin:
pip install opencv-python numpy pyserial inference roboflow
script.py dosyasını açın.
URL kısmına OLED ekranda yazan IP adresini girin.
ROBOFLOW_API_KEY kısmına kendi API anahtarınızı girin.
Kodu çalıştırın:
python script.py
Screenshots
<img width="1110" height="869" alt="Ekran görüntüsü 2026-01-14 184600" src="https://github.com/user-attachments/assets/5d7e5506-9f72-45a4-b1cf-3aa5827536a7" />
<img width="1113" height="862" alt="Ekran görüntüsü 2026-01-14 184614" src="https://github.com/user-attachments/assets/9a7afd71-0002-4750-8631-0cc4a0b160db" />

Disclaimer
Bu proje eğitim ve hobi amaçlıdır. Tıbbi bir cihaz değildir. Gerçek tıbbi teşhis ve tedavi için kullanılmamalıdır. This project is for educational purposes only. It is not a medical device.

Author
[Yasir GÜNEY / Kağan HACIOSMANOĞLU]
