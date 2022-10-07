# pythonvideocompiler
compile individual mp4 clips into a single video file.
#make_compilation.py 
#magnus8672 9/2022
#A simple Tool for taking all the .mp4 video files in directory resizing them to 1080P and concatenating them to a single video file
#Use the INI file  to change variables for locations of input and output to match your file system layout.
#Remember to escape (bouble slash) any slash "\" characters in your file path as python will otherwise interpreate some combos of a "\" 
#and a letter as a control character and freak the heck out" C:\\\some\\\dir\\\ == good. C:\some\dir\ == bad
#Set compile4YT to False if you do not have an intro and midrole and outtro clip to stuff into each video.
