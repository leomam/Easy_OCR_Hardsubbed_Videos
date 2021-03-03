from headers import WORKING_DIRECTORY_NAME
from functions import splitExtensionFile, extractFrameFromVid, createFoldersForVideo, getNumberOfFrames, getDurationVideo, getVidDimensions, processOCR, framesCleaning

class Video:

    def __init__(self, name):
        self.name = name
        self.nameWithoutExt = splitExtensionFile(self.name)[0]
        self.path = name
        self.ext = splitExtensionFile(self.name)[1]
        self.frames = []
        self.nbFrames = getNumberOfFrames(self.path)
        self.duration = getDurationVideo(self.path)
        self.fps = float(self.nbFrames/self.duration)
        self.dimensions = getVidDimensions(self.path)
        self.workDir = WORKING_DIRECTORY_NAME + '/' + self.nameWithoutExt
    
    def getName(self):
        return self.name

    def getNameWithoutExt(self):
        return self.nameWithoutExt
    
    def getPath(self):
        return self.path
    
    def getExt(self):
        return self.ext
    
    def getDuration(self):
        return self.duration
    
    def getFPS(self):
        return self.fps

    def getNbFrames(self):
        return self.nbFrames
    
    def getFrames(self):
        return self.frames

    def getDimensions(self):
        return self.dimensions

    def getWorkDir(self):
        return self.workDir

    def addFrame(self, frame):
        self.frames.append(frame)
    
    def setFrames(self, frames):
        self.frames = frames
    
    def setDuration(self, duration):
        self.duration = duration
    
    def setFPS(self):
        self.fps = float(self.nbFrames/self.duration)
    
    def setNbFrames(self, nbFrames):
        self.nbFrames = nbFrames

    def createFolders(self):
        createFoldersForVideo(self)
    
    def extractFrames(self):
        extractFrameFromVid(self)
    
    def cleanFrames(self):
        framesCleaning(self)

    def processFrames(self):
        processOCR(self)

    def toString(self):
        return '''
#####################################################
# Video #
#########
# Name : \t\t{name}
# Name Without Ext : \t{nameWithoutExt}
# Ext : \t\t{ext}
# Frames : \t\t{lengthFrames} 
# Extracted Frames : \t{lengthExtractedFrames}
# Dimensions : \t\t{width}x{height}
# Duration : \t\t{duration}
# FPS : \t\t{fps}
# Working Dir : \t{workDir}
#####################################################
'''.format(name=self.name, nameWithoutExt=self.nameWithoutExt, ext=self.ext, lengthFrames=self.nbFrames, lengthExtractedFrames=len(self.frames), width=self.dimensions['width'], height=self.dimensions['height'], duration=self.duration, fps=self.fps, workDir=self.workDir)