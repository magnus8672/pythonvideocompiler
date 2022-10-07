#make_compilation.py 
#magnus8672 9/2022
#A simple Tool for taking all the .mp4 video files in directory resizing them to 1080P and concatenating them to a single video file
#Use the PARAMS section to change variables for locations of input and output to match your file system layout.
#Remember to escape (bouble slash) any slash "\" characters in your file path as python will otherwise interpreate some combos of a "\" 
#and a letter as a control character and freak the heck out" C:\\some\\dir\\ == good. C:\some\dir\ == bad
#Set compile4YT to False if you do not have an intro and midrole and outtro clip to stuff into each video.

# Import everything needed to edit video clips
import os
import moviepy.editor as mp
from moviepy.editor import *
from datetime import datetime
import hashlib
import time
import configparser

#PARAMS. Change these to suit your environment
config = configparser.ConfigParser()
config.read('wwdmakecomp.ini')
bInputDir = config['options']['rootLocation']
bOutDir = config['options']['targetLocation']
bUtilDir = config['options']['utilityLocation']
compile4YT = config.getboolean('youtube', 'compileForYoutube')
introVid = config['youtube']['introFileName']
midroleVid = config['youtube']['midRoleFileName']
outtroVid = config['youtube']['outtroFileName']
#END OF PARAMS


#instantiate empy global to store list of clips
clips = []

#get current date for output video name
date = datetime.now().strftime("%Y_%m_%d-%I_%M")

#specify location of outoging video
vout = bOutDir + str(date) + '_output.mp4'

#ensure there are no duplicate video files in the folder
#if you ran feddit against two related sub reddits sometimes people cross post
MD5s = []

for filename in os.listdir(bInputDir):
    with open(bInputDir + filename, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()    
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        md5str = str(md5_returned)
        file_to_check.close()
        if md5str in MD5s:
            print("Duplicate Video Found" + filename )
            os.remove(bInputDir + filename)
        else:
            MD5s.append(md5str)

#Once duplicate files are cleaned from the folder 
#Check MD5s of remaing videos against list of previously encountered clips 
#and delete repeats.
md5file = open("md5.log", "r")
md5s = md5file.read()
print("List of known MD5 sums")
print(md5s)
for filename in os.listdir(bInputDir):
    with open(bInputDir + filename, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()    
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        md5str = str(md5_returned)
        file_to_check.close()
        if md5str in md5s:
            print("MD5 Match found, delete previously encountered clip")
            print("removing previously used clip" + filename)
            #time.sleep(5)
            os.remove(bInputDir + filename)


#get the MD5sum of each video in the diretory and store it
#open MD5 log for writing
md5log = open("md5.log", "a")
#Append Md5 value of each video in the input dir 
for filename in os.listdir(bInputDir):
    with open(bInputDir + filename, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()    
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        md5str = str(md5_returned)
        print(md5str)
        md5log.write(md5str + "\n")
        file_to_check.close()

#close md5log for writing        
md5log.close()

#compile list of video clips from a target directory
for filename in os.listdir(bInputDir):
    if filename.endswith(".mp4"):
        #find clips with weird sizes and get rid of them, make the rest 1080p
        clip = mp.VideoFileClip((bInputDir + filename))
        #resize clip to 1080p
        clip_resized = clip.resize(height=1080)
        clip_resized.write_videofile(bInputDir + '\\resized_' + filename)
        #Some clips resize to dumb sizes that make youtube explode. delete them
        if (clip_resized.w % 2) == 0:
                    print("width after resize: " + str(clip_resized.w))                   
                    #append resized clip to list
                    clips.append(VideoFileClip(bInputDir + '\\resized_' + filename))
        else:
            print("found invalid sized file: " + str(filename))
            dfile = bInputDir + filename
            os.remove(dfile)
            rdfile = bInputDir + '\\resized_' + filename
            os.remove(rdfile)

#get the number of clips
cnum = len(clips)

#find roughly the middle index value
mnum = round(cnum/2)

if compile4YT == True:
    #add pre role to index 0 of clips
    clips.insert(0, VideoFileClip(bUtilDir + introVid))

    #add mid role to middle index of clips list
    clips.insert(mnum, VideoFileClip(bUtilDir + midroleVid))

    #add closing clip to clips list
    clips.append(VideoFileClip(bUtilDir + outtroVid))

#compile all clips in the list into a single video and place in target location specified above.
video = concatenate_videoclips(clips, method='compose')
video.write_videofile(vout)
