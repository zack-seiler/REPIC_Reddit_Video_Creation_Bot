from moviepy.editor import *
import os
import wave
import contextlib
import random
import main


def get_duration(file_name):
    """
    Return the duration of a WAV file in seconds.

    Args:
        file_name (str): The name of the WAV file.

    Returns:
        float: The duration of the WAV file in seconds.
    """

    with contextlib.closing(wave.open(file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def create_video(length, subreddit_name, title):
    """
    Create a video by merging an audio clip with a background video and adding image and text clips.
    Add a music clip to the final video.

    Args:
        length (int): The number of comments to include in the video.
        subreddit_name (str): The name of the subreddit to include in the video.
        title (str): The title of the post to include in the video.

    Returns:
        None
    """

    # List of start times gathered from the source video file in which the video cuts
    # ensuring a video never begins on a cut.
    start_time_list = [0, 52, 95, 152, 192, 220, 257, 347, 406, 458, 487]
    video_start_time = random.choice(start_time_list)

    # Load audio clip
    audio_clip = AudioFileClip(os.path.join(os.getcwd(), "Stitched_Audio.wav"))

    # Load background video clip
    video = VideoFileClip(os.path.join(os.getcwd(), "Video\\Vaporwave Background Series 1.mp4"))
    video_clip = video.subclip(video_start_time, video_start_time + int(audio_clip.duration))

    # Set duration and audio of the video clip
    video_clip = video_clip.set_duration(audio_clip.duration)
    video_clip = video_clip.set_audio(audio_clip)

    # Calculate the duration of the subreddit and post title clips
    subreddit_title_duration = get_duration(os.path.join(os.getcwd(), "Data_Cache\\Subreddit_Name.wav"))
    post_title_duration = get_duration(os.path.join(os.getcwd(), "Data_Cache\\Post_Title.wav"))

    # Set the delay for the comment image clips
    image_start_delay = subreddit_title_duration + post_title_duration + 1

    # Load subreddit title image clip
    subreddit_card = ImageClip(os.path.join(os.getcwd(), "Data_Cache\\Subreddit_Title.png")).set_start(
        0).set_duration(subreddit_title_duration).set_pos(("center", "center"))

    # Load post title image clip
    post_title_card = ImageClip(os.path.join(os.getcwd(), "Data_Cache\\Post_Title.png")).set_start(
        subreddit_title_duration).set_duration(post_title_duration).set_pos(("center", "center"))

    # Load and add comment image clips to the list
    comment_image_clip_list = []

    for i in range(0, length):
        current_comment_duration = get_duration(
            os.path.join(os.getcwd(), "Data_Cache\\Comment_#" + str(i + 1) + ".wav"))
        comment = ImageClip(os.path.join(os.getcwd(), "Data_Cache\\Comment #" + str(i + 1) + ".png")).set_start(
            image_start_delay).set_duration(current_comment_duration + 1).set_pos(("center", "center"))

        comment_image_clip_list.append(comment)

        image_start_delay += current_comment_duration + 1

    # Create the final video clip by merging all clips
    final_video = CompositeVideoClip([video_clip,
                                      subreddit_card,
                                      post_title_card,
                                      *comment_image_clip_list])

    # Set the video title
    video_title = "r" + subreddit_name + " - " + title

    # Write the final video to the file
    final_video.write_videofile(os.path.join(os.getcwd(), "Final_Video.mp4"), fps=30)

    # Load the final video clip with audio
    video_for_music = VideoFileClip(os.path.join(os.getcwd(), "Final_Video.mp4"))

    # Load the music clip
    music = AudioFileClip(os.path.join(os.getcwd(), "Audio\\Audio Base.wav"))

    # Get the duration and start time of the music clip
    music_duration = int(get_duration(os.path.join(os.getcwd(), "Audio\\Audio Base.wav")))
    start_time = random.randint(10, music_duration - 120)

    # Get the total duration of the audio clip and create a subclip of the music clip with the same duration
    total_duration = int(get_duration(os.path.join(os.getcwd(), "Stitched_Audio.wav")))
    music_clip = music.subclip(start_time, start_time + total_duration)

    # Adjust the volume of the music clip
    music_clip = music_clip.volumex(0.2)

    # Merge the audio of the final video clip with the music clip
    final_video_sound = CompositeAudioClip([video_for_music.audio, music_clip])
    video_for_music.audio = final_video_sound

    # Write the final video with the music to the file
    video_for_music.write_videofile(os.path.join(os.getcwd(), main.remove_invalid_file_characters(video_title) + ".mp4"),
                                    fps=30)
