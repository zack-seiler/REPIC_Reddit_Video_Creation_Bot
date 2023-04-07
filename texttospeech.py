import pyttsx3
import os
from google.cloud import texttospeech

credential_path = "E:\\MEMPHIS_AI\\memphis-ai-e42646e3a2e0.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def main(text, name):
    """
    Generate speech from input text and save it as a wav file.

    Args:
        text (str): The text to convert to speech.
        name (str): The file name for the generated wav file.
    """

    synthesis_input = texttospeech.SynthesisInput({"text": text})

    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.VoiceSelectionParams({
        "name": 'en-US-Wavenet-J',
        "language_code": 'en-US'
    })

    audio_config = texttospeech.AudioConfig({
        "audio_encoding": texttospeech.AudioEncoding.LINEAR16,
        "pitch": 0
    })

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(os.path.join(os.getcwd(), "Data_Cache\\" + str(name)) + ".wav", 'wb') as output:
        output.write(response.audio_content)
    output.close()


def robo_speak(text):
    """
    Use the pyttsx3 library to convert text to speech and play it.

    Args:
        text (str): The text to convert to speech.
    """

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 120)
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    main()
