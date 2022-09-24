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

#PARAMS. Change these to suite your environment
#Base Output Dirtectory. The place your final video will go. Make sure it exists.
bOutDir = 'D:\\somedir\\on\\your\\D\\drive\\'
#Base Iput Directory. The place you will take all your clips from to convert them to a single video
bInputDir = 'D:\\some\\OTHER\\DIR\\on\\your\\D\\drive\\'
#Base utility Dir. The place where you will store Intro, Midrole and Outtro clips to add to the video
bUtilDir = 'D:\\some\\third\\DIR\\'
#Into Midrole and Outtro file names. If you want to be a fancy pants, 
#use these along with compile4YT flag to add specific mp4's to the front middle and end of your compilation.
introVid = 'somefile.mp4'
midroleVid = 'anotherfile.mp4'
outtroVid = 'thirdfile.mp4'
#BOOL to add intro/midrole/outtro
compile4YT = False
#END OF PARAMS


#instantiate empy global to store list of clips
clips = []

#get current date for output video name
date = datetime.now().strftime("%Y_%m_%d-%I_%M")

#specify location of outoging video
vout = bOutDir + str(date) + '_output.mp4'

#compile list of video clips from a target directory
for filename in os.listdir(bInputDir):
    if filename.endswith(".mp4"):
        #resize clip to 1080p
        clip = mp.VideoFileClip((bInputDir + filename))
        clip_resized = clip.resize(height=1080)
        clip_resized.write_videofile(bInputDir + '\\resized_' + filename)
        
        #append resized clip to list
        clips.append(VideoFileClip(bInputDir + '\\resized_' + filename))

#get the number of clips
cnum = len(clips)

#find roughly the middle index value
mnum = round(cnum/2)

if compile4YT == True:
    #add intro video to index 0 of clips
    clips.insert(0, VideoFileClip(bUtilDir + introVid))

    #add mid role to middle index of clips list
    clips.insert(mnum, VideoFileClip(bUtilDir + midroleVid))

    #add closing outtro clip to clips list
    clips.append(VideoFileClip(bUtilDir + outtroVid))

#compile all clips in the list into a single video and place in target location specified above.
video = concatenate_videoclips(clips, method='compose')
video.write_videofile(vout)
