import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

from flask import Flask, render_template, Response
import cv2

serverIp = "0.0.0.0"

app = Flask(__name__)

def find_camera(id):
    cameras = ['rtsp://admin:fragata@23@192.168.1.231:554/onvif1','rtsp://admin:livia2013@192.168.1.23:554/onvif1']
    return cameras[int(id)]
 
def gen_frames(camera_id):
    cam = find_camera(camera_id)
    cap=  cv2.VideoCapture(cam)
    
    while True:
        success, frame = cap.read()  
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
