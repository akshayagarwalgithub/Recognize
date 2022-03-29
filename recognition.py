import cv2
import face_recognition
import numpy as np
import pickle
from pathlib import Path
from utils.get_project_root import get_project_root
from utils.log_instantiator import LogInstantiator
from utils.load_configuration import get_configuration

log_initiator=LogInstantiator()
logger=log_initiator.get_logger(__name__)

logger.info("Starting to Capture Video from camera.")
logger.info("\nTo stop video capture, click anywhere on Webcam window and press 'x' key on your keyboard")

root_dir=get_project_root()

conf_variables=get_configuration()

camera=cv2.VideoCapture(0)
encode_list_known_file_path=root_dir/conf_variables['training_dir']['path']/conf_variables['encode_list_known_file']['path']
encode_list_known_file=Path(encode_list_known_file_path)

while True:
    success, img = camera.read()
    imgS=img
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faces_cur_frame = face_recognition.face_locations(imgS)
    encodings_cur_frame = face_recognition.face_encodings(imgS, faces_cur_frame)

    class_names, encode_list_known = [], []
    class_names_file = Path(root_dir / conf_variables['training_dir']['path'] / \
                                  conf_variables['class_names_file']['path'])

    open_class_names_file = open(class_names_file, "rb")
    class_names = pickle.load(open_class_names_file)
    open_class_names_file.close()

    open_encode_list_known_file = open(encode_list_known_file, "rb")
    encode_list_known = pickle.load(open_encode_list_known_file)
    open_encode_list_known_file.close()

    for encode_face, face_loc in zip(encodings_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_dis = face_recognition.face_distance(encode_list_known, encode_face)

        match_index = np.argmin(face_dis)

        if matches[match_index]:
            name = class_names[match_index]

            y1,x2,y2,x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)

            cv2.putText(img,name.title(),(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,0),1)

    cv2.imshow('Webcam',img)

    if cv2.waitKey(1)== ord('x'):
        break

camera.release()
cv2.destroyAllWindows()