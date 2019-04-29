from flask import Flask, render_template, request
import wave
import os
import pygame
from threading import Thread
import pyaudio
import time
from collections import Counter
from Web_Application_ASR_Input_Problem_Demo.ASR_Processing import recognize_speech_prototype as rsp1
from Web_Application_ASR_Output_Problem_Demo.Probability_next_word import *
from Web_Application_ASR_Output_Problem_Demo.Audio_editing import determine_duration, remove_silence


# Create instance of Flask
app = Flask(__name__)

# Store the text area content
utterances = {'O1': [], 'O2': [], 'O3': []}

# Store processing times
timings = {'O2_record': [], 'O2_asr': [], 'O2_edited': []}

# Audio recording controller + data storage
record = [False]
frames = []


# Output 1 Page
# -------------

@app.route('/')
def output_1():
    """
    Output 1 page renderer.
    :return: Output page 1 template
    """
    return render_template('Output1.html')


@app.route('/ASR_output1/', methods=['POST', 'GET'])
def output_asr1():
    """
    Text area 1 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    Allows user to pause the recording
    :return: relevant rendered template
    """
    if request.form['ta1'] == 'start/stop_button1':
        if not record[0]:

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

            return render_template('Output1.html', utterance1=display_string(1))
        else:
            stop_recording(1)
            return render_template('Output1.html', utterance1=display_string(1))
    elif request.form['ta1'] == 'pause/restart_button1':
        if record[0]:
            # timings['S3'].append(time.time())
            record[0] = False
            return render_template('Output1.html', utterance1=display_string(1))
        else:
            # timings['S3'].append(time.time())
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
            return render_template('Output1.html', utterance1=display_string(1))
    elif request.form['ta1'] == 'clear_button1':
        clear_text_area(1)
        return render_template('Output1.html', utterance1=display_string(1))
    elif request.form['ta1'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Output1.html',
                               audio1='Playing file 1...')
    elif request.form['ta1'] == 'play_button2':
        th = Thread(target=play_audio, args=('Test2.wav',))
        th.start()
        return render_template('Output1.html',
                               audio1='Playing file 2...')
    elif request.form['ta1'] == 'asr_button1':
        utterance = 'You said: ' + rsp1('Test1.wav')
        store_utterance(1, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['S2'] = str(elapsed_time) + ' seconds'
        return render_template('Output1.html', utterance1=display_string(1), asr1='Recognised file 1')
    elif request.form['ta1'] == 'asr_button2':
        utterance = 'You said: ' + rsp1('Test2.wav')
        store_utterance(1, utterance)
        # elapsed_time = round(time.time() - start, 2)
        # timings['P1'] = str(elapsed_time) + ' seconds'
        return render_template('Output1.html', utterance1=display_string(1), asr1='Recognised file 2')


# Helper methods for output_asr1()
# --------------------------------

def play_audio(file: str):
    """
    Output_asr1() helper method.
    :return: None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    return None


def stop_recording(text_area_no: int):
    """
    Function to stop the audio recording and to recognise the audio
    :return: None
    """
    if text_area_no == 1:
        record[0] = False

        wf = wave.open('Test.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        utterance = 'You said: ' + rsp1('Test.wav')
        store_utterance(text_area_no, utterance)

        frames.clear()
        os.remove('Test.wav')
    elif text_area_no == 2:
        record[0] = False

        wf = wave.open('Test.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        timings['O2_record'].append(time.time())

        timings['O2_asr'].append(time.time())
        utterance = 'Original: ' + rsp1('Test.wav')
        timings['O2_asr'].append(time.time())
        asr_timing = timings['O2_asr'][1] - timings['O2_asr'][0]
        timings['O2_asr'].clear()
        timings['O2_asr'].append(round(asr_timing, 2))
        store_utterance(text_area_no, utterance)

        z = [x for x in timings['O2_record']]
        timer = 0.0
        for i in range(0, len(z) - 1, 2):
            timer += z[i + 1] - z[i]

        elapsed_time = round(timer, 2)
        timings['O2_record'].clear()
        timings['O2_record'].append(elapsed_time)

        remove_silence('Test.wav', 'Test.wav')
        timings['O2_edited'].append(determine_duration('Test.wav'))
        timings['O2_asr'].append(time.time())
        utterance = 'Edited: ' + rsp1('Test.wav')
        timings['O2_asr'].append(time.time())
        asr_timing = timings['O2_asr'][2] - timings['O2_asr'][1]
        # timings['O2_asr'].clear()
        timings['O2_asr'].append(round(asr_timing, 2))
        store_utterance(text_area_no, utterance)

        frames.clear()
        os.remove('Test.wav')
    else:
        record[0] = False

        wf = wave.open('Test.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        timings['O2_record'].append(time.time())

        timings['O2_asr'].append(time.time())
        utterance = 'Original: ' + rsp1('Test.wav')
        timings['O2_asr'].append(time.time())
        asr_timing = timings['O2_asr'][1] - timings['O2_asr'][0]
        timings['O2_asr'].clear()
        timings['O2_asr'].append(round(asr_timing, 2))
        store_utterance(text_area_no, utterance)

        z = [x for x in timings['O2_record']]
        timer = 0.0
        for i in range(0, len(z) - 1, 2):
            timer += z[i + 1] - z[i]

        elapsed_time = round(timer, 2)
        timings['O2_record'].clear()
        timings['O2_record'].append(elapsed_time)

        remove_silence('Test.wav', 'Test.wav')
        timings['O2_edited'].append(determine_duration('Test.wav'))
        timings['O2_asr'].append(time.time())
        utterance = 'Edited: ' + rsp1('Test.wav')
        timings['O2_asr'].append(time.time())
        asr_timing = timings['O2_asr'][2] - timings['O2_asr'][1]
        # timings['O2_asr'].clear()
        timings['O2_asr'].append(round(asr_timing, 2))
        store_utterance(text_area_no, utterance)

        frames.clear()
        os.remove('Test.wav')

    return None


# Output 2 Page
# -------------


@app.route('/output2/')
def output_2():
    """
    Output 2 page renderer.
    :return: Relevant rendered page template
    """
    return render_template('Output2.html')


@app.route('/ASR_output2/', methods=['POST', 'GET'])
def output_asr2():
    """
    Text area 2 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    Allows user to pause the recording
    :return: relevant rendered template
    """
    if request.form['ta2'] == 'start/stop_button1':
        if not record[0]:

            record[0] = True

            timings['O2_record'].append(time.time())

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

            return render_template('Output2.html', utterance2=display_string(2))
        else:
            stop_recording(2)
            return render_template('Output2.html', utterance2=display_string(2),
                                   processing3='Original Recording: ' + str(timings['O2_record'][0]),
                                   processing4='Recognized in: ' + str(timings['O2_asr'][0]),
                                   processing5='Total Original: ' + str(timings['O2_record'][0] + timings['O2_asr'][0]),
                                   processing6='Edited Recording: ' + str(timings['O2_edited'][0]),
                                   processing7='Recognized in: ' + str(timings['O2_asr'][3]),
                                   processing8='Total Edited: ' + str(timings['O2_edited'][0] + timings['O2_asr'][3]))
    elif request.form['ta2'] == 'pause/restart_button1':
        if record[0]:
            timings['O2_record'].append(time.time())
            record[0] = False
            return render_template('Output2.html', utterance2=display_string(2))
        else:
            timings['O2_record'].append(time.time())
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
            return render_template('Output2.html', utterance2=display_string(2))
    elif request.form['ta2'] == 'clear_button1':
        clear_text_area(2)
        return render_template('Output2.html', utterance2=display_string(2))
    elif request.form['ta2'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test1.wav',))
        th.start()
        return render_template('Output2.html',
                               audio2='Playing file 1...', duration2=str(determine_duration('Test1.wav')))
    elif request.form['ta2'] == 'play_button2':
        remove_silence('Test1.wav', 'Test2.wav')
        th = Thread(target=play_audio, args=('Test2.wav',))
        th.start()
        return render_template('Output2.html',
                               audio2='Playing file 2...', duration2=str(determine_duration('Test2.wav')))
    elif request.form['ta2'] == 'asr_button1':
        start = time.time()
        utterance = 'You said: ' + rsp1('Test1.wav')
        finish = time.time()
        elapsed_time = round(finish - start, 2)
        store_utterance(2, utterance)
        return render_template('Output2.html', utterance2=display_string(2), asr2='Recognised file 1',
                               processing2=elapsed_time, audio2='File 1', duration2=str(determine_duration('Test1.wav')))
    elif request.form['ta2'] == 'asr_button2':
        start = time.time()
        utterance = 'You said: ' + rsp1('Test2.wav')
        finish = time.time()
        elapsed_time = round(finish - start, 2)
        store_utterance(2, utterance)
        return render_template('Output2.html', utterance2=display_string(2), asr2='Recognised file 2',
                               processing2=elapsed_time, audio2='File 2', duration2=str(determine_duration('Test2.wav')))


# Output 3 Page
# -------------


@app.route('/output3/')
def output_3():
    """
    Output 3 page renderer.
    :return: Relevant rendered page template
    """
    return render_template('Output3.html')


@app.route('/ASR_output3/', methods=['POST', 'GET'])
def output_asr3():
    """
    Text area 3 controller.
    Records audio, waits for user to manually stop recording, and then processes through ASR
    Allows user to pause the recording
    :return: relevant rendered template
    """
    if request.form['ta3'] == 'start/stop_button1':
        if not record[0]:

            record[0] = True

            timings['O2_record'].append(time.time())

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

            return render_template('Output3.html', utterance3=display_string(3))
        else:
            stop_recording(3)
            return render_template('Output3.html', utterance3=display_string(3))
    elif request.form['ta3'] == 'pause/restart_button1':
        if record[0]:
            timings['O2_record'].append(time.time())
            record[0] = False
            return render_template('Output3.html', utterance3=display_string(3))
        else:
            timings['O2_record'].append(time.time())
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
            return render_template('Output3.html', utterance3=display_string(3))
    elif request.form['ta3'] == 'clear_button1':
        clear_text_area(3)
        return render_template('Output3.html', utterance3=display_string(3))
    elif request.form['ta3'] == 'play_button1':
        th = Thread(target=play_audio, args=('Test5.wav',))
        th.start()
        return render_template('Output3.html',
                               audio3='Playing file 1...', duration3=str(determine_duration('Test5.wav')))
    elif request.form['ta3'] == 'play_button2':
        remove_silence('Test1.wav', 'Test6.wav')
        th = Thread(target=play_audio, args=('Test6.wav',))
        th.start()
        return render_template('Output3.html',
                               audio3='Playing file 2...', duration3=str(determine_duration('Test6.wav')))
    elif request.form['ta3'] == 'asr_button1':
        start = time.time()
        utterance = rsp1('Test5.wav')
        mis_recs = calculate_accuracy(utterance)
        amended_utterance = get_best_candidates(mis_recs, utterance)
        utterance = 'You said: ' + utterance
        finish = time.time()
        elapsed_time = round(finish - start, 2)
        store_utterance(3, utterance)
        return render_template('Output3.html', utterance3=display_string(3), asr3='Recognised file 1',
                               processing3=elapsed_time, audio3='File 1', duration3=str(determine_duration('Test5.wav')),
                               misrecs3=mis_recs, amended1=amended_utterance)
    elif request.form['ta3'] == 'asr_button2':
        start = time.time()
        utterance = 'You said: ' + rsp1('Test2.wav')
        finish = time.time()
        elapsed_time = round(finish - start, 2)
        store_utterance(3, utterance)
        return render_template('Output3.html', utterance3=display_string(3), asr3='Recognised file 2',
                               processing2=elapsed_time, audio3='File 2', duration3=str(determine_duration('Test2.wav')))


def calculate_accuracy(recognized_text: str) -> str:
    """
    Calculates the accuracy of the ASR text compared to the original script
    :param recognized_text: string of recognized text
    :return: tuple containing the number of words accurately recognized by ASR, accuracy as a percentage, any
    mis-recognitions
    """
    phrase1 = 'When the sunlight strikes raindrops in the air they act as a prism and form a rainbow'.lower()

    r1_counted_dict = Counter(phrase1.split(' '))

    recognized_list = list(recognized_text.split(' '))
    recognized_list.pop(len(recognized_list) - 1)  # Remove empty string at final index in list

    accuracy_count = 0
    mis_recs = []
    for line in recognized_list:
        if line in r1_counted_dict.keys():
            if r1_counted_dict[line] > 0:
                accuracy_count += 1
                r1_counted_dict[line] -= 1
            else:
                mis_recs.append(line)
        else:
            mis_recs.append(line)

    mis_recs_str = ''
    for i in mis_recs:
        mis_recs_str += i + ' '

    return mis_recs_str


# Helper methods for output_asr3()
# --------------------------------

def get_best_candidates(misrecs: str, text: str):

    misrecs = misrecs[:-1]

    text = text.split(' ')
    print(text)

    phrase1 = 'When the sunlight strikes raindrops in the air they act as a prism and form a rainbow'.lower()
    phrase_list = phrase1.split(' ')
    print(phrase_list)

    mis_recs_split = misrecs.split(' ')
    print(mis_recs_split)

    misrec_indexes = []
    for i in range(len(phrase_list)):
        if phrase_list[i] == text[i]:
            pass
        else:
            misrec_indexes.append(i)

    print(misrec_indexes)

    bi_sub = form_bigrams_subsequent(corpus=corpus_r1 + corpus_r2 + corpus_r3 + corpus_g1)

    probs_sub = calculate_probabilities(bigrams=bi_sub)

    bi_prev = form_bigrams_previous(corpus=corpus_r1 + corpus_r2 + corpus_r3 + corpus_g1)

    probs_prev = calculate_probabilities(bigrams=bi_prev)

    best_cands = []
    for el in misrec_indexes:
        print(el)
        print(phrase_list[el-1])
        print(phrase_list[el+1])
        best = best_candidate(probs_prev, probs_sub, phrase_list[el-1], phrase_list[el+1])
        best_cands.append(best)
        text[el] = best
    print(best_cands)
    print(' '.join(text))

    return ' '.join(text)


# Misc Functions
# ---------------


def clear_text_area(text_area_no):
    """
    Clear the selected text area of content
    :param text_area_no: the text area id
    :return: None
    """
    if text_area_no == 1:
        utterances['O1'].clear()
    elif text_area_no == 2:
        utterances['O2'].clear()
        timings['O2_record'].clear()
        timings['O2_asr'].clear()
        timings['O2_edited'].clear()
    elif text_area_no == 3:
        utterances['O3'].clear()
        timings['O2_record'].clear()
        timings['O2_asr'].clear()
        timings['O2_edited'].clear()
    return None


def store_utterance(text_area_no, utterance):
    """
    Store each ASR recognition in the relevant list.
    :param text_area_no: the text area id
    :param utterance: the utterance
    :return: None
    """
    if text_area_no == 1:
        utterances['O1'].append(utterance)
    elif text_area_no == 2:
        utterances['O2'].append(utterance)
    elif text_area_no == 3:
        utterances['O3'].append(utterance)
    return None


def display_string(text_area_no):
    """
    Format the text to display in the text area.
    :param text_area_no: the text area id
    :return: the formatted text to be displayed
    """
    if text_area_no == 1:
        text = ''
        for v in utterances['O1']:
            text += v + '\n'
        return text
    elif text_area_no == 2:
        text = ''
        for v in utterances['O2']:
            text += v + '\n'
        return text
    elif text_area_no == 3:
        text = ''
        for v in utterances['O3']:
            text += v + '\n'
        return text


def run():
    """
    Run the web app.
    :return: None
    """
    app.run(debug=True, port=5004)