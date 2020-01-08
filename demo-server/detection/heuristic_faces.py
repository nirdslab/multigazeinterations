import cv2
import numpy as np


class HeuristicFaceClassifier:
    face_cascade = None

    eye_cascade = None

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def detect_faces(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_image)

        valid_faces = []
        for face in faces:
            (x, y, w, h) = face
            crop = gray_image[y:y + h, x: x + w]
            heuristic_result = self._heuristic_test(crop)
            heuristic_result['eyes'].sort(key=lambda x: x['eye'][0])

            if heuristic_result['result']:
                valid_faces.append({'face': face, 'eyes': heuristic_result['eyes']})
        return valid_faces

    def _heuristic_test(self, face_image):
        (w, h) = face_image.shape
        eyes = self.eye_cascade.detectMultiScale(face_image)
        return_data = {'result': True, 'eyes': []}

        if len(eyes) == 2:
            for eye in eyes:
                (x, y, w, h) = eye
                pupil = self._heuristic_pupil(face_image[y:y + h, x: x + w])
                return_data['eyes'].append({'eye': eye, 'pupil': pupil})
            # (e1x, e1y, e1w, e1h) = eyes[0]
            # (e2x, e2y, e2w, e2h) = eyes[1]
            #
            # # eye should be same side of 1/5 line
            # (x1, y1) = (int(w / 5.0), 0)
            # (x2, y2) = (int(w / 5.0), h)
            # d1 = ((e1x - x1) * (y2 - y1)) - ((e1y - y1) * (x2 - x1))
            # d2 = ((e2x - x1) * (y2 - y1)) - ((e2y - y1) * (x2 - x1))
            #
            # if (d1 > 0) ^ (d2 > 0):
            #     return False
            #
            # # eye should be same side of 4/5 line
            # (x1, y1) = (int(w * 4 / 5.0), 0)
            # (x2, y2) = (int(w * 4 / 5.0), h)
            # d1 = ((e1x - x1) * (y2 - y1)) - ((e1y - y1) * (x2 - x1))
            # d2 = ((e2x - x1) * (y2 - y1)) - ((e2y - y1) * (x2 - x1))
            # if (d1 > 0) ^ (d2 > 0):
            #     return False
            #
            # # check eyes either side of mid line
            # (x1, y1) = (int(w / 2.0), 0)
            # (x2, y2) = (int(w / 2.0), h)
            # d1 = ((e1x - x1) * (y2 - y1)) - ((e1y - y1) * (x2 - x1))
            # d2 = ((e2x - x1) * (y2 - y1)) - ((e2y - y1) * (x2 - x1))
            # if not ((d1 > 0) ^ (d2 > 0)):
            #     return False
            # return True
        elif len(eyes) == 1:
            # Try to detect the other eye in the face image
            return_data['result'] = False
        else:
            return_data['result'] = False
        return return_data

    def _heuristic_pupil(self, eye_image):
        # gray = eye_image
        eye_image = ~ eye_image
        eye_image = cv2.GaussianBlur(eye_image, (7, 7), 0)

        # Gaussian Kernel Amplification ?
        (w, h) = eye_image.shape
        g = cv2.getGaussianKernel(w, 1)
        eye_image = ((eye_image * g).T * g).T

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(eye_image)
        # cv2.circle(gray, minLoc, 7, (255, 0, 0), 2)
        # cv2.imshow("Eye", gray)
        # cv2.waitKey()
        return np.array(list(maxLoc) + [7])
