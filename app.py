import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import subprocess
import whisper

app = Flask(__name__)

# Ensure a designated folder exists
OUTPUT_FOLDER = "transcriptions"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_audio(youtube_url, output_path):
    """
    Download audio from YouTube using yt-dlp.
    """
    command = ["yt-dlp", "--extract-audio", "--audio-format", "mp3", "-o", output_path, youtube_url]
    subprocess.run(command, check=True)

def transcribe_audio(file_path, model_type="base"):
    """
    Transcribe the audio using OpenAI Whisper.
    """
    model = whisper.load_model(model_type)
    result = model.transcribe(file_path)
    return result['text']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        output_name = request.form["output_name"]
        model_type = request.form.get("model_type", "base")

        # Define paths
        audio_path = os.path.join(OUTPUT_FOLDER, f"{output_name}.mp3")
        transcription_path = os.path.join(OUTPUT_FOLDER, f"{output_name}.txt")

        try:
            # Download and transcribe
            download_audio(youtube_url, audio_path)
            transcription = transcribe_audio(audio_path, model_type)

            # Save transcription
            with open(transcription_path, "w", encoding="utf-8") as f:
                f.write(transcription)

            return redirect(url_for("success", file_name=f"{output_name}.txt"))

        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("index.html")

@app.route("/success/<file_name>")
def success(file_name):
    return f"Transcription saved as: <a href='/transcriptions/{file_name}'>{file_name}</a>"

@app.route("/transcriptions/<file_name>")
def download_file(file_name):
    return send_from_directory(OUTPUT_FOLDER, file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)