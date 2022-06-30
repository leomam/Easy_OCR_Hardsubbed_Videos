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

##### Crop Image #####
def cropImage(x, y, h, w, image):
    crop = image[y:y+h, x:x+w]
    return crop
######################

##### Extract Frames From Video #####
def extractFrameFromVid(video):
    if os.path.exists(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES):
        print('Starting Extraction')
        cap = cv2.VideoCapture(video.getPath())
        i=0
        rate=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            if rate > 2000:
                frame = cropImage(int(video.getDimensions()['width']*0.02), int(video.getDimensions()['height']*0.8), int(video.getDimensions()['height']*0.2), int(video.getDimensions()['width']-(video.getDimensions()['width']*0.02)), frame)
                cv2.imwrite(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES + '/' + str(i) + '.png', frame)
                video.addFrame(str(i) + '.png')
                rate=0
            i+=1
            rate+=1
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

##### SRT #####
def srtSave(dialogueTime, it):
    srtTemplate = '''{it}
{startDialogueTime} --> {endDialogueTime}
{dialogue}

'''.format(it=it, startDialogueTime=formatTime(dialogueTime['startDialogueTime']), endDialogueTime=formatTime(dialogueTime['endDialogueTime']), dialogue=dialogueTime['dialogue'])
    if it == 1:
        file = open('read.srt', 'w')
    else:
        file = open('read.srt', 'a')
    file.write(srtTemplate) 
    file.close()

def formatTime(time):
    hours = 0
    minutes = 0
    secondes = 0
    milisecondes = 0
    if time>=3600:
        hours = int(time/3600)
        time = time - (3600*hours)
    if time>=60:
        minutes = int(time/60)
        time = time - (60*minutes)
    if time>=1:
        secondes =  int(time)
        time = time - secondes
    milisecondes = int(time*1000)
    return '{:0>2}:{:0>2}:{:0>2},{:0>3}'.format(hours, minutes, secondes, milisecondes)
###############

##### Metadata Functions #####
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
    return {'width': int(width), 'height': int(height)}

def imagePerTime(fps, imageNum):
    return float(imageNum/fps)
##############################

def checkExtractedFile(video):
    allFrames = os.listdir(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES_CLEAN)
    video.setNbFrames(len(allFrames))
    video.setFrames(allFrames)


def processOCR(video):
    if os.path.exists(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES):
        print('Starting OCR')
        allDialogueTime = []
        previousDialogue = ""
        startDialogueTime = 0
        endDialogueTime = 0
        it = 0
        checkExtractedFile(video)
        for i in range (video.getNbFrames()):
            dialogue = pytesseract.image_to_string(Image.open(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES_CLEAN + '/' + video.getFrames()[i]), lang='fra')
            print(dialogue)
            if dialogue == previousDialogue:
                endDialogueTime = imagePerTime(video.getFPS(), i+1)
            else:
                it += 1
                startDialogueTime = imagePerTime(video.getFPS(), i+1)
                previousDialogue = dialogue
                srtSave({'dialogue': dialogue, 'startDialogueTime': startDialogueTime, 'endDialogueTime':endDialogueTime}, it)
        #allDialogueTime.append({'dialogue': dialogue, 'startDialogueTime': startDialogueTime, 'endDialogueTime':endDialogueTime})
        
        #print(allDialogueTime)
    else :
        print('Error: You should create folders before extract something in it !')


##############################
def frameCleaning(videoWorkingDir, frame, numFrame):
    frame = apply_brightness_contrast(frame, -115, 150)
    frame[np.all(frame >= (0, 0, 255), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (0, 255, 0), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (255, 0, 0), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (254, 0, 254), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (0, 254, 254), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (254, 254, 0), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (254, 255, 255), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (255, 254, 255), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (255, 255, 254), axis=-1)] = (255,255,255)
    #frame[np.all(frame >= (100, 100, 100), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (70, 0, 0), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (0, 0, 70), axis=-1)] = (255,255,255)
    frame[np.all(frame >= (0, 70, 0), axis=-1)] = (255,255,255)
    cv2.imwrite(videoWorkingDir + '/' + OUT_EXTRACT_IMAGES_CLEAN + '/' + str(numFrame), frame)

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

    
#frameCleaning(video.getWorkDir(), Image.open(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES + '/' + video.getFrames()[i]), video.getFrames()[i])

def framesCleaning(video):
    checkExtractedFile(video)
    for i in range (video.getNbFrames()):
        frameCleaning(video.getWorkDir(), cv2.imread(video.getWorkDir() + '/' + OUT_EXTRACT_IMAGES + '/' + video.getFrames()[i]), video.getFrames()[i])