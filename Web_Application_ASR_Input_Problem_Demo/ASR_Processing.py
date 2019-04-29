import speech_recognition as sr

# Display the problem with the the average timeout time for consumer-grade ASR systems.
# Average timeout is between 5 - 7 seconds.
# Systems tested: Siri, Google Chrome

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def recognize_speech_problem(pause_threshold: int) -> str:
    """
    Function to enable sound to be taken by the microphone and to be sent to the ASR for recognition.
    Result is printed to the console.
    :return: None
    """
    # print(pause_threshold)
    # recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    # Values below this threshold are considered silence, and values above this threshold are considered speech.
    # recognizer.energy_threshold = 4000
    recognizer.pause_threshold = pause_threshold

    # microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, 1)
        # print('[' + str(timeout) + ' second timeout]: Say something...')
        try:
            audio = recognizer.listen(source, timeout=pause_threshold, phrase_time_limit=None)
            text = recognizer.recognize_google(audio)
            # print('You said: ' + recognizer.recognize_google(audio))
            return text
        except sr.WaitTimeoutError:
            return 'Sorry, timed out.'
            # print('Sorry, timed out.')
        except sr.UnknownValueError:
            return 'Unable to understand what you said.'
            # print('Unable to understand what you said.')
        except sr.RequestError:
            return 'ASR API connection error.'
            # print('ASR API connection error.')


def recognize_speech_prototype(file: str) -> str:
    """
    Function to enable sound to be taken by the microphone and to be sent to the ASR for recognition.
    Result is printed to the console.
    :param file: file to be recognised
    :return: recognized text string
    """

    # Store the audio data
    audio = sr.AudioFile(file)

    recognized_text = ''

    with audio as source:
        audio = recognizer.record(source)
        try:
            recognized_text += recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            recognized_text = ''
        except sr.RequestError:
            recognized_text = ''

    return recognized_text
