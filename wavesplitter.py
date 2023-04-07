"""
Module: WaveSplitter
---------------------

A Python class that provides methods to split a .wav audio file into smaller parts.

Usage ----- 1. Create an instance of the WaveSplitter class by providing the path of the folder containing the .wav
file and the name of the file.

    Example:
    ```
    splitter = WaveSplitter(folder='path/to/folder', filename='audio_file.wav')
    ```

2. Use the `single_split` method to split the audio file into smaller parts of specified duration.

    Example:
    ```
    splitter.single_split(from_min=1, to_min=2, split_filename='audio_part1.wav')
    ```

3. Use the `multiple_split` method to split the audio file into multiple parts of equal duration.

    Example:
    ```
    splitter.multiple_split(min_per_split=5)
    ```

Classes
-------
WaveSplitter(folder: str, filename: str)
    A class that represents an audio file and provides methods to split it into smaller parts.

    Methods:
    --------
    get_duration() -> float
        Returns the duration of the audio file in seconds.

    single_split(from_min: float, to_min: float, split_filename: str) -> None
        Splits the audio file into a smaller part from `from_min` to `to_min` minutes and saves it with the provided filename.

    multiple_split(min_per_split: float) -> None
        Splits the audio file into multiple smaller parts of `min_per_split` minutes each.

"""

from pydub import AudioSegment
import math


class WaveSplitter:
    """
    A class that represents an audio file and provides methods to split it into smaller parts.

    Parameters
    ----------
    folder : str
        The path of the folder containing the .wav file.
    filename : str
        The name of the .wav file.

    Attributes
    ----------
    folder : str
        The path of the folder containing the .wav file.
    filename : str
        The name of the .wav file.
    filepath : str
        The full path of the .wav file.
    audio : AudioSegment
        The audio file represented as an AudioSegment object.
    """

    def __init__(self, folder: str, filename: str) -> None:
        """
        Initializes the WaveSplitter class.

        Parameters
        ----------
        folder : str
            The path of the folder containing the .wav file.
        filename : str
            The name of the .wav file.
        """
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self) -> float:
        """
        Returns the duration of the audio file in seconds.

        Returns
        -------
        duration : float
            The duration of the audio file in seconds.
        """
        return self.audio.duration_seconds

    def single_split(self, from_min: float, to_min: float, split_filename: str) -> None:
        """
        Splits the audio file into a smaller part from `from_min` to `to_min` minutes and saves it with the provided filename.

        Parameters
        ----------
        from_min : float
            The starting minute of the smaller part.
        to_min : float
            The ending minute of the smaller part.
        split_filename : str
            The filename to save the smaller part.

        Returns
        -------
        None
        """
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '\\' + split_filename, format="wav")


def multiple_split(self, min_per_split: float) -> None:
    """
    Splits the audio file into multiple smaller parts of `min_per_split` minutes each.

    Parameters
    ----------
    min_per_split : float
        The duration of each smaller part in minutes.

    Returns
    -------
    None
    """
    total_minutes = math.ceil(self.get_duration() / 60)
    for i in range(0, total_minutes, min_per_split):
        split_fn = str(i) + '_' + self.filename
        self.single_split(i, i + min_per_split, split_fn)
        print(str(i) + ' Done')
        if i == total_minutes - min_per_split:
            print('All split successfully')
