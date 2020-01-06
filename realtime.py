import cv2
from heuristic_faces import HeuristicFaceClassifier
import pickle
import pandas as pd

cap = cv2.VideoCapture(0)
clf = HeuristicFaceClassifier()

horizontal_model = pickle.load(open("horizontal_gaze.pkcls", "rb"))
vertical_model = pickle.load(open("vertical_gaze.pkcls", "rb"))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = clf.detect_faces(frame)
    # Display the resulting frame
    for face in faces:
        (x, y, w, h) = face["face"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        for eye in face["eyes"]:
            (ex, ey, ew, eh) = eye["eye"]
            ex, ey = x + ex, y + ey
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)

        face_size = face['face'][2]
        dataframe = pd.DataFrame({
            'r_eye_px': face['eyes'][1]['pupil'][0] / face_size,
            'l_eye_px': face['eyes'][0]['pupil'][0] / face_size,
            'r_eye_s': face['eyes'][1]['eye'][2] / face_size,
            'l_eye_s': face['eyes'][0]['eye'][2] / face_size,
            'r_eye_x': face['eyes'][1]['eye'][0] / face_size,
            'l_eye_x': face['eyes'][0]['eye'][0] / face_size,
            'r_eye_y': face['eyes'][1]['eye'][1]/face_size,
            'l_eye_y': face['eyes'][0]['eye'][1]/face_size,
            'r_eye_py': face['eyes'][1]['pupil'][1]/face_size,
            'l_eye_py': face['eyes'][0]['pupil'][1]/face_size}, index=[0])

        horizontal_prediction = round(horizontal_model.predict(dataframe)[0], 1)
        vertical_prediction = round(vertical_model.predict(dataframe)[0], 1)
        label = "H: " + str(horizontal_prediction) \
                + " V: " + str(vertical_prediction)
        cv2.putText(frame, label, (x, y), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                    color=(255, 255, 255))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

a = input("Test")