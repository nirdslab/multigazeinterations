from detection.heuristic_faces import HeuristicFaceClassifier
import pickle
import pandas as pd


class HeuristicGazeClassifier():
    clf = None

    horizontal_model = None

    vertical_model = None

    def __init__(self):
        self.clf = HeuristicFaceClassifier()
        self.horizontal_model = pickle.load(open("horizontal_gaze.pkcls", "rb"))
        self.vertical_model = pickle.load(open("vertical_gaze.pkcls", "rb"))

    def detect_gazes(self, image):
        faces = self.clf.detect_faces(image)

        for face in faces:
            face_size = face['face'][2]

            dataframe = pd.DataFrame({
                'r_eye_px': face['eyes'][1]['pupil'][0] / face_size,
                'l_eye_px': face['eyes'][0]['pupil'][0] / face_size,
                'r_eye_s': face['eyes'][1]['eye'][2] / face_size,
                'l_eye_s': face['eyes'][0]['eye'][2] / face_size,
                'r_eye_x': face['eyes'][1]['eye'][0] / face_size,
                'l_eye_x': face['eyes'][0]['eye'][0] / face_size,
                'r_eye_y': face['eyes'][1]['eye'][1] / face_size,
                'l_eye_y': face['eyes'][0]['eye'][1] / face_size,
                'r_eye_py': face['eyes'][1]['pupil'][1] / face_size,
                'l_eye_py': face['eyes'][0]['pupil'][1] / face_size}, index=[0])

            horizontal_prediction = round(self.horizontal_model.predict(dataframe)[0], 1)
            vertical_prediction = round(self.vertical_model.predict(dataframe)[0], 1)
            face["gaze"] = dict()
            face["gaze"]["vertical"] = vertical_prediction
            face["gaze"]["horizontal"] = horizontal_prediction

        return faces
