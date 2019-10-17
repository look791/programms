# Libraries --------------------------------------------------------------------------------------------

from scipy.io.wavfile import write, read
import os
import sys
import numpy as np
import math
from wit import Wit
import azure.cognitiveservices.speech as speechsdk
import time

eps = np.finfo(float).eps
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './utilFunctions_C/'))
try:
    import utilFunctions_C as UF_C
except ImportError:
    print("\n")
    print("-------------------------------------------------------------------------------")
    print("Warning:")
    print("Cython modules for some of the core functions were not imported.")
    print("Please refer to the README.md file in the 'sms-tools' directory,")
    print("for the instructions to compile the cython modules.")
    print("Exiting the code!!")
    print("-------------------------------------------------------------------------------")
    print("\n")
    sys.exit(0)

# Definitions ----------------------------------------------------------------------------------------
def wavread(filename):
    INT16_FAC = (2 ** 15) - 1
    INT32_FAC = (2 ** 31) - 1
    INT64_FAC = (2 ** 63) - 1
    norm_fact = {'int16': INT16_FAC, 'int32': INT32_FAC, 'int64': INT64_FAC, 'float32': 1.0, 'float64': 1.0}
    """
    Read a sound file and convert it to a normalized floating point array
    filename: name of file to read
    returns fs: sampling rate of file, x: floating point array
    """
    if (os.path.isfile(filename) == False):  # raise error if wrong input file
        raise ValueError("Input file is wrong")
    fs, x = read(filename)
    if (len(x.shape) != 1):  # raise error if more than one channel
        raise ValueError("Audio file should be mono")
    if (fs != 44100):  # raise error if more than one channel
        raise ValueError("Sampling rate of input sound should be 44100")
    # scale down and convert audio into floating point number in range of -1 to 1
    x = np.float32(x) / norm_fact[x.dtype.name]
    return fs, x
def signaltonoise(a, axis=0, ddof=0):
    """
    The signal-to-noise ratio of the input data.
    Returns the signal-to-noise ratio of `a`, here defined as the mean
    divided by the standard deviation.
    Parameters
    ----------
    a : array_like
        An array_like object containing the sample data.
    axis : int or None, optional
        If axis is equal to None, the array is first ravel'd. If axis is an
        integer, this is the axis over which to operate. Default is 0.
    ddof : int, optional
        Degrees of freedom correction for standard deviation. Default is 0.
    Returns
    -------
    s2n : ndarray
        The mean to standard deviation ratio(s) along `axis`, or 0 where the
        standard deviation is 0.
    """
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)
def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""
    speech_key, service_region = "64ceb5014e30446b901ddec92f5e0fb1", "eastus"
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
    ''''#speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    #speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    #speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    #speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events'''
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    #logs.write(str(globals()["all_results"][0]) + '\n')
def test_result(fl):
    if fl == sp:
        passed = 1
    else:
        raise ValueError(1)
    return passed

# Variables ------------------------------------------------------------------------------------------
n = 0
p = 1
SNRs = []
AZURE = []
WIT = []
sp = 20
fl = 0
passed = 0

# Flags vector (0: SNR && (AZURE || WIT) = false, 1: SNR && (AZURE || WIT) = true) -------------------
flags_s = []
flags_a = []
flags_w = []
flags = []
nr = str(time.strftime("%m%d%H%M%S"))
logs = open(f'{nr}_voice_verify_log.txt', 'w')
logs.write(f'{time.strftime("%H:%M:%S")} TEST STARTED\n')

# Constant -------------------------------------------------------------------------------------------
ref = ('i', 'know', 'the', 'human', 'being', 'and', 'fish', 'can', 'coexist', 'peacefully')
ref_long = 'i know the human being and fish can coexist peacefully'

# Thresholds (snr_tr - acceptable level of SNR, azure_tr - more than 70% recognized, wit_tr - more than 70% recognized)
snr_tr = -30
azure_tr = 50
wit_tr = 50
logs.write(f'{time.strftime("%H:%M:%S")} ' + 'Thresholds - SNR[dB]:'f'{snr_tr} ' + 'Azure[%]:'f'{azure_tr} \n')

