from flask import Flask, render_template, Response, url_for
from ultralytics import YOLO
import cv2
import numpy as np
import requests

app = Flask(__name__)

# YOLO model
model = YOLO("yolov8n.pt")

# Ảnh snapshot từ ESP32-CAM
url = "http://10.158.229.118/cam-hi.jpg"


def gen_frames():
    while True:
        try:
            # load ảnh từ URL
            response = requests.get(url, timeout=1)
            img_bytes = response.content

            # decode sang ảnh opencv
            img_array = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is None:
                continue

            # YOLO detect
            results = model(frame)
            annotated = results[0].plot()

            # encode lại JPG để stream
            ret, buffer = cv2.imencode('.jpg', annotated)
            frame = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )

        except Exception as e:
            print("❌ Error:", e)
            continue


@app.route("/")
def index():
    video_url = url_for('video_feed', _external=True)
    return render_template("index.html", video_url=video_url)


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
