'''import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "probe1.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = speechsdk.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
#try:
#    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
#except sr.UnknownValueError:
#    print("Sphinx could not understand audio")
#except sr.RequestError as e:
#    print("Sphinx error; {0}".format(e))

# recognize speech using Microsoft Azure Speech
AZURE_SPEECH_KEY = "f0138dd2633b444683b3ec23b3e501aa"  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Azure Speech thinks you said " + r.recognize_azure(audio, key=AZURE_SPEECH_KEY))
except sr.UnknownValueError:
    print("Microsoft Azure Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Azure Speech service; {0}".format(e))

# recognize speech using Microsoft Bing Voice Recognition
#BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
#try:
#    print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
#except sr.UnknownValueError:
#    print("Microsoft Bing Voice Recognition could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))'''

import azure.cognitiveservices.speech as speechsdk
import time


ref = ('i', 'know', 'the', 'human', 'being', 'and', 'fish', 'can', 'coexist', 'peacefully')
ref_long = 'i know the human being and fish can coexist peacefully'

def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""
    speech_key, service_region = "api_key", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=globals()["audiofilename"])
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        #print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    globals()["all_results"] = []

    def handle_final_result(evt):
        globals()["all_results"].append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    #speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    #speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    #speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    #speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

p = 1
n = 0
i = 0

while(n < 21):
    result = 0
    i = 0
    err = 0
    well = 0
    globals()["audiofilename"] = "p" + str(p) + "n" + str(n) + ".wav"
    speech_recognize_continuous_from_file()
    while(i != 10):
      if len(globals()["all_results"][0]) != 0:
        a = str(globals()["all_results"][0]).find(ref[i])
      else:
        a = 0
      if (a <= 0):
        err = err + 1
      else:
        well = well + 1
      i = i + 1
    result = (len(ref) - err) * 10
    #print(ref_long)
    print(globals()["all_results"][0])
    print(f'Result matched with reference in: {result}%' + " " + globals()["audiofilename"])
    n = n + 1

