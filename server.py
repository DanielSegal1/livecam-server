import sys
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


def gen_frames():
    global camera
    
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/stream')
def stream():
    # video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    global camera

    auto_detected_camera_param = 0 if sys.platform == 'win32' else '/dev/video0' 
    camera = cv2.VideoCapture(sys.argv[1] if len(sys.argv) >= 2 else auto_detected_camera_param)
    app.run(debug=True)