from Video import Video

#cropImage(0, 0, 100, 400, 'hey', FULL_PATH_OUT_EXTRACT_IMAGES)
#extractText()

v = Video("test.mp4")
v.createFolders()
v.extractFrames()
v.cleanFrames()
v.processFrames()
print(v.toString())