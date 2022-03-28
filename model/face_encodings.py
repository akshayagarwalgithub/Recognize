import cv2
import face_recognition

from utils.log_instantiator import LogInstantiator

log_initiator=LogInstantiator()
logger=log_initiator.get_logger(__name__)

def find_encodings(images, to_process_images_list):
    encode_list = []
    try:
        for img, person_image in zip(images, to_process_images_list):

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            logger.info("Training model on {} of {}".format(person_image[1],person_image[0]))

            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)

    except Exception:
        logger.error("\nImage {} of {} is not fit for training. Please choose a different image.".format(person_image[1],person_image[0]))
        exit(1)
    return encode_list

