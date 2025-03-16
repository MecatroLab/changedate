# changedate
Here is a project which aims at changing automatically photos/videos' date, useful when you receive photos from your friend or when you download files from your camera, and disappear in your gallery cause the date is wrong :)

You have two files, because I've made two versions. The first one only works for photos, the second one works for all photos and videos.
Why I've left the first version? Because it is simpler and it doesn't use ffmpeg, which can cause troubles.

To make it work : 
- Open the file in a python interpreter and download the libraries if necessary.
- Download all the files whose date you want to change in a folder.
- Copy the folder's path into the python file in the variable directory.
- Chose the new date in the variable new_date.
- Execute the code !

Possibles errors:
- Python cannot access your files : make sure that the python interpreter you use is allowed to access the folder.
- The code stops when it's processing a video : make sure that the ffmpeg path is righ, it depends of your OS. If ffmpeg is not install on your computer, install it by using the terminal.
