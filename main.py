import os

import praw
import texttospeech
import drawtext
import audioprocessing
import videoprocessing
import requests
import re
from unidecode import unidecode


def find_urls(text):
    """
    Finds all URLs in the given text using regular expressions.

    Args:
        text (str): The text to search for URLs.

    Returns:
        list: A list of URLs found in the text.
    """

    return re.findall(r'(https?://[^\s]+)', text)


def contains_profanity(text):
    """
    Checks if the given text contains profanity using the Purgomalum API.

    Args:
        text (str): The text to check for profanity.

    Returns:
        bool: True if the text contains profanity, False otherwise.
    """

    profanity = requests.get("https://www.purgomalum.com/service/containsprofanity?text=" + str(text))
    if profanity.text == 'true':
        print("Input contains profanity")
        return True
    elif profanity.text == 'false':
        print("Input does not contain profanity")
        return False
    else:
        print("ERROR. Cannot determine profanity")
        return False


def censor_profanity(text):
    """
    Censors profanity in the given text using the Purgomalum API.

    Args:
        text (str): The text to censor profanity.

    Returns:
        str: The text with profanity censored.
    """

    print("Censoring text...")
    return requests.get("https://www.purgomalum.com/service/plain?text=" + str(text) + "&fill_char=*").text


def get_comment_list(post, comment_limit):
    """
    Retrieves a list of comments from the given Reddit post object.

    Args:
        post (praw.models.Submission): A Reddit post object.
        comment_limit (int): The maximum number of comments to retrieve.

    Returns:
        list: A list of comments from the post.
    """

    comment_counter = 0
    comments = []
    for top_level_comment in post.comments:
        comment = top_level_comment.body
        if comment == '[deleted]' or comment == '[removed]':
            continue
        comment = decode_unicode(comment)
        comment = remove_symbols(comment)
        print("VALID: " + comment)
        comment_counter += 1
        if count_words(comment) <= 75:
            print("Comment #", comment_counter, ":", comment)

            comment_urls = find_urls(comment)
            print(comment_urls)

            if comment_urls:
                for item in comment_urls:
                    print("URL found in comment #", comment_counter, "... Removing")
                    comment = comment.replace(item, "")
                    comment_urls.clear()

            if contains_profanity(comment) is True:
                censored_comment = censor_profanity(comment)
                censored_comment = re.sub('\\*\\*+', '*', censored_comment)
                print("Censored comment: " + censored_comment)
                print("DECODED COMMENT: ", censored_comment)
                comments.append(censored_comment)
            else:
                comments.append(str(comment))

        else:
            print("COMMENT TOO LONG!!!")
            comment_counter -= 1
        print("\n---------------------------------------------------\n")

        if comment_counter == comment_limit:
            break
    return comments


def generate_audio(subreddit_name, title, comments):
    """
    Generates audio files for the subreddit name, post title, and comments using text-to-speech.

    Args:
        subreddit_name (str): The name of the subreddit.
        title (str): The title of the post.
        comments (list): A list of comments from the post.
    """

    texttospeech.main("r slash" + subreddit_name, "Subreddit_Name")
    print("Generated Subreddit Name Audio")
    texttospeech.main(title, "Post_Title")
    print("Generated Post Title Audio")
    for counter, item in enumerate(comments):
        texttospeech.main(item, "Comment_#" + str(counter + 1))
        print("Generated " + "Comment_#" + str(counter + 1) + " Audio")


def remove_invalid_file_characters(filename):
    """
    Removes invalid characters from a filename.

    Args:
        filename (str): The original filename.

    Returns:
        str: The filename with invalid characters removed.
    """

    invalid_characters = ['/', '\\', '*', ':', '?', '<', '>', '|', '"', '”', '’']
    for character in invalid_characters:
        filename = filename.replace(character, '')
    return filename


def decode_unicode(text):
    """
    Decodes Unicode characters in the given text using the unidecode library.

    Args:
        text (str): The text to decode.

    Returns:
        str: The decoded text.
    """

    return unidecode(text)


def remove_symbols(data):
    """
    Removes symbols from the given data using regular expressions.

    Args:
        data (str): The data to remove symbols from.

    Returns:
        str: The data with symbols removed.
    """

    symbol = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002500-\U00002BEF"  # chinese char
                        u"\U00002702-\U000027B0"
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u200d"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"
                        "]+", re.UNICODE)
    return re.sub(symbol, '', data)


def count_words(text):
    """
    Counts the number of words in the given text.

    Args:
        text (str): The text to count words.

    Returns:
        int: The number of words in the text.
    """

    word_count = len(text.split())
    print(word_count, " word(s)")
    return word_count


def generate_images(image_text_input, style):
    """
    Generates images of text from the given text input using the specified style.

    Args:
        image_text_input (str or list): The text input for generating images.
        style (int): The style to apply to the images (1, 2, or 3).
    """

    if type(image_text_input) is list:
        counter = 0
        for item in image_text_input:
            counter += 1
            name = "Comment #" + str(counter)
            drawtext.create_image(item, name, style)
            print("Generated image for ", name)
    else:
        name = "Intro " + remove_invalid_file_characters(image_text_input)
        drawtext.create_image(image_text_input, name, style)


def clear_data():
    """
    Removes generated files and directories.
    """

    path = os.getcwd()
    try:
        os.remove(os.path.join(path, "Final_Video.mp4"))
        os.remove(os.path.join(path, "Stitched_Audio.wav"))

        path = os.path.join(os.getcwd(), "Data_Cache")
        file_list_for_removal = os.listdir(path)

        for item in file_list_for_removal:
            os.remove(os.path.join(path, item))
    except FileNotFoundError:
        print("Files cannot be removed, no such files or directories.")


def main():
    """
    Main function of the script. Processes Reddit comments, generates audio and video files, and cleans up.
    """

    # List of all URLs that the script will create videos from
    # Each item in the list must be a reddit post URL
    # A new video will be created for each item in the list
    url_list = ["https://www.reddit.com/r/SubReddit/comments/ID/post_title_1/",
                "https://www.reddit.com/r/SubReddit/comments/ID/post_title_2/",
                "https://www.reddit.com/r/SubReddit/comments/ID/post_title_3/"]

    def read_api_tokens(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            client_id_from_file = lines[0].strip()
            client_secret_from_file = lines[1].strip()
        return client_id_from_file, client_secret_from_file

    client_id, client_secret = read_api_tokens('Client_Tokens.txt')

    for url in url_list:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="Reddit scraper 1.0 /u/kennyredditbot",
        )

        clear_data()

        post = reddit.submission(url=url)
        subreddit_name = str(post.subreddit)
        title = post.title

        comments = get_comment_list(post, 10)

        generate_audio(subreddit_name, title, comments)

        generate_images(subreddit_name, style=2)
        generate_images(title, style=3)
        generate_images(comments, style=1)

        number_of_comments = audioprocessing.stitch_audio()
        print("Number of comments = ", number_of_comments)
        videoprocessing.create_video(number_of_comments, subreddit_name, title)

        clear_data()


if __name__ == '__main__':
    main()
