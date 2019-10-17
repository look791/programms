import speech_recognition as sr
#from scipy.io.wavfile import read as read_wav

AUDIO_FILE = ('probe4_noise1.wav')

# use the audio file as the audio source

r = sr.Recognizer()

#sampling_rate, data=read_wav("pass2.wav") # enter your filename
#print(sampling_rate)

with sr.AudioFile(AUDIO_FILE) as source:
    # reads the audio file. Here we use record instead of
    # listen
    audio = r.record(source)

try:
    print(r.recognize_sphinx(audio, language="en-US"))

except sr.UnknownValueError:
    print("Sphinx Recognition could not understand audio")

except sr.RequestError as e:
    print("Could not request results from service;{0}".format(e))