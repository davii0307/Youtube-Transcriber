#!//Users/davidni/opt/anaconda3/envs/new_env/bin/python

import subprocess
import whisper
import argparse
import os

def download_audio(youtube_url, output_path="audio.mp3"):
    """
    Download audio from a YouTube video using yt-dlp.
    """
    try:
        print("[INFO] Downloading audio...")
        command = ["yt-dlp", "--extract-audio", "--audio-format", "mp3", "-o", output_path, youtube_url]
        subprocess.run(command, check=True)
        print(f"[INFO] Audio downloaded to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to download audio: {e}")
        raise

def transcribe_audio(file_path, model_type="base"):
    """
    Transcribe the audio using OpenAI Whisper.
    """
    try:
        print("[INFO] Loading Whisper model...")
        model = whisper.load_model(model_type)
        print("[INFO] Transcribing audio...")
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        print(f"[ERROR] Failed to transcribe audio: {e}")
        raise

def save_transcription(text, output_file):
    """
    Save the transcription to a text file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[INFO] Transcription saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Transcriber CLI Tool")
    parser.add_argument("url", type=str, help="URL of the YouTube video")
    parser.add_argument("--output", type=str, default="transcription.txt", help="File to save the transcription")
    parser.add_argument("--model", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model type")
    
    args = parser.parse_args()

    # Temporary file for the audio
    audio_file = "audio.mp3"

    try:
        # Download audio and transcribe
        download_audio(args.url, audio_file)
        transcription = transcribe_audio(audio_file, args.model)

        # Save or print the transcription
        save_transcription(transcription, args.output)
        print("[INFO] Transcription completed successfully!")
    finally:
        # Clean up temporary files
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    main()
