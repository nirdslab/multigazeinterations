from flask import render_template, request, redirect, jsonify
from detection.heuristic_gaze import HeuristicGazeClassifier
from app import app
import numpy as np
import cv2
import json


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/image-upload', methods=["GET", "POST"])
def image_upload():

    if request.method == "POST":
        g = HeuristicGazeClassifier()

        if request.files:
            image = request.files["image"]
            filestr = request.files["image"].read()
            # convert string data to numpy array
            npimg = np.fromstring(filestr, np.uint8)
            # convert numpy array to image
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            faces = g.detect_gazes(img)

            for face_info in faces:
                (x, y, w, h) = face_info["face"]
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

                label = "H: " + str(face_info["gaze"]["horizontal"]) \
                        + " V: " + str(face_info["gaze"]["vertical"])
                cv2.putText(img, label, (x, y), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                            color=(255, 255, 255))

            img = img.tolist()
            return render_template("image-upload.html", image=json.dumps(img))

    return render_template("image-upload.html", image=None)


@app.route('/webcam-streaming')
def webcam_streaming():
    return render_template("webcam-streaming.html")

@app.route('/frame-process', methods=["POST"])
def frame_process():
    g = HeuristicGazeClassifier()
    if request.files:

        filestr = request.files["image"].read()
        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        faces = g.detect_gazes(img)

        for face_info in faces:
            (x, y, w, h) = face_info["face"]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

            label = "H: " + str(face_info["gaze"]["horizontal"]) \
                    + " V: " + str(face_info["gaze"]["vertical"])
            cv2.putText(img, label, (x, y), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                        color=(255, 255, 255))

        img = img.tolist()
        return json.dumps(img)
    return jsonify([])