# SNR calculation ------------------------------------------------------------------------------------
while(n < sp):
    globals()["audiofilename"] = "p" + str(p) + "n" + str(n) + ".wav"
    fs, x = wavread(globals()["audiofilename"])
    snr = signaltonoise(x, axis=0, ddof=0)
    db = 10 * math.log10(abs(snr))
    #print("Signal/Noise (S/N) = " + str(round(db,2)) + "[dB] in file " + str(globals()["audiofilename"]))
    logs.write(f'{time.strftime("%H:%M:%S")}')
    logs.write(" Signal/Noise (S/N) = " + str(round(db, 2)) + "[dB] in file " + str(globals()["audiofilename"] + "\n"))
    n = n + 1
    SNRs.append(round(db))
    if db < snr_tr:
        flags_s.append(1)
    else:
        flags_s.append(0)
#print("SNR [dB]: " + str(SNRs))
print("SNR(stage 1): " + str(flags_s))

# Azure recognition ----------------------------------------------------------------------------------
p = 1
n = 0
i = 0
while(n < sp):
    result = 0
    i = 0
    err = 0
    well = 0
    globals()["audiofilename"] = "p" + str(p) + "n" + str(n) + ".wav"
    speech_recognize_continuous_from_file()
    while(i != 10):
      if len(globals()["all_results"]) != 0:
        a = str(globals()["all_results"][0]).find(ref[i])
      else:
        a = 0
      if (a <= 0):
        err = err + 1
      else:
        well = well + 1
      i = i + 1
    result = (len(ref) - err) * 10
    #print(f'Result matched with reference in: {result}%' + " " + globals()["audiofilename"])
    logs.write(f'{time.strftime("%H:%M:%S")}')
    logs.write(f' Result matched with reference in: {result}%' + " " + globals()["audiofilename"] + "\n")
    n = n + 1
    AZURE.append(result)
    if result > azure_tr:
        flags_a.append(1)
    else:
        flags_a.append(0)
#print("Azure [%]: " + str(AZURE))
print("AZURE(stage 2): " + str(flags_a))

'''
# Wit.ai recognition

client = Wit('I5IIH7FKUKTUGPLHUCQXSRJOIGB45CXA')
resp = None
i = 0
err = 0
well = 0

p = 1
n = 0

while(n < sp):
    result = 0
    i = 0
    err = 0
    well = 0
    with open(globals()["audiofilename"], 'rb') as f:
      resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
      globals()["audiofilename"] = "p" + str(p) + "n" + str(n) + ".wav"
    while(i != 10):
      a = str(resp['_text']).find(ref[i])
      if (a == -1):
        err = err + 1
      else:
        well = well + 1
      i = i + 1
    result = (len(ref) - err) * 10
    #print(f'Result matched with reference in: {result}%' + " " + globals()["audiofilename"])
    n = n + 1
    WIT.append(result)
    if result > wit_tr:
        flags_w.append(1)
    else:
        flags_w.append(0)

#print("WIT [%]: " + str(WIT))
print("WIT: " + str(flags_w))
'''
r = 0
st_1 = []
st_2 = []
p = 1
n = 0
# Results ----------------------------------------------------------------------------------------------
while(r < sp):

    if int(flags_s[r]) > 0:
        st1 = 1
        if (int(flags_a[r])) > 0:
        #if (int(flags_a[r]) or int(flags_w[r])) > 0:
            st2 = 1
            print("Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was passed.")
            logs.write(f'{time.strftime("%H:%M:%S")}')
            logs.write(" Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was passed.\n")
        else:
            st2 = 0
            print("Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was failed.")
            logs.write(f'{time.strftime("%H:%M:%S")}')
            logs.write(" Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was failed.\n")
    else:
        st2 = 0
        st1 = 0
        print("Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was failed.")
        logs.write(f'{time.strftime("%H:%M:%S")}')
        logs.write(" Sample: " + "p" + str(p) + "n" + str(n) + ".wav" + " was failed.\n")
    st_2.append(st2)
    r = r + 1
    n = n + 1

for st_22 in st_2:
    if st_22 > 0:
        fl = fl + 1
logs.write(f'{time.strftime("%H:%M:%S")}')
logs.write(" TOTAL: " + str(fl) + "/" + str(sp) + " was passed.\n")
#print("Stage 1 & 2: " + str(st_2))
logs.close()
#test_result(fl)





