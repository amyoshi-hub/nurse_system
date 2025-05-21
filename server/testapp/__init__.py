from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # 0は内蔵カメラ、USBなら1や2の可能性あり

# HTMLテンプレートを直接書いて簡易表示
HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Webカメラ映像</title>
</head>
<body>
    <h1>介護サポート - カメラ映像</h1>
    <img src="{{ url_for('video_feed') }}">
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # JPEGにエンコード
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # multipartで返す（HTML側で連続画像に見せる）
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

