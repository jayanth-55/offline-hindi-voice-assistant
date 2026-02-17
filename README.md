# Offline Hindi Voice Assistant (Raspberry Pi)

This project implements a fully offline Hindi voice assistant running on Raspberry Pi.  
It captures voice from a USB microphone, recognizes Hindi speech locally, detects commands, and responds using offline text-to-speech.

## System Architecture

Microphone → Vosk ASR → Intent Recognition → Piper TTS → Speaker

## Performance
-Response time: ~1.5 second
-Offline operation: Yes
-Commands supported: 10–15 Hindi commands

## Features
- Offline Hindi speech recognition (Vosk)
- Keyword-based command recognition
- Offline text-to-speech (Piper)
- Wake word detection
- Sleep mode after inactivity
- Music playback and volume control
- Runs completely offline

## Hardware Required
- Raspberry Pi
- USB microphone
- Speaker or headphones

## Software Requirements
- Python 3
- Vosk
- Piper TTS
- Sounddevice
- Soundfile

## Installation

Clone the repository:

git clone https://github.com/jayanth-55/offline-hindi-voice-assistant.git

Navigate into project:

cd offline-hindi-voice-assistant

Create virtual environment:

python3 -m venv venv  
source venv/bin/activate  

Install dependencies:

pip install -r requirements.txt

## Download Models

Download Hindi Vosk model:
https://alphacephei.com/vosk/models

Extract and place it in the project folder.

Download Piper Hindi voice:
https://github.com/rhasspy/piper

Place the .onnx file in the project directory.

## Run

python test_mic.py

## Example Commands
- समय क्या है
- तारीख क्या है
- नमस्ते
- संगीत चलाओ
- संगीत बंद करो
- आवाज बढ़ाओ
- आवाज कम करो
- कैसे हो
- धन्यवाद
- तुम कौन ह

## Project Overview
This project implements a fully offline Hindi voice assistant on Raspberry Pi using Vosk for speech recognition and Piper for text-to-speech. The system processes audio locally with response time under 2 seconds.

## Project Goal
Build a low-latency offline Hindi voice assistant running on ARM hardware.
