from flask import Flask, render_template, request, send_from_directory
import cv2
import mediapipe as mp
import os
import numpy as np

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "outputs"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

def analyze_face(image_path):
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape

    with mp_face.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        result = face_mesh.process(rgb)
        if not result.multi_face_landmarks:
            return None, "No face detected."

        for face_landmarks in result.multi_face_landmarks:
            mp_draw.draw_landmarks(img, face_landmarks, mp_face.FACEMESH_TESSELATION)

            # Simple demo: measure face width between two landmarks (left & right cheek)
            x1 = int(face_landmarks.landmark[234].x * w)
            x2 = int(face_landmarks.landmark[454].x * w)
            face_width = abs(x2 - x1)

        profile = "Extrovert" if face_width > 200 else "Introvert"
        return img, f"Face Width: {face_width}px → Personality: {profile}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            processed_img, result = analyze_face(path)
            if processed_img is None:
                return render_template("index.html", result=result)

            out_path = os.path.join(app.config["OUTPUT_FOLDER"], "output.jpg")
            cv2.imwrite(out_path, processed_img)
            return render_template("index.html", result=result, image="output.jpg")
    return render_template("index.html")

@app.route("/outputs/<filename>")
def outputs(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
