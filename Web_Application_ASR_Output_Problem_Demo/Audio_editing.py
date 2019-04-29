import contextlib
import wave
import scipy.io
from scipy.io import wavfile
import numpy as np
from ASR_Processing.Recognize_Audio import recognise_audio


def open_wav(input_file: str) -> tuple:
    """
    Function to open a wav file
    :param input_file: file name
    :return: file parameters (tuple containing channels, sampwidth, framerate, totalframes, compressiontype, compressionname
    """
    r = wave.open(input_file, 'r')
    file_parameters = r.getparams()

    rate, data = scipy.io.wavfile.read(input_file)

    return file_parameters, data


def determine_duration(input_file: str) -> float:
    """
    Function to determine the duration of an audio file
    :param input_file: name of the file to be processed
    :return: the duration of the file as a float
    """
    with contextlib.closing(wave.open(input_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = round(frames / float(rate), 2)

    return duration


def determine_duration_silence(input_file: str) -> float:
    """
    Function to determine the duration of silence in a wav file
    :param input_file: the file to be analysed
    :return:
    """
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    silent_frames = []

    for i in range(len(data)):
        if data[i][0] >= -40  and data[i][0] <= 40:
            silent_frames.append(data[i])
        else:
            pass

    data2 = np.asarray(silent_frames, dtype=np.int16)

    scipy.io.wavfile.write('../Silence' + '.wav', frame_rate, data2)

    return determine_duration('../Silence.wav')


def remove_silence(input_file: str, output_file: str) -> None:
    """
    Function to remove silence from a wav file
    :param input_file: file name of file to be modified
    :param output_file: name of the file to be created
    :return: None
    """

    # Read the wav file and get rate and list of data
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    # Create list for data of amended wav file
    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i][0] >= -40 and data[i][0] <= 40:
            pass
        else:
            data2.append(data[i])

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write(output_file, frame_rate, data2)

    return None


def increase_overall_amplitude(input_file: str, output_file: str):
    """
    Function to increase the overall amplitude of an audio file
    :param input_file: name of the file to be edited.
    :param output_file: name of the file to be created
    :return: None
    """
    # Read the wav file and get rate and list of data
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    # Create list for data of amended wav file
    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i].all() < 0:
            data2.append(data[i] - 2000)
        else:
            data2.append(data[i] + 2000)

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write('/Users/benjaminhewett/Desktop/' + output_file, frame_rate, data2)

    return None


def decrease_overall_amplitude(input_file: str, output_file: str):
    """
    Function to decrease the amplitude of an audio file
    :param input_file: name of the file to be edited
    :param output_file: name of the file to be created
    :return: None
    """
    # Read the wav file and get rate and list of data
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    # Create list for data of amended wav file
    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i].all() < 0:
            data2.append(data[i] + 2000)
        else:
            data2.append(data[i] - 2000)

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write('/Users/benjaminhewett/Desktop/' + output_file, frame_rate, data2)

    return None


def remove_all_sound(input_file: str, output_file: str):
    """
    Function to remove all sound from a file.
    File duration remains intact.
    :param input_file: name of the file to be edited.
    :param output_file: name of the file to be created
    :return: None
    """
    # Read the wav file and get rate and list of data
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    # Create list for data of amended wav file
    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i].all() < 0:
            data2.append(data[i] + data[i])
        else:
            data2.append(data[i] - data[i])

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write('/Users/benjaminhewett/Desktop/' + output_file, frame_rate, data2)

    return None


def get_specific_duration(input_file: str, output_file: str, start: float, end: float) -> str:
    """
    Function to extract a specified duration of audio from a file
    :param input_file: the name of the file to be edited
    :param output_file: name of the file to be created
    :param start: the start time
    :param end: the end time
    :return: None if successful, error message if not
    """
    # Read the wav file and get rate and list of data
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    file_duration = determine_duration(input_file)

    if end <= file_duration:
        start_location = round((len(data) / file_duration) * start)
        end_location = round((len(data) / file_duration) * end)

        # Create list for data of amended wav file
        data2 = []

        # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
        for i in range(start_location, end_location):
            data2.append(data[i])

        # Create NumPy array from revised data
        data2 = np.asarray(data2, dtype=np.int16)

        # Write new data to wav file
        scipy.io.wavfile.write(output_file, frame_rate, data2)

        return data2
    else:
        return 'Required duration longer than file duration'


