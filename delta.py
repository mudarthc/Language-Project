# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from google.cloud import texttospeech
from google.cloud import speech
import unidecode
from pydub import AudioSegment

from scipy.io import wavfile
from pydub.playback import play

import subprocess

import io
import os
# Instantiates a client


import speech_recognition as sr 
r= sr.Recognizer()
with sr.Microphone() as source:
    print("Say something");
    audio = r.listen(source)
    print("Time over")





client = language.LanguageServiceClient()

# The text to analyze
text = unidecode.unidecode(r.recognize_google(audio))
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))



try: 


# Instantiates a client

#################
# Imports the Google Cloud client library

# Instantiates a client
    client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text= r.recognize_google(audio))

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

# Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    if sentiment.score < 0:
        octaves = -0.2
        frame =  70000
    if sentiment.score > 0:
        octaves = 0.2
        frame = 44000
    if sentiment.score == 0:
        octaves = 0
        frame = 44100

    sound = AudioSegment.from_mp3("output.mp3")
    sound.export("apple.wav", format="wav")
    sound = AudioSegment.from_file('apple.wav', format="wav")

# shift the pitch up by half an octave (speed will increase proportionally)
    

    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

# keep the same samples but tell the computer they ought to be played at the 
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
    hipitch_sound = hipitch_sound.set_frame_rate(frame)

#Play pitch changed sound
    play(hipitch_sound)

#export / save pitch changed sound
    




except: 
    pass;
