# rEPIC - Reddit Post Video Creation Tool
rEPIC is a Python-based tool that generates videos using Reddit posts and comments. It utilizes Reddit's API and several libraries to process the text and generate audio, images, and video. The generated videos can be used for entertainment, educational purposes, and social media content.

# Setup
# Required Dependencies
To use rEPIC, the following libraries must be installed:

praw
requests
re
unidecode
PIL
textwrap
os
google.cloud text to speech
pyttsx3
pydub
contextlib
wave
moviepy

You must also make a reddit bot and it's Client ID and Client Secret must be stored in a text file called "Client_Tokens.txt" with the Client ID placed on the first line of the text file, and the Client Secret on the second line.

All you have to do to generate a video is find a reddit post, copy the link to the post (not the subreddit), and paste it in the url_list variable. You can add as many posts as you would like, and the program will generate them sequentially automatically.
NOTE: Video length is limited to one minute, so try to find posts with many shorter comments, rather than posts with long comments.

# Audio and Video Files
To generate videos using rEPIC, you must place your own audio file in the Audio folder and your own background video file in the Video folder. Be sure to specify the start times to be randomly selected from the video file using the start_time_list in videoprocessing.py

# Usage
# Running the Program
To run the program, navigate to the directory where the main.py file is located and enter the following command in the terminal:

python main.py

# URL List
The url_list variable in the main function contains a list of all URLs that the script will create videos from. Each item in the list must be a Reddit post URL, and a new video will be created for each item in the list.

# Output
The final video file will be saved in the same directory as the main.py file with the name of the original post title.

# Cleaning Up
The program automatically clears out all cached data and pre-generated audio/video files.
