from flask import Flask, render_template, request
import pyaudio
import wave
import numpy as np
import scipy.io
from scipy.io import wavfile
import os
import time
import matplotlib.pyplot as plt
from threading import Thread
import pygame
from Web_Application_ASR_Input_Problem_Demo.ASR_Processing import recognize_speech_problem as rsp
from Web_Application_ASR_Input_Problem_Demo.ASR_Processing import recognize_speech_prototype as rsp1


# Create instance of Flask
app = Flask(__name__)

# Store the text area content
utterances = {'P1': [], 'P2': [], 'S1': [], 'S2': [], 'S3': [], 'S4': [], 'C1': [], 'C2': []}

# Store processing times
timings = {'P1': 0, 'S1': 0, 'S2': 0, 'S3': [], 'S4': [], 'C1': 0, 'C2': 0}

# Control and store the audio recording
record = [False]
frames = []

# ASR Pause Threshold
pause_threshold = [0]


# Problem Page
# -------------

@app.route('/')
def home():
    """
    Problem page renderer.
    :return: Problem page template
    """
    return render_template('Problem.html')


@app.route('/ASR_problem1/', methods=['POST', 'GET'])
def problem_asr1():
    """
    Text area 1 controller.
    Utilises ASR with variable pause threshold
    :return: relevant rendered template
    """
    start = time.time()

    if request.form['ta1'] == 'pt_2':
        pause_threshold[0] = 2
        return render_template('Problem.html', utterance1=display_string(1), time1=timings['P1'],
                               pause_threshold1='Pause threshold = ' + str(pause_threshold[0]), asr1='')
    elif request.form['ta1'] == 'pt_4':
        pause_threshold[0] = 4
        return render_template('Problem.html', utterance1=display_string(1), time1=timings['P1'],
                               pause_threshold1='Pause threshold = ' + str(pause_threshold[0]), asr1='')
    elif request.form['ta1'] == 'pt_6':
        pause_threshold[0] = 6
        return render_template('Problem.html', utterance1=display_string(1), time1=timings['P1'],
                               pause_threshold1='Pause threshold = ' + str(pause_threshold[0]), asr1='')
    elif request.form['ta1'] == 'asr_button1':
        try:
            utterance = 'You said: ' + rsp(pause_threshold[0])
            store_utterance(1, utterance)
            elapsed_time = round(time.time() - start, 2)
            timings['P1'] = str(elapsed_time) + ' seconds'
        except AssertionError:
            # Assertion error thrown if 'ASR' button pressed again before ASR method has finished
            pass
        return render_template('Problem.html', utterance1=display_string(1), time1=timings['P1'],
                               pause_threshold1='Pause threshold = ' + str(pause_threshold[0]), asr1='')
    elif request.form['ta1'] == 'clear_button1':
        clear_text_area(1)
        return render_template('Problem.html', utterance1=display_string(1), time1=timings['P1'],
                               pause_threshold1='', asr1='')


# Prototype 1
# -----------

@app.route('/prototype_page1/')
def prototype_page1():
    """
    Prototype page 1 renderer.
    :return: Prototype page 1 template
    """
    return render_template('Prototype1.html')


@app.route('/ASR_prototype1/', methods=['POST', 'GET'])
def prototype_asr1():
    """
    Text area 2 controller.
    Utilises ASR with variable pause threshold
    :return: relevant rendered template
    """
    start = time.time()

    if request.form['ta2'] == 'pt_5':
        pause_threshold[0] = 5
        return render_template('Prototype1.html', utterance2=display_string(2),
                               pause_threshold2='Pause threshold = ' + str(pause_threshold[0]))
    elif request.form['ta2'] == 'pt_10':
        pause_threshold[0] = 10
        return render_template('Prototype1.html', utterance2=display_string(2),
                               pause_threshold2='Pause threshold = ' + str(pause_threshold[0]))
    elif request.form['ta2'] == 'pt_15':
        pause_threshold[0] = 15
        return render_template('Prototype1.html', utterance2=display_string(2),
                               pause_threshold2='Pause threshold = ' + str(pause_threshold[0]))
    elif request.form['ta2'] == 'pt_20':
        pause_threshold[0] = 20
        return render_template('Prototype1.html', utterance2=display_string(2),
                               pause_threshold2='Pause threshold = ' + str(pause_threshold[0]))
    elif request.form['ta2'] == 'start_button1':
        utterance = 'You said: ' + rsp(pause_threshold[0])
        store_utterance(2, utterance)
        utterance2 = display_string(2)
        elapsed_time = round(time.time() - start, 2)
        timings['P2'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype1.html', utterance2=utterance2,
                               time2=timings['P2'], pause_threshold2='Pause threshold set to ' + str(pause_threshold[0]))
    elif request.form['ta2'] == 'clear_button1':
        clear_text_area(2)
        return render_template('Prototype1.html', utterance2=display_string(2), time2='', pause_threshold='')


