#### Import ####
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import os
import numpy as np
from headers import *
################

def createOutFolder():
    try:
        if not os.path.exists(WORKING_DIRECTORY_NAME): 
            os.makedirs(WORKING_DIRECTORY_NAME)
    except OSError: 
        print ('Error: Creating directory ' + WORKING_DIRECTORY_NAME) 
    try:
        if not os.path.exists(FULL_PATH_OUT_EXTRACT_IMAGES): 
            os.makedirs(FULL_PATH_OUT_EXTRACT_IMAGES)
    except OSError: 
        print ('Error: Creating directory ' + OUT_EXTRACT_IMAGES) 

def extarctImageFromVid(nameOfTheVideoFile):
    cap= cv2.VideoCapture(nameOfTheVideoFile + '.mp4')
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(FULL_PATH_OUT_EXTRACT_IMAGES + '/' + nameOfTheVideoFile + '_' + str(i) + '.jpg', frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

def helloWorld():
    print(pytesseract.image_to_string(Image.open('test.png')))


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