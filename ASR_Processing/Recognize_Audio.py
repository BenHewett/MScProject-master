import speech_recognition as sr
import wave
import contextlib
import math
from collections import Counter
from mysql import connector
import re
import os

"""
Processes audio files of specific scripts of text from .wav to string using ASR.
Calculates a percentage accuracy of the original script - recognized text conversion.
"""

########################################################################################################################
# Scripts (formatted and counted)

r1 = 'When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is ' \
     'a division of white light into many beautiful colours. These take the shape of a long round arch, with its ' \
     'path high above, and its two ends apparently beyond the horizon. There is, according to legend, a boiling ' \
     'pot of gold at one end. People look, but no one ever finds it. When a man looks for something beyond his ' \
     'reach, his friends say he is looking for the pot of gold at the end of the rainbow.'\
    .lower().replace('.', '').replace(',', '').replace("'", '')

r1_count = len(re.findall(r'\w+', r1))

r2 = 'Throughout the centuries people have explained the rainbow in various ways. Some have ' \
     'accepted it as a miracle without physical explanation. To the Hebrews it was a token that there ' \
     'would be no more universal floods. The Greeks used to imagine that it was a sign from the gods to ' \
     'foretell war or heavy rain. The Norsemen considered the rainbow as a bridge over which the gods passed ' \
     'from earth to their home in the sky. Others have tried to explain the phenomenon physically. Aristotle ' \
     'thought that the rainbow was caused by reflection of the sun\'s rays by the rain.'.lower().replace('.', '')\
    .replace(',', '').replace("'", '')

r2_count = len(re.findall(r'\w+', r2))

r3 = 'Since then physicists have found that it is not reflection, but refraction by the raindrops which causes ' \
     'the rainbows. Many complicated ideas about the rainbow have been formed. The difference in the rainbow ' \
     'depends considerably upon the size of the drops, and the width of the colored band increases as the size ' \
     'of the drops increases. The actual primary rainbow observed is said to be the effect of super-imposition ' \
     'of a number of bows. If the red of the second bow falls upon the green of the first, the result is to ' \
     'give a bow with an abnormally wide yellow band, since red and green light when mixed form yellow. This ' \
     'is a very common type of bow, one showing mainly red and yellow, with little or no green or blue.'.lower()\
    .replace('.', '').replace(',', '').replace("'", '')

r3_count = len(re.findall(r'\w+', r3))

g1 = 'You wished to know all about my grandfather. Well, he is nearly ninety-three years old; he dresses ' \
     'himself in an ancient black frock coat, usually minus several buttons; yet he still thinks as swiftly ' \
     'as ever. A long, flowing beard clings to his chin, giving those who observe him a pronounced feeling of ' \
     'the utmost respect. When he speaks, his voice is just a bit cracked and quivers a trifle. Twice each day ' \
     'he plays skilfully and with zest upon our small organ. Except in the winter when the ooze or snow or ice ' \
     'prevents, he slowly takes a short walk in the open air each day. We have often urged him to walk more and ' \
     'smoke less, but he always answers, “Banana oil!” Grandfather likes to be modern in his language.'.lower()\
    .replace('.', '').replace(',', '').replace("'", '')

g1_count = len(re.findall(r'\w+', r1))

########################################################################################################################

# Database connection and cursor objects
connection = connector.connect(user='root', password='elsamax1981',
                               host='localhost',
                               database='mscproject')

cursor = connection.cursor()

########################################################################################################################


