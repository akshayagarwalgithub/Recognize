#This would convert HEIC format images to jpg format.
#Prerequisite - To execute this successfully, you need to first install ImageMagick from https://imagemagick.org/script/download.php

#Benefit - heic_to_jpg_converter.py scans all the images inside subdirectories of input_images directory and convert them to jpg format.

from utils.get_project_root import get_project_root
from utils.input_validator import validate_images_jpg_png_type,validate_all_files_presence_in_names_dir,validate_all_dir_presence_in_input_images_dir
from utils.log_instantiator import LogInstantiator
import os, subprocess
from utils.load_configuration import get_configuration

log_initiator=LogInstantiator()
logger=log_initiator.get_logger(__name__)

root_dir=get_project_root()

conf_variables=get_configuration()

to_process_images_path = root_dir/conf_variables['input_images_dir']['path']

dir_presence_in_input_images_dir=validate_all_dir_presence_in_input_images_dir(to_process_images_path)

if not dir_presence_in_input_images_dir[0]:
    logger.error("\nOnly directories are allowed inside {} but found '{}' which is not a directory. Please address this before starting conversion.".format(to_process_images_path,dir_presence_in_input_images_dir[1]))
    exit(1)

all_files_presence_in_names_dir=validate_all_files_presence_in_names_dir(to_process_images_path)

if not all_files_presence_in_names_dir[0]:
    logger.error("\nOnly files are allowed inside {}, but found '{}' which is not a file. Please address this before starting conversion.".format(all_files_presence_in_names_dir[1],all_files_presence_in_names_dir[2]))
    exit(1)

heic_images_cnt=0
name_dirs=[]
for name_dir in os.listdir(to_process_images_path):
    name_dirs.append(name_dir)
    name_dir_path=os.path.join(to_process_images_path, name_dir)

    for image in os.listdir(name_dir_path):
        if image.lower().endswith(".heic"):
            heic_images_cnt+=1
            os.chdir(name_dir_path)
            image_file_path = os.path.join(name_dir_path, image)

            logger.info('\nConverting {} to jpg format'.format(image_file_path))
            subprocess.run(["magick", "%s" % image, "%s" % (image[0:-5] + '.jpg')],check=True)
            logger.debug('Deleting converted file {}'.format(image_file_path))
            os.remove(image_file_path)

if heic_images_cnt==0:
    logger.warning("\nNo heic format images found inside input name directories.")
else:
    logger.info("\nSuccessfully converted heic files to jpg.")
