from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Load YOLO model
model = YOLO("yolov8n.pt")

# Khởi tạo webcam
cap = cv2.VideoCapture(0)
# replace with cv2.VideoCapture('http://<ip_cam>/cam-hi.jpg')
def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Nhận diện vật thể
        results = model(frame)
        annotated_frame = results[0].plot()

        # Mã hóa khung hình sang JPEG để gửi qua HTTP stream
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Trả về chuỗi byte cho trình duyệt (MJPEG)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)