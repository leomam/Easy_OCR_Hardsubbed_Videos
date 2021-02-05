#### Import ####
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import os
import numpy as np
import subprocess
from headers import *

################

##### Split Video Name and Extension #####
def verifIfExtensionExist(file):
    i = 0
    found = False
    ext = None
    ext = file.rsplit('.', 1)[1]
    if ext != None:
        while (i < (len(VIDEO_EXTENSION_ARRAY)) and not found):
            if (VIDEO_EXTENSION_ARRAY[i] == ext):
                found = True
            i+=1
    return found

def splitExtensionFile(file):
    if verifIfExtensionExist(file):
        return file.rsplit('.', 1)
    else:
        return None
##########################################

##### Extract Frames From Video #####
def extractFrameFromVid(video):
    if os.path.exists(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES):
        cap = cv2.VideoCapture(video.getPath())
        i=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            cv2.imwrite(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES + '/' + str(i) + '.jpg', frame)
            video.addFrame(str(i) + '.jpg')
            i+=1
        cap.release()
        cv2.destroyAllWindows()
    else :
        print('Error: You should create folders before extract something in it !')
#####################################

##### Creat Folders #####
def createFoldersForVideo(video):
    try:
        if not os.path.exists(WORKING_DIRECTORY_NAME): 
            os.makedirs(WORKING_DIRECTORY_NAME)
    except OSError: 
        print ('Error: Creating directory ' + WORKING_DIRECTORY_NAME) 
    try:
        if not os.path.exists(video.getWorkDir()): 
            os.makedirs(video.getWorkDir())
        else :
            print('Warning : the folder \"' + video.getWorkDir() + '\" already exist, you shouldn\'t extract frames in there !')
    except OSError: 
        print ('Error: Creating directory ' + video.getWorkDir())
    try:
        if not os.path.exists(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES): 
            os.makedirs(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES)
        else :
            print('Warning : the folder \"' + video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES + '\" already exist, you shouldn\'t extract frames in there !')
    except OSError: 
        print ('Error: Creating directory ' + video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES) 
#########################



def extractText():
    allImages = os.listdir(FULL_PATH_OUT_EXTRACT_IMAGES)
    allImages.sort()
    #print(allImages)

    for i in range (len(allImages)):
        val = FULL_PATH_OUT_EXTRACT_IMAGES + '/' + allImages[i]
        print(pytesseract.image_to_string(Image.open(val)))


def cropImage(x, y, h, w, nameImage, saveFolder):
    image = cv2.imread('test.png')
    crop = image[y:y+h, x:x+w]
    cv2.imwrite(saveFolder + '/' + nameImage + '.jpg', crop)


def getDurationVideo(pathOfTheVideoFile):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", pathOfTheVideoFile],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def getNumberOfFrames(pathOfTheVideoFile):
    cap = cv2.VideoCapture(pathOfTheVideoFile)
    totalframecount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return totalframecount

def getVidDimensions(pathOfTheVideoFile):
    vid = cv2.VideoCapture(pathOfTheVideoFile)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    return str(width) + 'x' + str(height)