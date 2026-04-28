import os
import time
from flask import Flask, render_template, Response, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

FRAME_PATH = os.getenv("FRAME_PATH", "latest_frame.jpg")


@app.route("/")
def index():
    return render_template("index.html")


def generate_frames():
    while True:
        if not os.path.exists(FRAME_PATH):
            time.sleep(0.1)
            continue

        with open(FRAME_PATH, "rb") as frame_file:
            frame = frame_file.read()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

        time.sleep(0.05)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/events")
def events():
    return jsonify({
        "events": []
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
