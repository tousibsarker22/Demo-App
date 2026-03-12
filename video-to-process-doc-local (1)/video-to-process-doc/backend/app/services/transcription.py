import os
from pathlib import Path
import time
import azure.cognitiveservices.speech as speechsdk


def transcribe_with_azure(audio_path: Path) -> str:
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    if not (speech_key and service_region):
        raise RuntimeError("Azure Speech credentials missing.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "en-US"

    audio_input = speechsdk.audio.AudioConfig(filename=str(audio_path))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    done = False
    results = []

    def handle_recognized(evt):
        if evt.result and evt.result.text:
            results.append(evt.result.text)

    def stop_cb(evt):
        nonlocal done
        done = True

    recognizer.recognized.connect(handle_recognized)
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)

    recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)
    recognizer.stop_continuous_recognition()

    return "
".join(results)


def clean_transcript(text: str) -> str:
    return (
        text.replace(" uh ", " ").replace(" um ", " ").replace("you know", "")
            .replace("kind of", "").replace("sort of", "")
    )