def get_duration(filename: str) -> float:
    """
    Calculates the duration of an audio (.wav) file
    :param filename: the filename to calculate the duration
    :return: the duration (as a float) of the file rounded to two decimal places
    """
    with contextlib.closing(wave.open(filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    return round(duration, 2)


def recognise_audio(filename: str) -> tuple:
    """
    Processes an audio file through ASR
    :param filename: the file to be processed
    :return: tuple containing the string of recognised words and an integer word count
    """
    print(filename + ' is being recognized...')
    duration = get_duration(filename)
    # Create a Recognizer object
    recognizer = sr.Recognizer()

    # Store the audio data
    file = sr.AudioFile(filename)

    # Initialise empty String variable for storing result from recognizer
    recognized_text = ''

    # Length of some audio files causes the ASR to hang, therefore recognizing in chunks of 16 seconds
    # j = chunk duration
    # k = cumulative offset
    j = 16
    k = 0
    for i in range(math.ceil(duration/j)):
        with file as source:
            audio = recognizer.record(source, duration=j, offset=k)
            try:
                recognized_text += recognizer.recognize_google(audio) + ' '
                k += (j - 0.1)
            except sr.UnknownValueError:
                recognized_text = ''
            except sr.RequestError:
                recognized_text = ''

    recognized_text = recognized_text.lower().replace("'", '')

    recognized_text_count = len(re.findall(r'\w+', recognized_text))

    print(filename + ' recognition complete.')

    return recognized_text, recognized_text_count


def calculate_accuracy(filename: str, recognized_text: str) -> tuple:
    """
    Calculates the accuracy of the ASR text compared to the original script for each script ID.
    :param filename: the file being compared.
    :param recognized_text: string of recognized text.
    :return: tuple containing the number of words accurately recognized by ASR, accuracy as a percentage, any
    mis-recognitions.
    """

    script_ref = filename[(filename.find('!')) - 2: filename.find('!')]

    # Accuracy for script with reference R1
    if script_ref == 'R1':
        print(filename + ' is being analyzed...')

        # Counts the occurrences of each word in script and stores in a dictionary
        r1_counted_dict = Counter(r1.split(' '))

        # Splits the recognized text into word tokens and stores in a list
        recognized_list = list(recognized_text.split(' '))
        recognized_list.pop(len(recognized_list) - 1)  # Remove empty string at final index in list

        # Variable to hold accurate recognitions and mis-recognised words
        accuracy_count = 0
        mis_recs = []

        # Loops through list of recognized words:
        # If the word is in the dictionary of counted words and the number of occurrences is > 0
        # Increment accuracy count by 1 and decrement number of occurrences of that word in the counted dictionary
        # If word is in counted dictionary but the number of occurrences is == 0, add word to list of mis-recognitions
        # If the word is not in the counted dictionary, add the word to the list of mis-recognitions
        for line in recognized_list:
            if line in r1_counted_dict.keys():
                if r1_counted_dict[line] > 0:
                    accuracy_count += 1
                    r1_counted_dict[line] -= 1
                else:
                    mis_recs.append(line)
            else:
                mis_recs.append(line)

        # Turn list of mis-recognitions into a String
        mis_recs_str = ''
        for i in mis_recs:
            mis_recs_str += i + ' '

        print(filename + ' analysis complete.')

        # Return tuple of accuracy rate, number of mis-recognitions, mis-recognition string
        return accuracy_count / len(r1.split(' ')) * 100, len(mis_recs), mis_recs_str
    # Accuracy for script with reference R2
    # See comments for R1 for code explanation
    elif script_ref == 'R2':
        print(filename + ' is being analyzed...')

        r2_counted_dict = Counter(r2.split(' '))

        recognized_list = list(recognized_text.split(' '))
        recognized_list.pop(len(recognized_list) - 1)  # Remove empty string at final index in list

        accuracy_count = 0
        mis_recs = []
        for line in recognized_list:
            if line in r2_counted_dict.keys():
                if r2_counted_dict[line] > 0:
                    accuracy_count += 1
                    r2_counted_dict[line] -= 1
                else:
                    mis_recs.append(line)
            else:
                mis_recs.append(line)

        mis_recs_str = ''
        for i in mis_recs:
            mis_recs_str += i + ' '

        print(filename + ' analysis complete.')
        return accuracy_count / len(r2.split(' ')) * 100, len(mis_recs), mis_recs_str
    # Accuracy for script with reference R3
    # See comments for R1 for code explanation
    elif script_ref == 'R3':
        print(filename + ' is being analyzed...')

        r3_counted_dict = Counter(r3.split(' '))

        recognized_list = list(recognized_text.split(' '))
        recognized_list.pop(len(recognized_list) - 1)  # Remove empty string at final index in list

        accuracy_count = 0
        mis_recs = []
        for line in recognized_list:
            if line in r3_counted_dict.keys():
                if r3_counted_dict[line] > 0:
                    accuracy_count += 1
                    r3_counted_dict[line] -= 1
                else:
                    mis_recs.append(line)
            else:
                mis_recs.append(line)

        mis_recs_str = ''
        for i in mis_recs:
            mis_recs_str += i + ' '

        print(filename + ' analysis complete.')
        return accuracy_count / len(r3.split(' ')) * 100, len(mis_recs), mis_recs_str
    # Accuracy for script with reference G1
    # See comments for R1 for code explanation
    else:
        print(filename + ' is being analyzed...')

        g1_counted_dict = Counter(g1.split(' '))

        recognized_list = list(recognized_text.split(' '))
        recognized_list.pop(len(recognized_list) - 1)  # Remove empty string at final index in list

        accuracy_count = 0
        mis_recs = []
        for line in recognized_list:
            if line in g1_counted_dict.keys():
                if g1_counted_dict[line] > 0:
                    accuracy_count += 1
                    g1_counted_dict[line] -= 1
                else:
                    mis_recs.append(line)
            else:
                mis_recs.append(line)

        mis_recs_str = ''
        for i in mis_recs:
            mis_recs_str += i + ' '

        print(filename + ' analysis complete.')
        return accuracy_count / len(g1.split(' ')) * 100, len(mis_recs), mis_recs_str


def process_store_fluent() -> str:
    """
    Process all fluent files and store required data statistics results in DB.
    :return: confirmation string
    """

    # Locations for local files
    location = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Audio_Data/'
    sub_loc = ['R1/', 'R2/', 'R3/', 'G1/', 'Fluent/']

    files = {'R1/Fluent/': os.listdir(location + sub_loc[0] + sub_loc[4]),
             'R2/Fluent/': os.listdir(location + sub_loc[1] + sub_loc[4]),
             'R3/Fluent/': os.listdir(location + sub_loc[2] + sub_loc[4]),
             'G1/Fluent/': os.listdir(location + sub_loc[3] + sub_loc[4])}

    # Lists to store results
    filename = []
    ASR_script_word_count = []
    ASR_script_text = []
    ASR_accuracy_rate = []
    misrecognition_count = []
    misrecognitions = []

    # For each file, process the results
    # Recognise the audio
    # Calculate the accuracy statistics
    for key, values in files.items():
        for value in values:
            recog = recognise_audio(location + key + value)
            acc = calculate_accuracy(location + key + value, recog[0])

            filename.append(value)
            ASR_script_word_count.append(recog[1])
            ASR_script_text.append(recog[0])
            ASR_accuracy_rate.append(acc[0])
            misrecognition_count.append(acc[1])
            misrecognitions.append(acc[2])

    # Database - store results
    # Check for files already in DB
    # Store only non-duplicates
    _SQL = str.format("""SELECT filename FROM ASR_Results""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    file_list = []
    for tup in fetch:
        file_list.append(tup[0])

    for i in range(len(filename)):
        if filename[i] not in file_list:
            if filename[i][-13:-4] == 'R1!Fluent':
                _SQL = str.format(
                """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], True, False, 'R1', r1_count, r1, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            elif filename[i][-13:-4] == 'R2!Fluent':
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], True, False, 'R2', r2_count, r2, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            elif filename[i][-13:-4] == 'R3!Fluent':
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], True, False, 'R3', r3_count, r3, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            else:
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], True, False, 'G1', g1_count, g1, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()

    return 'All fluent files recognized, analyzed and stored.'


