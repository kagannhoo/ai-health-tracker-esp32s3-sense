#include "esp_camera.h"
#include <WiFi.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "esp_http_server.h"

// KULLANICI AYARLARI
const char* ssid = "YOUR HOTSPOT NAME";      
const char* password = "YOUR HOTSPOT PASSWORDS"; 

// XIAO ESP32S3 Sense Pinleri
#define I2C_SDA_PIN 5 
#define I2C_SCL_PIN 6 

// OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// SENSÖR
MAX30105 particleSensor;
const byte RATE_SIZE = 4; 
byte rates[RATE_SIZE]; 
byte rateSpot = 0;
long lastBeat = 0;
int beatAvg = 0;

// SpO2 Değişkenleri
double avered = 0; double aveir = 0;
double sumirrms = 0; double sumredrms = 0;
int i = 0; int Num = 100; 
double ESpO2 = 95.0; double FSpO2 = 0.7; double frate = 0.95;
int spo2_final = 0;

// KAMERA PİNLERİ
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     10
#define SIOD_GPIO_NUM     40
#define SIOC_GPIO_NUM     39
#define Y9_GPIO_NUM       48
#define Y8_GPIO_NUM       11
#define Y7_GPIO_NUM       12
#define Y6_GPIO_NUM       14
#define Y5_GPIO_NUM       16
#define Y4_GPIO_NUM       18
#define Y3_GPIO_NUM       17
#define Y2_GPIO_NUM       15
#define VSYNC_GPIO_NUM    38
#define HREF_GPIO_NUM     47
#define PCLK_GPIO_NUM     13

httpd_handle_t stream_httpd = NULL;

esp_err_t stream_handler(httpd_req_t *req){
  camera_fb_t * fb = NULL;
  esp_err_t res = ESP_OK;
  size_t _jpg_buf_len = 0;
  uint8_t * _jpg_buf = NULL;
  char * part_buf[64];

  static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=frame";
  static const char* _STREAM_BOUNDARY = "\r\n--frame\r\n";
  static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

  res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
  if(res != ESP_OK){ return res; }

  while(true){
    fb = esp_camera_fb_get();
    if (!fb) { Serial.println("Kamera yakalama hatasi"); res = ESP_FAIL; break; }
    _jpg_buf_len = fb->len;
    _jpg_buf = fb->buf;

    if(res == ESP_OK){
      size_t hlen = snprintf((char *)part_buf, 64, _STREAM_PART, _jpg_buf_len);
      res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
      if(res == ESP_OK) res = httpd_resp_send_chunk(req, (const char *)part_buf, hlen);
      if(res == ESP_OK) res = httpd_resp_send_chunk(req, (const char *)_jpg_buf, _jpg_buf_len);
    }
    esp_camera_fb_return(fb);
    if(res != ESP_OK){ break; }
  }
  return res;
}

void startCameraServer(){
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 80; 
  httpd_uri_t stream_uri = {
    .uri       = "/stream",
    .method    = HTTP_GET,
    .handler   = stream_handler, 
    .user_ctx  = NULL
  };
  if (httpd_start(&stream_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &stream_uri);
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { Serial.println("OLED Yok"); }
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("Sistem Aciliyor...");
  display.display();

  if (particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    byte ledBrightness = 0x1F; 
    byte sampleAverage = 4; 
    byte ledMode = 2; 
    int sampleRate = 400; 
    int pulseWidth = 411; 
    int adcRange = 4096; 
    particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); 
  }

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  
  config.frame_size = FRAMESIZE_VGA; 
  config.pixel_format = PIXFORMAT_JPEG; 
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
 
  config.jpeg_quality = 10; 
  config.fb_count = 2;

  esp_camera_init(&config);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }

  startCameraServer(); 

  display.clearDisplay();
  display.setCursor(0,0);
  display.print("IP: "); display.println(WiFi.localIP());
  display.display();
}

void loop() {
  uint32_t irValue = particleSensor.getIR();
  uint32_t redValue = particleSensor.getRed(); 

  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    float bpm = 60 / (delta / 1000.0);
    if (bpm < 255 && bpm > 20) {
      rates[rateSpot++] = (byte)bpm; 
      rateSpot %= RATE_SIZE;
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++) beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }

  if (irValue > 50000) { 
    aveir = aveir * frate + (double)irValue * (1.0 - frate);
    avered = avered * frate + (double)redValue * (1.0 - frate);
    sumirrms += (irValue - aveir) * (irValue - aveir);
    sumredrms += (redValue - avered) * (redValue - avered);
    i++;
    if (i >= Num) { 
      double R = (sqrt(sumredrms) / avered) / (sqrt(sumirrms) / aveir);
      double spo2_calc = -45.060 * R * R + 30.354 * R + 94.845;
      ESpO2 = FSpO2 * ESpO2 + (1.0 - FSpO2) * spo2_calc;
      if(ESpO2 > 100) ESpO2 = 100;
      if(ESpO2 < 80) ESpO2 = 80;
      spo2_final = (int)ESpO2;
      sumirrms = 0.0; sumredrms = 0.0; i = 0;
    }
  } else {
    spo2_final = 0; beatAvg = 0;
  }

  static long lastUpdate = 0;
  if(millis() - lastUpdate > 100){
    Serial.print("DATA:");
    Serial.print(irValue > 50000 ? beatAvg : 0);
    Serial.print(",");
    Serial.println(irValue > 50000 ? spo2_final : 0);

    display.fillRect(0, 20, 128, 44, BLACK);
    if(irValue > 50000){
      display.setCursor(0, 25); display.setTextSize(2);
      display.print("BPM: "); display.println(beatAvg);
      display.setCursor(0, 45); display.setTextSize(1);
      display.print("SpO2: %"); display.println(spo2_final);
    } else {
      display.setCursor(0, 25); display.setTextSize(1);
      display.println("Parmak Yok");
    }
    display.display();
    lastUpdate = millis();
  }
}
