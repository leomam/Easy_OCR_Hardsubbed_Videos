from headers import VIDEO_PATH
from Video import Video

v = Video(VIDEO_PATH)
print(v.toString())
v.createFolders()
v.extractFrames()
v.cleanFrames()
v.processFrames()
print(v.toString())

## TO DO ##
#Verif if path exist                    Check
#Print All info of file                 Check
#Create Folders                         Check
#Choose crop place
#Choose color to select
#Extract cropped Frames every second    Check
#Clean Frames
#OCR Frames
#Generate SRT