# Prototype 2
# ----------------

@app.route('/prototype_page2/')
def prototype_page2():
    """
    Prototype page 2 renderer.
    :return: Prototype page 2 template
    """
    return render_template('Prototype2.html')


@app.route('/ASR_prototype2/', methods=['POST', 'GET'])
def prototype_asr2():
    """
    Text area 3 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    :return: relevant rendered template
    """
    if request.form['ta3'] == 'start/stop_button2':
        if not record[0]:

            timings['S2'] = time.time()

            record[0] = True

            # Create an instance of PyAudio
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

            i = int(44100 / 1024 * 300)         # Arbitrary duration set at 300 seconds
            while i > 0:
                data = stream.read(1024)
                frames.append(data)
                i -= 1
                if not record[0]:
                    break

            stream.stop_stream()
            stream.close()
            p.terminate()

            elapsed_time = round(time.time() - timings['S2'], 2)
            timings['S2'] = str(elapsed_time) + ' seconds'

            return render_template('Prototype2.html', utterance3=display_string(3))
        else:
            stop_recording_asr2()
            return render_template('Prototype2.html', utterance3=display_string(3))
    elif request.form['ta3'] == 'clear_button2':
        clear_text_area(3)
        return render_template('Prototype2.html', utterance3=display_string(3))
    elif request.form['ta3'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype2.html', utterance3=display_string(3),
                               audio3='Playing file 1...')
    elif request.form['ta3'] == 'play_button2':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype2.html', utterance3=display_string(3),
                               audio3='Playing file 2...')
    elif request.form['ta3'] == 'asr_button1':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(3, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['S2'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype2.html', utterance3=display_string(3), asr3='Recognised file 1')
    elif request.form['ta3'] == 'asr_button2':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(3, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['P1'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype2.html', utterance3=display_string(3), asr3='Recognised file 2')


# Prototype 3
# ----------------

@app.route('/prototype_page3/')
def prototype_page3():
    """
    Prototype page 3 renderer.
    :return: Prototype page 3 template
    """
    return render_template('Prototype3.html')


@app.route('/ASR_prototype3/', methods=['POST', 'GET'])
def prototype_asr3():
    """
    Text area 4 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    Allows user to pause the recording
    :return: relevant rendered template
    """
    if request.form['ta4'] == 'start/stop_button2':
        if not record[0]:

            timings['S3'] = []
            timings['S3'].append(time.time())

            record[0] = True

            # Create an instance of PyAudio
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

            i = int(44100 / 1024 * 300)  # Arbitrary duration set at 300 seconds
            while i > 0:
                data = stream.read(1024)
                frames.append(data)
                i -= 1
                if not record[0]:
                    break

            stream.stop_stream()
            stream.close()
            p.terminate()

            # elapsed_time = round(time.time() - timings['S3'], 2)
            # timings['S3'] = str(elapsed_time) + ' seconds'

            return render_template('Prototype3.html', utterance4=display_string(4))
        else:
            stop_recording_asr3(3)
            return render_template('Prototype3.html', utterance4=display_string(4))
    elif request.form['ta4'] == 'pause/restart_button2':
        if record[0]:
            timings['S3'].append(time.time())
            record[0] = False
            return render_template('Prototype3.html', utterance4=display_string(4))
        else:
            timings['S3'].append(time.time())
            record[0] = True
            # Create an instance of PyAudio
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

            i = int(44100 / 1024 * 300)  # Arbitrary duration set at 300 seconds
            while i > 0:
                data = stream.read(1024)
                frames.append(data)
                i -= 1
                if not record[0]:
                    break

            stream.stop_stream()
            stream.close()
            p.terminate()
            return render_template('Prototype3.html', utterance4=display_string(4))
    elif request.form['ta4'] == 'clear_button2':
        clear_text_area(4)
        return render_template('Prototype3.html', utterance4=display_string(4))
    elif request.form['ta4'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype3.html',
                               audio4='Playing file 1...')
    elif request.form['ta4'] == 'play_button2':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype3.html',
                               audio4='Playing file 2...')
    elif request.form['ta4'] == 'asr_button1':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(4, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['S2'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype3.html', utterance4=display_string(4), asr4='Recognised file 1')
    elif request.form['ta4'] == 'asr_button2':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(4, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['P1'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype3.html', utterance4=display_string(4), asr4='Recognised file 2')


# Prototype 4
# -----------

@app.route('/prototype_page4/')
def prototype_page4():
    """
    Prototype page 4 renderer.
    :return: Prototype page 4 template
    """
    return render_template('Prototype4.html')


@app.route('/ASR_prototype4/', methods=['POST', 'GET'])
def prototype_asr4():
    """
    Text area 5 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    Allows using to pause and/or reset the recording
    :return: relevant rendered template
    """
    if request.form['ta5'] == 'start/stop_button3':
        if not record[0]:

            timings['S4'] = []
            timings['S4'].append(time.time())

            record[0] = True

            # Create an instance of PyAudio
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

            i = int(44100 / 1024 * 300)  # Arbitrary duration set at 300 seconds
            while i > 0:
                data = stream.read(1024)
                frames.append(data)
                i -= 1
                if not record[0]:
                    break

            stream.stop_stream()
            stream.close()
            p.terminate()

            # elapsed_time = round(time.time() - timings['S3'], 2)
            # timings['S3'] = str(elapsed_time) + ' seconds'

            return render_template('Prototype4.html', utterance5=display_string(5))
        else:
            stop_recording_asr3(4)
            return render_template('Prototype4.html', utterance5=display_string(5))
    elif request.form['ta5'] == 'pause/restart_button3':
        if record[0]:
            timings['S4'].append(time.time())
            record[0] = False
            return render_template('Prototype4.html', utterance5=display_string(5))
        else:
            timings['S4'].append(time.time())
            record[0] = True
            # Create an instance of PyAudio
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

            i = int(44100 / 1024 * 300)  # Arbitrary duration set at 300 seconds
            while i > 0:
                data = stream.read(1024)
                frames.append(data)
                i -= 1
                if not record[0]:
                    break

            stream.stop_stream()
            stream.close()
            p.terminate()
            return render_template('Prototype4.html', utterance5=display_string(5))
    elif request.form['ta5'] == 'reset_button3':
        record[0] = False
        frames.clear()
        return render_template('Prototype4.html', utterance5=display_string(5))
    elif request.form['ta5'] == 'clear_button3':
        clear_text_area(5)
        return render_template('Prototype4.html', utterance5=display_string(5))
    elif request.form['ta5'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype4.html', utterance5=display_string(5),
                               audio5='Playing file 1...')
    elif request.form['ta5'] == 'play_button2':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Prototype4.html', utterance5=display_string(5),
                               audio5='Playing file 2...')
    elif request.form['ta5'] == 'asr_button1':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(5, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['S2'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype4.html', utterance5=display_string(5), asr5='Recognised file 1')
    elif request.form['ta5'] == 'asr_button2':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(5, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['P1'] = str(elapsed_time) + ' seconds'
        return render_template('Prototype4.html', utterance5=display_string(5), asr5='Recognised file 2')


# Results Page
# -------------

@app.route('/results/', methods=['POST', 'GET'])
def results_page():
    """

    :return: relevant rendered template
    """
    return render_template('Prototype_Results.html')


# Misc Functions
# ---------------

def stop_recording_asr2():
    """
    Helper method for prototype_asr2()
    Stops the recording, creates the .wav file, processes file through ASR
    :return: the relevant rendered template
    """
    record[0] = False

    wf = wave.open('Test.wav', 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    utterance = 'You said: ' + rsp1('Test.wav')
    store_utterance(3, utterance)

    utterance3 = display_string(3)

    frames.clear()
    os.remove('Test.wav')

    return render_template('Prototype2.html', utterance3=utterance3)


def play_audio(file: str) -> None:
    """
    Prototype_asr2()/asr3() helper method.
    Plays an audio file.
    :return: None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue


def stop_recording_asr3(prototype_number: int) -> None:
    """
    Helper method for solution_asr3()
    :return: None
    """
    if prototype_number == 3:
        record[0] = False
    
        wf = wave.open('Test.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()
    
        utterance = 'You said: ' + rsp1('Test.wav')
        store_utterance(4, utterance)
    
        frames.clear()
        os.remove('Test.wav')
    
        z = [x for x in timings['S3']]
        timer = 0.0
        for i in range(0, len(z)-1, 2):
            timer += z[i+1] - z[i]
    
        elapsed_time = round(timer, 2)
        timings['S3'].clear()
        timings['S3'].append(str(elapsed_time) + ' seconds')
    
        return None
    else:
        record[0] = False

        wf = wave.open('Test.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        utterance = 'You said: ' + rsp1('Test.wav')
        store_utterance(5, utterance)

        frames.clear()
        os.remove('Test.wav')

        z = [x for x in timings['S4']]
        timer = 0.0
        for i in range(0, len(z) - 1, 2):
            timer += z[i + 1] - z[i]

        elapsed_time = round(timer, 2)
        timings['S4'].clear()
        timings['S4'].append(str(elapsed_time) + ' seconds')

        return None


def remove_silence_audio() -> None:
    """
    Helper method for telephone_asr1()
    :return:
    """
    # Read the wav file and get rate and list of data
    rate, data = scipy.io.wavfile.read('Test.wav')

    # Create list for data of amended wav file
    data2 = []

    # Loop through data of original file and add data that doesn't meed condition: values >= -10 and <= 10
    for i in range(len(data)):
        if data[i][0] >= -10 and data[i][0] <= 10:
            pass
        else:
            data2.append(data[i])

    # Create NumPy array from revised data
    data2 = np.asarray(data2, dtype=np.int16)

    # Write new data to wav file
    scipy.io.wavfile.write('Test.wav', rate, data2)

    return None


def store_utterance(text_area_no: int, utterance: str) -> None:
    """
    Store each ASR recognition in the relevant list.
    :param text_area_no: the text area id
    :param utterance: the utterance
    :return: None
    """
    if text_area_no == 1:
        utterances['P1'].append(utterance)
    elif text_area_no == 2:
        utterances['S1'].append(utterance)
    elif text_area_no == 3:
        utterances['S2'].append(utterance)
    elif text_area_no == 4:
        utterances['S3'].append(utterance)
    elif text_area_no == 5:
        utterances['S4'].append(utterance)
    elif text_area_no == 6:
        utterances['S4'].append(utterance)
    elif text_area_no == 7:
        utterances['C1'].append(utterance)
    elif text_area_no == 8:
        utterances['C2'].append(utterance)
    return None


def display_string(text_area_no: int) -> str:
    """
    Format the text to display in the text area.
    :param text_area_no: the text area id
    :return: the formatted text to be displayed
    """
    if text_area_no == 1:
        text = ''
        for v in utterances['P1']:
            text += v + '\n'
        return text
    elif text_area_no == 2:
        text = ''
        for v in utterances['S1']:
            text += v + '\n'
        return text
    elif text_area_no == 3:
        text = ''
        for v in utterances['S2']:
            text += v + '\n'
        return text
    elif text_area_no == 4:
        text = ''
        for v in utterances['S3']:
            text += v + '\n'
        return text
    elif text_area_no == 5:
        text = ''
        for v in utterances['S4']:
            text += v + '\n'
        return text
    elif text_area_no == 6:
        text = ''
        for v in utterances['S4']:
            text += v + '\n'
        return text
    elif text_area_no == 7:
        text = ''
        for v in utterances['C1']:
            text += v + '\n'
        return text
    elif text_area_no == 8:
        text = ''
        for v in utterances['C2']:
            text += v + '\n'
        return text


def clear_text_area(text_area_no: int) -> None:
    """
    Clear the selected text area of content
    :param text_area_no: the text area id
    :return: None
    """
    if text_area_no == 1:
        utterances['P1'].clear()
        timings['P1'] = 0
    elif text_area_no == 2:
        utterances['S1'].clear()
        timings['S1'] = 0
    elif text_area_no == 3:
        utterances['S2'].clear()
        timings['S2'] = 0
    elif text_area_no == 4:
        utterances['S3'].clear()
        timings['S3'] = 0
    elif text_area_no == 5:
        utterances['S4'].clear()
        timings['S4'] = 0
    elif text_area_no == 6:
        utterances['S4'].clear()
        timings['S4'] = 0
    elif text_area_no == 7:
        utterances['C1'].clear()
        timings['C1'] = 0
    elif text_area_no == 8:
        utterances['C2'].clear()
        timings['C2'] = 0
    return None


# Launch Function
# ---------------


def run():
    """
    Run the web app.
    :return: None
    """
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    run()
