# 🤖 Hệ thống ESP32-CAM + YOLO Detection + Flask Web

Tài liệu này hướng dẫn cách thiết lập **ESP32-CAM**, cài đặt môi trường **YOLO** trên Python, và chạy server **Flask** để hiển thị kết quả nhận diện đối tượng trực tiếp từ camera.

---
# Cấu trúc dự án
.
├── .vscode/
│   └── ... (các cấu hình cho VS Code – launch.json, settings.json)
│
├── ESP32_server/
│   ├── ESP32_server.ino
│   └── ... (mã nguồn chạy trên Arduino, tạo WebServer xuất ảnh JPG)
│
├── templates/
│   └── index.html        # Template HTML cho Flask hiển thị video MJPEG stream
│
├── README.md             # Hướng dẫn sử dụng (file Markdown)
│
├── default_labels_detection.note
│                         # Ghi chú về các nhãn YOLO COCO 80 classes mặc định, xem cho biết
│
├── environment.yml       # File cấu hình Conda cho môi trường YOLO + Flask bằng conda
│
├── esp32cam-main.zip     # Thư viện ESP32-CAM cần thêm vào thêm vào Arduino IDE
│
├── main.py               # Code Flask + YOLO detect từ ESP32-CAM
│
├── requirements.txt      # Danh sách Python packages (pip)
│
└── yolov8n.pt            # Pretrained YOLOv8 model (COCO 80 classes)

---

## I. 📷 Chạy ESP32-CAM Camera Server

### 1. Nạp chương trình cho ESP32-CAM

* Mở **Arduino IDE**. Mở file chương trình **ESP32_server/ESP32_server.ino**.
* Vào **Sketch → Include Library → Add .ZIP Library…**
    * Chọn file **esp32cam-main.zip** để cài đặt thư viện cần thiết.
* **Mở lại file chương trình:** Kiểm tra và cập nhật các thông số **WiFi SSID** và **Mật khẩu** của bạn.

### 2. Cấu hình Board và Nạp Code

* Vào **Tools → Board → ESP32 Arduino**
    * Chọn **ESP32 Wrover Module**.
* Nhấn **Upload** để nạp code vào ESP32-CAM.

### 3. Lấy địa chỉ IP camera

* Mở **Serial Monitor** (Baud rate: **115200**).
* Sau khi kết nối WiFi thành công, ESP32-CAM sẽ in ra địa chỉ IP của nó.
* **Ví dụ:** `http://192.168.1.9/cam-hi.jpg`
    > **Ghi chú:** Đây chính là **URL đầu vào** cho bước cấu hình YOLO.

---

## II. 🐍 Cài môi trường YOLO trên Python

### 1. Tạo môi trường Python bằng Conda

Bạn nên tạo một môi trường ảo để quản lý thư viện tốt hơn.

#### **Cách 1: Từ file `environment.yml` (Khuyến khích)**
```sh
conda env create -f environment.yml
conda activate yolovenv
```
#### **Cách 2: Từ file `requirements.txt` (Khuyến khích)**
```
conda create -n yolovenv python==3.9
conda activate yolovenv
python -m pip install -r requirements.txt
```

### 2. Cập nhật lại đường dẫn url trong main.py
- url = "http://<your ip>/cam-hi.jpg"
- Và sau đó trong terminal chạy python `main.py`

### 3. Mở đường dẫn và xem http://localhost:5000