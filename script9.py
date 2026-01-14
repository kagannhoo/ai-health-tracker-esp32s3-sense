import cv2
import numpy as np
import serial
import time
import threading
from inference import get_model

#İP PORT VE BAUND AYARLARI
URL = "http://YOUR İP"
SERIAL_PORT = "YOUR COM"
BAUD_RATE = 115200

# API KEY VE MODEL ID
ROBOFLOW_API_KEY = "YOUR APİ KEY"
ROBOFLOW_MODEL_ID = "yuz-verilerinden-duygu-analizi/1"

# RENK PALETİ
C_DARK_BG = (30, 30, 40)  # Koyu Lacivert/Gri Arkaplan
C_WHITE = (245, 245, 245)  # Kırık Beyaz
C_TEAL = (255, 200, 0)  # Turkuaz (Normal Durum)
C_WARNING = (0, 165, 255)  # Turuncu (Uyarı)
C_DANGER = (80, 80, 255)  # Mercan Kırmızısı (Tehlike)
C_SUCCESS = (100, 255, 100)  # Yumuşak Yeşil
C_GLASS = (20, 20, 20)  # Panel Rengi

# GLOBAL DEĞİŞKENLER
bpm = 0;
spo2 = 0;
status = "Sistem Hazir..."
running = True
current_emotion = "Analiz Ediliyor..."
emotion_color = C_WHITE

# HAFIZA DEĞİŞKENLERİ
last_known_face = None
last_known_emotion = "Araniyor..."
last_known_color = C_WHITE
missing_frame_count = 0
MAX_MISSING_FRAMES = 10

# MODELLER
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("Yapay Zeka Modeli Yukleniyor...")
try:
    model = get_model(model_id=ROBOFLOW_MODEL_ID, api_key=ROBOFLOW_API_KEY)
    print("Model Hazir!")
except Exception as e:
    print(f"Model Hatasi: {e}");
    running = False


# SERİ PORT
def read_serial_data():
    global bpm, spo2, status, running
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while running:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("DATA:"):
                    parts = line.split(":")[1].split(",")
                    bpm = int(parts[0]);
                    spo2 = int(parts[1])
                    status = "VERI ALINIYOR" if bpm > 0 else "SENSOR BEKLENIYOR"
            except:
                pass
    except:
        status = "BAGLANTI YOK"


t = threading.Thread(target=read_serial_data);
t.daemon = True;
t.start()


# YARDIMCI FONKSİYONLAR
def draw_glass_panel(img, x, y, w, h, color=C_GLASS, alpha=0.6):
    """Yarı saydam (cam görünümlü) panel çizer"""
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    # İnce çerçeve
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1)


def draw_progress_bar(img, x, y, w, h, val, max_val, color):
    """Dolum çubuğu çizer"""
    # Arkaplan
    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), -1)
    # Dolum
    fill_w = int((val / max_val) * w)
    fill_w = min(fill_w, w)
    cv2.rectangle(img, (x, y), (x + fill_w, y + h), color, -1)
    # Çerçeve
    cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 1)


def get_physio_stress(bpm_val):
    if bpm_val == 0: return "VERI YOK", C_WHITE
    if bpm_val > 110: return "YUKSEK STRES", C_DANGER
    if bpm_val > 90: return "HEYECAN / AKTIF", C_WARNING
    return "NORMAL", C_SUCCESS


# ANA DÖNGÜ
print(f"Kamera Baslatiliyor: {URL}")
cap = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frame_count = 0

