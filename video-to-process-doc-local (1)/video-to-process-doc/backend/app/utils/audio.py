from pathlib import Path
import subprocess

def extract_audio(input_path: Path, out_ext: str = ".wav") -> Path:
    audio_path = input_path.with_suffix(out_ext)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(audio_path),
    ]
    subprocess.run(cmd, check=True)
    return audio_path