def process_store_disfluent() -> str:
    """
    Process and store results for all disfluent files
    :return: confirmation string
    """

    # Locations for local files
    location = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Audio_Data/'
    sub_loc = ['R1/', 'R2/', 'R3/', 'G1/', 'Disfluent/']

    files = {'R1/Disfluent/': os.listdir(location + sub_loc[0] + sub_loc[4]),
             'R2/Disfluent/': os.listdir(location + sub_loc[1] + sub_loc[4]),
             'R3/Disfluent/': os.listdir(location + sub_loc[2] + sub_loc[4]),
             'G1/Disfluent/': os.listdir(location + sub_loc[3] + sub_loc[4])}

    # Lists to store results
    filename = []
    ASR_script_word_count = []
    ASR_script_text = []
    ASR_accuracy_rate = []
    misrecognition_count = []
    misrecognitions = []

    # For each file, process the results
    # Recognise the audio
    # Calculate the accuracy statistics
    for key, values in files.items():
        for value in values:
            recog = recognise_audio(location + key + value)
            acc = calculate_accuracy(location + key + value, recog[0])

            filename.append(value)
            ASR_script_word_count.append(recog[1])
            ASR_script_text.append(recog[0])
            ASR_accuracy_rate.append(acc[0])
            misrecognition_count.append(acc[1])
            misrecognitions.append(acc[2])

    # Database - store results
    # Check for files already in DB
    # Store only non-duplicates
    _SQL = str.format("""SELECT filename FROM ASR_Results""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    file_list = []
    for tup in fetch:
        file_list.append(tup[0])

    for i in range(len(filename)):
        if filename[i] not in file_list:
            if filename[i][-16:-4] == 'R1!Disfluent':
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], False, True, 'R1', r1_count, r1, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            elif filename[i][-16:-4] == 'R2!Disfluent':
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], False, True, 'R2', r2_count, r2, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            elif filename[i][-16:-4] == 'R3!Disfluent':
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], False, True, 'R3', r3_count, r3, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()
            else:
                _SQL = str.format(
                    """insert into ASR_Results (filename, fluent, disfluent, script_id, script_word_count, script_text, ASR_script_word_count, ASR_script_text, ASR_accuracy_rate, misrecognition_count, misrecognitions)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename[i], False, True, 'G1', g1_count, g1, ASR_script_word_count[i], ASR_script_text[i],
                          ASR_accuracy_rate[i], misrecognition_count[i], misrecognitions[i])
                cursor.execute(_SQL, insert)
                connection.commit()

    return 'All disfluent files recognized, analyzed and stored.'
