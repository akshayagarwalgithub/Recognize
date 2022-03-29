

  
<p align="center"><img src="https://user-images.githubusercontent.com/34087302/159622141-50bf479b-63ea-4716-9874-7cae6b7f47e0.PNG" width="500" height="125"></p>


Recognize is a facial recognition tool. It facilitates facial recognition using 3 simple steps. 



To recognize a person named John Doe, it requires the following 3 steps:

- Create a directory named John. Load John's images inside John directory.
- Execute one training script, to let Recognize get familiar with John's face.
- Execute one recognition script and John would be recognized, when he is in front of the camera.

The following few seconds video shows the final result of Recognize:   



https://user-images.githubusercontent.com/34087302/159835350-c863b249-78a9-4cb8-9354-22941e5a5c93.mp4




---
## 💡 Features offered

- Easy training - Train Recognize for any person, by creating a directory named after that person, then loading his/her images into that directory and just executing one training script. 
- Memorization of all past training.
- Intelligence to judge new images of a person, without unnecessary retraining on images already used in past.
- Provision to erase all past memorized training and start from scratch.
- Support for jpg and png format images.
- Inbuilt converter to convert any heic format images to jpg format.
 
Available below are all the detailed steps to use this project.
   
<br />
 
  
 <p align="center"><img src="https://user-images.githubusercontent.com/34087302/160212840-4af160bc-0491-4bcc-9d13-06177cd2817a.jpg" width="800" height="400"></p>  
   
<br />   
   
## :wrench: Dependencies and Installation

### Requirement  
- Python >= 3.7 (**Required**)


### Installation

1. Clone repo

    ```bash
    git clone https://github.com/akshayagarwalgithub/Recognize.git
    cd Recognize
    ```

1. **Install required packages** (depending on your local setup, feel free to use pip or pip3 whichever is suitable for your setup. Make sure you are using Python >=3.7)

    ```bash
    # Install cmake
    pip install cmake

    # Recognize uses face-recognition and internally dlib's deep learning state-of-the-art face recognition.
    pip install dlib

    pip install face-recognition
    
    pip install numpy
    
    # Install opencv-python - Pre-built OpenCV packages for Python
    pip install opencv-python
    
    pip install colorama
    ```
<br />

## :computer: Training (Steps 1 & 2)
    
Recognize support **jpg or png** images for training.

**Training steps**:

1. Create a directory named :file_folder:input_images in the root path of Recognize, as follows:
```
cd Recognize
mkdir input_images
```
2. Inside :file_folder: input_images, create a folder named after the person whose images will be used for training.
Example - If we are training for John, then the folder should be named John. If we are planning to simultaneously train for Nina and Sam also, then create 2 separate folders, one named Nina and the other named Sam. Basically create a separate folder for every unique individual, you would like to recognize.

3. Put all the jpg or png format images of the persons inside the folder named after that person. In the above example, all John's images should go inside :file_folder:John. Similarly Nina and Sam's images inside :file_folder:Nina and :file_folder:Sam. Note - Different image files of the same person should have different names.

An example of such name directory hierarchy is shown below:

<img src="https://user-images.githubusercontent.com/34087302/159601962-e6f59ccf-ecf5-4ef5-bce6-e3b5b65c9e28.PNG" width="500" height="300">

4. Once the images are loaded in the name folders, execute the following command (feel free to use _python_ or _python3_ based on your Python 3 setup):
    ```
    cd Recognize
    python training_on_images.py
    ```
<br />

## :camera: :video_camera: Recognize the face (Step 3)
Once the training is successfully complete, execute the following command and this would activate the webcam.
```
python recognition.py
```
As this would activate the webcam, you might need to authorize access to webcam, so please do so and then execute.  
Bring the person(whose images were used for training) in front of the webcam, to get recognized :sparkles:

To close the active webcam window appearing on your screen, click anywhere on Webcam window and then press **'x'** key on your keyboard at any time.

<br />  

## :loudspeaker: Key points to remember

1. Recognize should be trained for the person you finally want to be recognized.
2. The training images should be solo image of each person. Group photos should not be used.
3. It is best to use good quality photos, with visible face.
4. The better(more number of images) the training, the stronger would be the prediction.
5. The name which you choose for a person's name directory, the same name would be displayed during recognition. If the name is too long, please choose a shorter version.

<br />


## 🤖 Additional available features (to be used on as-needed basis):   
     
     
### :broom: Erasing past training:
**Recognize remembers all the training it receives.** It keeps a memory of the directory name of every person and the image file names used for each person.   
When training on new images, if it finds the same image file name for the same person, which it has already been trained on in past, it will efficiently skip retraining.    
If at any point you would like Recognize to erase and forget all past training, use --reset_training True as follows:
```
python training_on_images.py --reset_training True 
```
  
   
   
### :iphone: Converting heic format files to jpg format: 

**Note** - _Skip this part entirely, if you don't have any image in **.heic format**._   

If you are a heavy iphone user and realize that some of your training images are in heic format, you must first convert them to jpg or png. This is because Recognize only accept jpg or png file formats.   
You can choose to convert heic files yourself or use Recognize's built in converter. **To use Recognize's built in converter you need to first have imagemagick installed for your Operating System.**

[imagemagick installation](https://imagemagick.org/script/download.php)
    
Once imagemagick is installed successfully, load all the heic image files in respective name directories and execute:
```
python heic_to_jpg_converter.py
```
heic_to_jpg_converter scans all the name directories inside input_images directory and automatically converts every heic file to jpg. **It would do all the hard work of searching as well as converting.**

![images](https://user-images.githubusercontent.com/34087302/160299230-8b269436-8754-4b62-b8b7-552b87054b14.png)  

Thank you for your interest in Recognize. Ease of use has been the main goal behind creating this project. 
### If you like Recognize, please feel free to recommend it to your friends. Also if you would like to, you can :star: this repo. It helps. Thanks.
<br />


Many thanks to Davis King for creating dlib and for providing the trained facial feature detection and face encoding models and Adam Geitgey for creating face-recognition, used in this project.
Thanks to the creators of opencv.
Thanks to all who works on creating remarkable Python data science libraries like numpy etc.

