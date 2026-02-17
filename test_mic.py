import sounddevice as sd
import queue
import json
import time
import datetime
import os
import wave
import soundfile as sf

from vosk import Model, KaldiRecognizer
from commands import recognize_command
from piper import PiperVoice

q = queue.Queue()

# Volume
current_volume = 80

# Timeout control
TIMEOUT_SECONDS = 30
last_command_time = time.time()

# Wake words (reduced false triggers)
WAKE_WORDS = ["हे रोही", "असिस्टेंट", "ओए रोही","रोही","सुनो असिस्टेंट"]


def callback(indata, frames, time_info, status):
    if status:
        print(status)
    q.put(bytes(indata))


# Load Piper voice once
voice = PiperVoice.load("hi_IN-pratham-medium.onnx")


def speak(text, start_time=None):
    print("Assistant:", text)

    with wave.open("temp.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    audio, samplerate = sf.read("temp.wav")

    # Measure response time
    if start_time is not None:
        response_time = time.time() - start_time
        print("Response time:", round(response_time, 3), "sec")

    sd.play(audio, samplerate, device=1)
    sd.wait()


def perform_action(intent, start_time):
    global current_volume

    if intent == "GET_TIME":
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"अब समय {now}", start_time)

    elif intent == "GET_DATE":
        today = datetime.date.today().strftime("%d-%m-%Y")
        speak(f"तारीख {today}", start_time)

    elif intent == "GREETING":
        speak("नमस्ते", start_time)

    elif intent == "INTRO":
        speak("मैं रोही एक ऑफलाइन असिस्टेंट हूँ", start_time)

    elif intent == "THANKS":
        speak("स्वागत है", start_time)

    elif intent == "STATUS":
        speak("सब ठीक है", start_time)

    elif intent == "HELP":
        speak("समय या संगीत बोलें", start_time)

    elif intent == "PLAY_MUSIC":
        speak("संगीत चला रहा हूँ", start_time)
        os.system("mpg123 song.mp3 &")

    elif intent == "STOP_MUSIC":
        speak("संगीत बंद", start_time)
        os.system("pkill -f mpg123")

    elif intent == "VOLUME_UP":
        current_volume = min(100, current_volume + 10)
        speak("आवाज़ बढ़ा रहा हूँ", start_time)
        os.system(f"amixer -c 2 set PCM {current_volume}%")

    elif intent == "VOLUME_DOWN":
        current_volume = max(20, current_volume - 10)
        speak("आवाज़ कम कर रहा हूँ", start_time)
        os.system(f"amixer -c 2 set PCM {current_volume}%")

    elif intent == "EXIT":
        speak("स्लीप मोड")
        sleep_mode()

    else:
        speak("समझ नहीं आया", start_time)


def sleep_mode():
    """
    Sleep mode with wake word detection.
    Assistant stays running but waits for wake word.
    """
    speak("स्लीप मोड")

    while True:
        data = q.get()
        time.sleep(0.05)  # reduces CPU usage and temperature

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()

            if len(text) < 2:
                continue

            print("Sleep heard:", text)

            for word in WAKE_WORDS:
                if word in text:
                    speak("तैयार हूँ")
                    rec.Reset()
                    return


# Load Hindi ASR model
model = Model("/home/srujan_2425/voice_project/vosk-model-small-hi-0.22")

samplerate = 44100
device_id = 2

rec = KaldiRecognizer(model, samplerate)

# Reduce CPU usage slightly
rec.SetWords(False)


with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=3000,
        device=device_id,
        dtype='int16',
        channels=1,
        callback=callback):

    print("Assistant ready...")
    speak("तैयार हूँ")

    while True:
        data = q.get()

        # Check inactivity timeout
        if time.time() - last_command_time > TIMEOUT_SECONDS:
            sleep_mode()
            last_command_time = time.time()
            continue

        start_time = time.time()

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()

            if len(text) < 2:
                continue

            print("\nYou said:", text)

            intent = recognize_command(text)
            print("Intent:", intent)

            perform_action(intent, start_time)

            last_command_time = time.time()

            total_time = time.time() - start_time
            print("Total time:", round(total_time, 3), "sec")