def add_silence_front_back(input_file: str, output_file: str, duration_start=0.0, duration_end=0.0) -> None:
    """
    Function to add n seconds of silence to front and/or back of audio
    :param input_file: input file name
    :param output_file: output file name
    :param duration_start: duration of silence to add at start
    :param duration_end: duration of silence to add at end
    :return: None
    """
    params_data = open_wav(input_file)

    data = params_data[1]
    frame_rate = params_data[0][2]

    duration = determine_duration(input_file)

    number_frames_to_add_start = round((len(data) / duration) * duration_start)

    number_frames_to_add_end = round((len(data) / duration) * duration_end)

    silence_start = np.zeros((number_frames_to_add_start, 2), dtype=np.int16, order='C')
    silence_end = np.zeros((number_frames_to_add_end, 2), dtype=np.int16, order='C')

    data2 = np.concatenate((silence_start, data, silence_end), axis=0)

    # Write new data to wav file
    scipy.io.wavfile.write('/Users/benjaminhewett/Desktop/' + output_file, frame_rate, data2)

    return None


def remove_silence_front(input_file: str, output_file: str):
    """
    Function to remove silence from front of file
    :param input_file: input file name
    :param output_file: output file name
    :return: None
    """
    params_data = open_wav(input_file)

    data = params_data[1]
    params = params_data[0]
    frame_rate = params[2]

    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i][0] >= -50 and data[i][1] <= 50:
            pass
        else:
            for j in range(i, len(data[i:])):
                data2.append(data[j])
            break

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write(output_file, frame_rate, data2)

    return None


def remove_silence_rear(input_file: str, output_file: str):
    """
    Function to remove silence from rear of file
    :param input_file: input file name
    :param output_file: output file name
    :return: None
    """
    params_data = open_wav(input_file)

    data = params_data[1]
    params = params_data[0]
    frame_rate = params[2]

    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)-1, -1, -1):
        if data[i][0] >= -50 and data[i][1] <= 50:
            pass
        else:
            stop = i
            for j in range(stop):
                data2.append(data[j])
            break

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write(output_file, frame_rate, data2)

    return None


def insert_silence(input_file: str, output_file: str):
    """
    Function to add a segment of silence wherever a segment of silence appears in the audio
    :param input_file: input file name
    :param output_file: output file name
    :return: None
    """
    params_data = open_wav(input_file)

    data = params_data[1]
    params = params_data[0]
    frame_rate = params[2]

    data2 = []

    silence = np.zeros((1, 2), dtype=np.int16, order='C')

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i][0] >= -10 and data[i][1] <= 10:
            data2.append(data[i])
            data2.append(silence[0])
        else:
            data2.append(data[i])

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write(output_file, frame_rate, data2)

    return None


def asr_by_chunk(input_file: str):
    """
    Slices audio file into chunks of duration 2.5 seconds and processes through ASR
    If value returned by chunk is not unknown, adds to result string
    :param input_file:
    :return: ASR text
    """

    file_output = '/Users/benjaminhewett/Desktop/Test/Hen_no.wav'
    # remove_silence(input_file, file_output)

    duration = determine_duration(input_file)

    time_chunks = []

    start = 0.0
    finish = 5.0
    counter = duration

    while True:
        if counter > 0.0 and counter > 5.0:

            time_chunks.append([start, finish])
            start = finish
            finish = finish + 4.95
            counter -= 4.95
            continue
        else:
            time_chunks.append([start, duration])
            break

    file = '/Users/benjaminhewett/Desktop/Test/Test_file_blocks1'
    num = 2
    full_text = ''

    for chunk in time_chunks:
        get_specific_duration(input_file, file + '.wav', chunk[0], chunk[1])
        text = recognise_audio(file + '.wav')
        file = file[:-1] + str(num)
        num += 1
        if text != 'Unknown Value':
            full_text += ' ' + text

    return full_text
