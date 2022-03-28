import cv2
import os
import pickle
import colorama
import json

from utils.get_project_root import get_project_root
from utils.log_instantiator import LogInstantiator
from utils.parse_arguments import parse_training_arguments
from collections import defaultdict
from utils.input_validator import validate_all_dir_presence_in_input_images_dir,validate_all_files_presence_in_names_dir, validate_images_jpg_png_type
from utils.load_configuration import get_configuration
from model.face_encodings import find_encodings

def main():
    args=parse_training_arguments()
    root_dir=get_project_root()

    log_initiator = LogInstantiator()
    logger = log_initiator.get_logger(__name__)

    conf_variables=get_configuration()

    to_process_images_path = root_dir / conf_variables['input_images_dir']['path']

    dir_presence_in_input_images_dir=validate_all_dir_presence_in_input_images_dir(to_process_images_path)

    if not dir_presence_in_input_images_dir[0]:
        logger.error("\nOnly directories are allowed inside {}, but found '{}', which is not a directory. \nPlease address this and retrain.".format(to_process_images_path,dir_presence_in_input_images_dir[1]))
        exit(1)

    all_files_presence_in_names_dir=validate_all_files_presence_in_names_dir(to_process_images_path)

    if not all_files_presence_in_names_dir[0]:
        logger.error("\nOnly files are allowed inside {}, but found '{}' which is not a file.\nPlease address this and retrain.".format(all_files_presence_in_names_dir[1],all_files_presence_in_names_dir[2]))
        exit(1)

    images_jpg_png_type=validate_images_jpg_png_type(to_process_images_path)

    if not images_jpg_png_type[0]:
        logger.error("\nOnly jpg or png images are allowed inside {}, but found '{}'.\nPlease address this and retrain.\nIf you are using HEIC files, you can leverage heic_to_jpg_converter.py to convert them to jpg.".format(images_jpg_png_type[1],images_jpg_png_type[2]))
        exit(1)

    training_dir_path = root_dir / conf_variables['training_dir']['path']

    training_dir_path.mkdir(exist_ok=True)

    if args.reset_training==True:
        logger.debug('\nForget past training is True. Deleting all training files')
        for file in os.listdir(training_dir_path):
            os.remove(os.path.join(training_dir_path, file))

        logger.debug('Successfully deleted the files inside {}'.format(training_dir_path))

    images = []

    class_names = []

    input_images_dict = {}

    for name_dir in os.listdir(to_process_images_path):

        name_dir_path=os.path.join(to_process_images_path, name_dir)

        if not os.path.isdir(name_dir_path):
            logger.error("{} is a file inside {} directory.\nPlease ensure images are only in their respective name directory".format(name_dir,conf_variables['input_images_dir']['path']))
            exit(1)
        else:
            input_images_dict[name_dir]=os.listdir(name_dir_path)


    to_process_images_list=[]

    images_metadata_json_file_path = root_dir / conf_variables['training_dir']['path'] / \
                                     conf_variables['images_metadata_file']['path']

    images_metadata_json_file_path.touch(exist_ok=True)

    class_names_file = root_dir / conf_variables['training_dir']['path'] / \
                       conf_variables['class_names_file']['path']


    class_names_file.touch(exist_ok=True)

    encode_list_known_file= root_dir / conf_variables['training_dir']['path'] / \
                            conf_variables['encode_list_known_file']['path']
    encode_list_known_file.touch(exist_ok=True)

    images_metadata_json_dict = {}
    incremental_images_dict={}
    encode_list_known=[]

    try:
        with open(images_metadata_json_file_path, "r") as images_metadata_json_file:
            images_metadata_json_dict=json.load(images_metadata_json_file)
    except ValueError:
        pass


    for name, images_list in input_images_dict.items():
        if images_list:
            for name_image in images_list:
                file_path = os.path.join(to_process_images_path, name, name_image)

                if not os.path.isfile(file_path):
                    logger.error("Only files allowed inside directory {}".format(name))
                    exit(1)
                else:
                    if name in images_metadata_json_dict:
                        if name_image not in images_metadata_json_dict[name]:
                            #logger.debug("inside condition to check if image is already in trained json file\n")
                            if name in incremental_images_dict:
                                incremental_images_dict[name][name_image]={'file_name':os.path.splitext(name_image)[0], 'file_type':os.path.splitext(name_image)[1]}
                            else:
                                incremental_images_dict[name]={name_image:{'file_name': os.path.splitext(name_image)[0],'file_type': os.path.splitext(name_image)[1]}}
                            # print("incremental_images_dict = {} \n".format(incremental_images_dict))
                            cur_img = cv2.imread(f'{to_process_images_path}/{name}/{name_image}')
                            images.append(cur_img)
                            to_process_images_list.append((name,name_image))
                        else:
                            logger.info("{} of {} was already used for training before. Skipping reprocessing.".format(name_image,name))
                    else:
                        if name in incremental_images_dict:
                            incremental_images_dict[name][name_image]={'file_name': os.path.splitext(name_image)[0],'file_type': os.path.splitext(name_image)[1]}
                        else:
                            incremental_images_dict[name]={name_image:{'file_name': os.path.splitext(name_image)[0],'file_type': os.path.splitext(name_image)[1]}}

                        cur_img = cv2.imread(f'{to_process_images_path}/{name}/{name_image}')

                        images.append(cur_img)

                        to_process_images_list.append((name, name_image))

    if to_process_images_list:

        open_encd_lst_knwn_file = open(encode_list_known_file, "rb")
        try:
            encode_list_known = pickle.load(open_encd_lst_knwn_file)
        except EOFError:
            pass

        open_encd_lst_knwn_file.close()

        logger.info("\n################################################")
        logger.info("##                  TRAINING                  ##")
        logger.info("################################################")
        logger.info("Starting to train model on new images")

        encode_list_known.extend(find_encodings(images, to_process_images_list))

        logger.debug('Encoding calculation on input images complete')

        logger.debug('Writing encoding list to file')

        open_encode_list_known_file=open(encode_list_known_file, "wb")
        pickle.dump(encode_list_known, open_encode_list_known_file)
        open_encode_list_known_file.close()

        logger.debug('Completed writing encodings list to file')

        open_classnames_file = open(class_names_file, "rb")
        try:
            class_names = pickle.load(open_classnames_file)
        except EOFError:
            pass

        open_classnames_file.close()

        for to_prcs_img in to_process_images_list:

            class_names.append(to_prcs_img[0])

        logger.debug("Writing class names list to file")

        open_class_names_file = open(class_names_file, "wb")
        pickle.dump(class_names, open_class_names_file)
        open_class_names_file.close()

        logger.debug('Completed Writing class names list to file')

        logger.info("\n################################################")
        logger.info("##              MEMORIZATION                  ##")
        logger.info("################################################")
        logger.info("Model memorizing trained images for future use.")

        for name, images_details_dict in incremental_images_dict.items():
            for image, image_metadata_dict in incremental_images_dict[name].items():
                if name in images_metadata_json_dict:
                    images_metadata_json_dict[name][image] = image_metadata_dict
                else:
                    images_metadata_json_dict[name] = {image: image_metadata_dict}
        logger.info("Model's memorization complete.")


        logger.debug("Starting to write to images metadata json")
        with open(images_metadata_json_file_path, "w") as images_metadata_json_file:
            json.dump(images_metadata_json_dict, images_metadata_json_file, indent=2)

        logger.debug("Write to images metadata json is complete")

        logger.info(colorama.Fore.BLACK + colorama.Style.BRIGHT + colorama.Back.GREEN + "\n                 SUCCESS                 " + colorama.Fore.RESET)
        logger.info("Training on images completed successfully.")
    else:
        logger.warning("\nNo new images(different from previously trained images) available to train on.")

if __name__=="__main__":
    main()