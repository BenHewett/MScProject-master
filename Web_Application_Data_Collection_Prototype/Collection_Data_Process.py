from Web_Application_Data_Collection_Prototype import Connect_INI
from Web_Application_Data_Collection_Prototype.File_name_generator import file_name_generator
import pyaudio


def process_data(fluency_type):
    """
    Processes the data and stores in the database.
    :param fluency_type: the fluency type ('fluent', 'disfluent') of the audio
    :return: None
    """

    # Determine boolean value for fluency type
    fluent = False
    disfluent = False

    if fluency_type == 'fluent':
        fluent = True
    else:
        disfluent = True

    # Process audio recording
    # Get a unique filename of length 10 characters for audio file
    file_name = file_name_generator(10)

    # Create a PyAudio object
    py = pyaudio.PyAudio()

    # Initialise list for the wav file frames
    frames = []

    # Set the parameters of the wav file to be recorded
    chunk = 1024
    formatting = pyaudio.paInt16
    channels = 2
    frame_rate = 44100
    duration = 10
    print('Parameters initialised')

    # Open a new stream using the defined parameters
    stream = py.open(format=formatting, channels=channels, rate=frame_rate, input=True, frames_per_buffer=chunk)
    print('Recording audio')

    # Add chunks of the stream data to the list
    for i in range(0, int(frame_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Terminate the stream/recording
    stream.stop_stream()
    stream.close()
    py.terminate()
    print('Recording terminated, data acquired')

    frame_string = b''.join(frames)
    print(type(frame_string))

    # Get a data_processing connection object and initialise a cursor object
    db_con = Connect_INI.connect()
    db_cursor = db_con.cursor()

    _SQL = str.format(
        """INSERT INTO Audio_Data_Raw(file_name, fluent, disfluent, frame_rate, channels, sample_width, data) VALUES(%s, %s, %s, %s, %s, %s, %s)""")
    to_insert = (file_name, fluent, disfluent, frame_rate, channels, py.get_sample_size(formatting), frame_string)
    db_cursor.execute(_SQL, to_insert)
    db_con.commit()
    print('Data stored')
    db_cursor.close()
    db_con.close()
    print('Connection closed')