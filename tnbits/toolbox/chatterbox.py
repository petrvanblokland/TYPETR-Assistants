# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#

try:
    from AppKit import NSSpeechSynthesizer
except:
    print('Can\'t import AppKit NSSpeechSynthesizer')

import random
import time

class Chatterbox(object):
    """The `Chatterbox` object speaks to you from an app."""

    DEFAULTVOICE = "com.apple.speech.synthesis.voice.Alex"
    VOICEPREFIX = "com.apple.speech.synthesis.voice."
    VOICES = [
        "com.apple.speech.synthesis.voice.Agnes",
        "com.apple.speech.synthesis.voice.Albert",
        "com.apple.speech.synthesis.voice.Alex",
        "com.apple.speech.synthesis.voice.BadNews",
        "com.apple.speech.synthesis.voice.Bahh",
        "com.apple.speech.synthesis.voice.Bells",
        "com.apple.speech.synthesis.voice.Boing",
        "com.apple.speech.synthesis.voice.Bruce",
        "com.apple.speech.synthesis.voice.Bubbles",
        "com.apple.speech.synthesis.voice.Cellos",
        #"com.apple.speech.synthesis.voice.Deranged",
        "com.apple.speech.synthesis.voice.Fred",
        "com.apple.speech.synthesis.voice.GoodNews",
        #"com.apple.speech.synthesis.voice.Hysterical",
        "com.apple.speech.synthesis.voice.Junior",
        "com.apple.speech.synthesis.voice.Kathy",
        "com.apple.speech.synthesis.voice.Organ",
        "com.apple.speech.synthesis.voice.Princess",
        "com.apple.speech.synthesis.voice.Ralph",
        "com.apple.speech.synthesis.voice.Trinoids",
        "com.apple.speech.synthesis.voice.Vicki",
        "com.apple.speech.synthesis.voice.Victoria",
        "com.apple.speech.synthesis.voice.Whisper",
        "com.apple.speech.synthesis.voice.Zarvox",
    ]

    @classmethod
    def getRandomVoice(cls):
        return random.choice(cls.VOICES)

    @classmethod
    def speak(cls, partstring, voice=None, sleep=True):
        if not voice:
            voice = cls.DEFAULTVOICE

        nssp = NSSpeechSynthesizer
        ve = nssp.alloc().init()
        if (len(voice) > 4 and voice[:4] != 'com.') or len(voice) < 4:
            voice = cls.VOICEPREFIX + voice.capitalize()
        ve.setVoice_(voice)
        ve.startSpeakingString_(partstring)
        if sleep:
            while ve.isSpeaking():
                time.sleep(1)

    @classmethod
    def speakWithRandomVoice(cls, partstring, sleep=True):
        voice = cls.getRandomVoice()
        cls.speak(partstring, voice, sleep)

if __name__ == "__main__":
    for voice in Chatterbox.VOICES:
        voiceName = voice.split('.')[-1]
        text = "Hello my name is %s. We should hang out sometime." %voiceName
        Chatterbox.speak(text, voice)
        print(text)
