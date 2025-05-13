#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <SD.h>
#include <SPI.h>

// 引脚定义
const int trigPin = 11;      // 超声波 Trigger 引脚
const int echoPin = 12;      // 超声波 Echo 引脚
const int buzzerPin = 9;     // 蜂鸣器引脚
const int gpsTxPin = 4;      // GPS 模块 TX 引脚
const int gpsRxPin = 3;      // GPS 模块 RX 引脚
const int gsrPin = A0;       // GSR 传感器引脚
const int chipSelect = 4;    // SD 卡 CS 引脚

// GPS 模块初始化
TinyGPSPlus gps;
SoftwareSerial gpsSerial(gpsRxPin, gpsTxPin); // GPS 使用软串口通信

// 超声波测距变量
long duration;     // Echo 持续时间
float distanceCm;  // 测得的距离（厘米）

void setup() {
  // 初始化串行通信
  Serial.begin(9600);
  gpsSerial.begin(9600);
  Serial.println("系统初始化完成！");

  // 初始化引脚模式
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(gsrPin, INPUT);

  // 初始化蜂鸣器状态
  digitalWrite(buzzerPin, LOW);

  // 初始化 SD 卡
  Serial.print("正在初始化 SD 卡...");
  if (!SD.begin(chipSelect)) {
    Serial.println("SD 卡初始化失败，请检查连接！");
    while (1); // 如果初始化失败，停止程序
  }
  Serial.println("SD 卡初始化成功！");

  // 创建或打开 CSV 文件并写入标题
  File dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Timestamp,Distance(cm),GSR,Latitude,Longitude");
    dataFile.close();
  } else {
    Serial.println("无法创建或打开数据文件！");
    while (1); // 如果文件无法创建，停止程序
  }
}

void loop() {
  // 测量超声波距离
  measureDistance();

  // 检测 GSR 值
  int gsrValue = analogRead(gsrPin);

  // 记录时间戳
  unsigned long timestamp = millis() / 1000;

  // 获取 GPS 数据
  float latitude = 0.0, longitude = 0.0;
  bool gpsValid = readGPSData(latitude, longitude);

  // 写入数据到 SD 卡
  if (writeDataToSD(timestamp, distanceCm, gsrValue, latitude, longitude, gpsValid)) {
    Serial.println("数据成功写入 SD 卡！");
  } else {
    Serial.println("无法写入数据到 SD 卡！");
  }

  // 如果距离小于等于 1.5 米，蜂鸣器响
  if (distanceCm > 0 && distanceCm <= 150) {
    activateBuzzer();
  } else {
    deactivateBuzzer();
  }

  delay(3000); // 每 3 秒运行一次
}

// 测量超声波距离
void measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  if (duration == 0) {
    Serial.println("测距失败，超时！");
    distanceCm = -1; // 测距失败时设置为 -1
  } else {
    distanceCm = (duration * 0.0343) / 2;  // 计算距离（厘米）
    Serial.print("距离: ");
    Serial.print(distanceCm);
    Serial.println(" cm");
  }
}

// 激活蜂鸣器
void activateBuzzer() {
  tone(buzzerPin, 500); // 蜂鸣器发出 500Hz 的声音
  delay(400);           // 声音持续 400 毫秒
  noTone(buzzerPin);    // 停止蜂鸣器发声
  Serial.println("蜂鸣器长响！");
}

// 停止蜂鸣器
void deactivateBuzzer() {
  noTone(buzzerPin);
  Serial.println("蜂鸣器停止！");
}

// 获取 GPS 数据
bool readGPSData(float &latitude, float &longitude) {
  bool gpsValid = false;
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      if (gps.location.isValid()) {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
        Serial.print("当前位置：纬度 ");
        Serial.print(latitude, 6);
        Serial.print(" ，经度 ");
        Serial.println(longitude, 6);
        gpsValid = true;
      } else {
        Serial.println("GPS 信号无效！");
      }
    }
  }
  return gpsValid;
}

// 写入数据到 SD 卡
bool writeDataToSD(unsigned long timestamp, float distance, int gsr, float latitude, float longitude, bool gpsValid) {
  File dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print(timestamp);
    dataFile.print(",");
    dataFile.print(distance);
    dataFile.print(",");
    dataFile.print(gsr);
    dataFile.print(",");
    if (gpsValid) {
      dataFile.print(latitude, 6);
      dataFile.print(",");
      dataFile.print(longitude, 6);
    } else {
      dataFile.print("Invalid,Invalid");
    }
    dataFile.println();
    dataFile.close();
    return true;
  }
  return false;
}
