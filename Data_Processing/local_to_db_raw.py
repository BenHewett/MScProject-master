import os
from mysql import connector
import wave
import scipy.io.wavfile

location = '/Users/benjaminhewett/Desktop/MScProject/Audio_Data/Audio_Data_Raw/App_Data/'


def get_filenames_db() -> list:
    """
    Get a list of filenames currently in the DB
    :return: a list of all filenames in the DB
    """
    print('Getting filenames in DB...')
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT file_name FROM Audio_Data_Raw""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()
    # print('Fetch:', fetch)

    file_names_in_db = []

    for file in fetch:
        # print(file)
        for file1 in file:
            # print(file1)
            file_names_in_db.append(file1)
    # print(file_names)

    print('Filenames acquired.')
    return file_names_in_db


def to_db(file_names_in_db):
    """
    Upload all unique files from local drive to DB
    :param file_names_in_db: list of filenames currently stored in the DB
    :return: None
    """
    print('Connecting to DB...')
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()
    print('Connected to DB.')

    print('Collating files...')
    # Get list of files in target directory
    # Iterate through list and get all .wav files only
    files = os.listdir(location)
    wav_files = []
    for name in files:
        if name.endswith('.wav'):
            wav_files.append(name)
        else:
            pass

    print('Uploading files...')
    # Cross references file names in DB with file names in target directory
    # Only adds non-duplicates to DB
    for filename in wav_files:
        if filename not in file_names_in_db:
            if filename[-10:] == 'Fluent.wav':
                w = wave.open(location + filename)
                rate, data = scipy.io.wavfile.read(location + filename)
                frame_string = b''.join(data)
                script = filename[-13:-11]
                _SQL = str.format(
                    """insert into Audio_Data_Raw (file_name, script, fluent, disfluent, frame_rate, channels, sample_width, data) values (%s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename, script, True, False, w.getframerate(), w.getnchannels(), w.getsampwidth(), frame_string)
                cursor.execute(_SQL, insert)
                connection.commit()
            else:
                w = wave.open(location + filename)
                rate, data = scipy.io.wavfile.read(location + filename)
                frame_string = b''.join(data)
                script = filename[-16:-14]
                _SQL = str.format(
                    """insert into Audio_Data_Raw (file_name, script, fluent, disfluent, frame_rate, channels, sample_width, data) values (%s, %s, %s, %s, %s, %s, %s, %s)""")
                insert = (filename, script, False, True, w.getframerate(), w.getnchannels(), w.getsampwidth(), frame_string)
                cursor.execute(_SQL, insert)
                connection.commit()

    print('Upload Complete')

