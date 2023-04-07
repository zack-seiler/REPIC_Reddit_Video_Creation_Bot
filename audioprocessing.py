"""
This module provides utilities for splitting and stitching audio files.
It includes functionality to extract audio from video files and to
combine audio files with silence between them.
"""

import os
import subprocess
from pydub import AudioSegment
from wavesplitter import WaveSplitter


def call_split_class():
    """
    Splits a given audio file into smaller segments based on a specified minimum duration.

    This was only used for creating the audio segments from the master file, and is unused in the project.
    """

    folder = os.path.join(os.getcwd(), "\\Audio\\Audio_Segments")
    file = 'audio.wav'
    split_wav = WaveSplitter(folder, file)
    split_wav.multiple_split(min_per_split=1)


def audio_from_video(mp4_file_name):
    """
    Extracts audio from a given mp4 video file and saves the audio as a .wav file.

    This was only used for stripping the master audio clip from the NCS video, and is unused in the project.

    Args:
        mp4_file_name (str): The name of the mp4 file to extract audio from.
    """

    command = "ffmpeg -i " + str(os.path.join(os.getcwd(), "\\Audio\\Audio_Segments")) + str(mp4_file_name) + \
              ".mp4 -ab 160k -ac 2 -ar 44100 -vn " +\
              str(os.path.join(os.getcwd(), "\\Audio\\Audio_Segments\\audio.wav"))
    subprocess.call(command, shell=True)


def stitch_audio():
    """
    Stitches audio files found in the "Data_Cache" directory with a second of silence between each.
    The stitched audio file is exported as "Stitched_Audio.wav".

    Returns:
        int: The number of audio files stitched together.
    """

    combined = None
    file_list = []

    # Add .wav files to the file_list
    for item in os.listdir(os.path.join(os.getcwd(), "Data_Cache")):
        if item.endswith(".wav"):
            file_list.append(item)

    # Create a second of silence to be added between audio segments
    second_of_silence = AudioSegment.silent(duration=1000)

    # Load the subreddit name and post title audio segments
    combined = AudioSegment.from_file(os.path.join(os.getcwd(), "Data_Cache\\Subreddit_Name.wav"))
    sound = AudioSegment.from_file(os.path.join(os.getcwd(), "Data_Cache\\Post_Title.wav"))

    # Concatenate subreddit name, post title, and a second of silence
    combined += sound
    combined += second_of_silence

    # Sort the list of .wav files and remove the last two elements (Subreddit_Name.wav and Post_Title.wav)
    file_list.sort()
    file_list = file_list[:-2]
    counter = 0

    # Iterate over the file_list and stitch the comment audio files together
    for counter, item in enumerate(file_list):
        sound = AudioSegment.from_file(os.path.join(os.getcwd(), "Data_Cache\\Comment_#" + str(counter + 1) + ".wav"))

        # Check if the addition of the current sound segment and a second of silence would exceed 59 seconds
        if (combined + sound + second_of_silence).duration_seconds >= 59:

            # Export the stitched audio and return the number of files stitched
            combined.export(os.path.join(os.getcwd(), "Stitched_Audio.wav"), format="wav")
            return counter

        else:

            # Add the sound segment and a second of silence to the combined audio
            combined += sound
            combined += second_of_silence

    # Export the stitched audio
    combined.export(os.path.join(os.getcwd(), "Stitched_Audio.wav"), format="wav")
    print("Stitched Audio Successfully")

    # Return the number of audio files stitched together
    return counter


