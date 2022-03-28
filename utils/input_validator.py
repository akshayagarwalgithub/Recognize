import os

def validate_all_dir_presence_in_input_images_dir(to_process_images_path):
    for name_dir in os.listdir(to_process_images_path):
        name_dir_path=os.path.join(to_process_images_path, name_dir)
        if not os.path.isdir(name_dir_path):
            return [False,name_dir]
    return [True,"Success"]

def validate_all_files_presence_in_names_dir(to_process_images_path):
    for name_dir in os.listdir(to_process_images_path):
        name_dir_path=os.path.join(to_process_images_path, name_dir)
        for image in os.listdir(name_dir_path):
            image_file_path = os.path.join(name_dir_path, image)
            if not os.path.isfile(image_file_path):
                return [False,name_dir_path,image]
    return [True,"Success","Success"]


# Only jpg and png file types are permitted
def validate_images_jpg_png_type(to_process_images_path):
    for name_dir in os.listdir(to_process_images_path):
        name_dir_path=os.path.join(to_process_images_path, name_dir)
        for image_file_name in os.listdir(name_dir_path):
            if os.path.splitext(image_file_name)[1].lower()!='.jpg' and os.path.splitext(image_file_name)[1].lower()!='.png':
                return [False,name_dir_path,image_file_name]
    return [True,"Success","Success"]

