from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import numpy as np
import requests

app = Flask(__name__)

# Load YOLO model
model = YOLO("yolov8n.pt")
url = "http://192.168.1.9/cam-hi.jpg"

def gen_frames():
    while True:
        try:
            # Tải ảnh từ URL mỗi vòng → luôn mới
            img_bytes = requests.get(url, timeout=1).content

            # Chuyển bytes thành ảnh OpenCV
            img_array = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is None:
                continue

            # YOLO detect
            results = model(frame)
            annotated_frame = results[0].plot()

            # Encode JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("❌ Error:", e)
            continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