while running and cap.isOpened():
    try:
        ret, frame = cap.read()
        if not ret: time.sleep(1); cap.open(URL); continue

        frame = cv2.flip(frame, 0)
        frame_count += 1


        display_frame = cv2.resize(frame, (1000, 750))

        # YÜZ TAKİP VE AI
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) > 0:
            missing_frame_count = 0
            largest_face = max(faces, key=lambda r: r[2] * r[3])
            last_known_face = largest_face

            if frame_count % 3 == 0:
                try:
                    results = model.infer(frame)[0]
                    preds = results.predictions
                    top = max(preds, key=lambda x: preds[x].confidence)
                    conf = preds[top].confidence

                    # Renk ve Etiket Seçimi
                    lbl = top.lower()
                    if "mutlu" in lbl:
                        col = C_SUCCESS; txt = "MUTLU"
                    elif "uzgun" in lbl:
                        col = (230, 200, 50); txt = "UZGUN"  
                    elif "kizgin" in lbl:
                        col = C_DANGER; txt = "KIZGIN"
                    elif "korku" in lbl:
                        col = (50, 0, 200); txt = "KORKU"
                    elif "sasirma" in lbl:
                        col = C_WARNING; txt = "SASKIN"
                    elif "dogal" in lbl:
                        col = C_WHITE; txt = "NOTR"
                    elif "igrenc" in lbl:
                        col = (50, 150, 50); txt = "IGRENME"
                    else:
                        col = C_WARNING; txt = lbl.upper()

                    last_known_emotion = f"{txt} %{int(conf * 100)}"
                    last_known_color = col
                except:
                    pass
        else:
            missing_frame_count += 1

        # GÖRSEL TASARIM

        # A) Yüz Çerçevesi
        if missing_frame_count < MAX_MISSING_FRAMES and last_known_face is not None:
            (x, y, w, h) = last_known_face
            rx = int(x * (1000 / frame.shape[1]));
            ry = int(y * (750 / frame.shape[0]))
            rw = int(w * (1000 / frame.shape[1]));
            rh = int(h * (750 / frame.shape[0]))

            # Köşeli Çerçeve Çizimi
            line_len = int(rw / 4)
            thk = 3

            cv2.line(display_frame, (rx, ry), (rx + line_len, ry), last_known_color, thk)
            cv2.line(display_frame, (rx, ry), (rx, ry + line_len), last_known_color, thk)

            cv2.line(display_frame, (rx + rw, ry + rh), (rx + rw - line_len, ry + rh), last_known_color, thk)
            cv2.line(display_frame, (rx + rw, ry + rh), (rx + rw, ry + rh - line_len), last_known_color, thk)


            cv2.putText(display_frame, last_known_emotion, (rx, ry - 15),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, last_known_color, 1, cv2.LINE_AA)

        # SOL MENÜ
        draw_glass_panel(display_frame, 20, 20, 320, 450)

        # Başlık
        cv2.putText(display_frame, "MEDIKAL ANALIZ", (40, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.8, C_TEAL, 1, cv2.LINE_AA)
        cv2.line(display_frame, (40, 75), (320, 75), C_WHITE, 1)

        # 1. AI SONUCU
        cv2.putText(display_frame, "YUZ IFADESI", (40, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
                    cv2.LINE_AA)
        cv2.putText(display_frame, last_known_emotion.split(" ")[0], (40, 150), cv2.FONT_HERSHEY_DUPLEX, 1.2,
                    last_known_color, 1, cv2.LINE_AA)

        # 2. FİZYOLOJİK VERİLER
        phys_txt, phys_col = get_physio_stress(bpm)

        # Nabız Bölümü
        cv2.putText(display_frame, "NABIZ (BPM)", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
                    cv2.LINE_AA)
        cv2.putText(display_frame, str(bpm), (40, 240), cv2.FONT_HERSHEY_DUPLEX, 1.1, phys_col, 1, cv2.LINE_AA)
        # Nabız Barı
        draw_progress_bar(display_frame, 110, 215, 200, 15, bpm, 160, phys_col)

        # SpO2 Bölümü
        cv2.putText(display_frame, "SpO2 (%)", (40, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
                    cv2.LINE_AA)
        spo2_c = C_TEAL if spo2 > 95 else C_DANGER
        cv2.putText(display_frame, str(spo2), (40, 320), cv2.FONT_HERSHEY_DUPLEX, 1.1, spo2_c, 1, cv2.LINE_AA)
        # SpO2 Barı
        draw_progress_bar(display_frame, 110, 295, 200, 15, spo2, 100, spo2_c)

        # 3. GENEL DURUM
        cv2.line(display_frame, (40, 350), (320, 350), (100, 100, 100), 1)
        cv2.putText(display_frame, "STRES DUZEYI", (40, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
                    cv2.LINE_AA)
        cv2.putText(display_frame, phys_txt, (40, 420), cv2.FONT_HERSHEY_TRIPLEX, 0.7, phys_col, 1, cv2.LINE_AA)

        # Alt Bilgi
        cv2.putText(display_frame, f"DURUM: {status}", (20, 730), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1,
                    cv2.LINE_AA)

        cv2.imshow("Medical AI Dashboard Pro", display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    except Exception as e:
        time.sleep(0.01)

cap.release()

cv2.destroyAllWindows()
