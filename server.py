from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    audio_url = request.json.get("url")
    audio_file = request.files.get("file")

    if not audio_url and not audio_file:
        return jsonify({"error": "Send file or url"}), 400

    # Download file from URL
    if audio_url:
        try:
            audio_data = requests.get(audio_url).content
        except Exception as e:
            return jsonify({"error": f"Error downloading audio: {e}"}), 500
    else:
        audio_data = audio_file.read()

    files = {
        "file": ("audio.ogg", audio_data, "audio/ogg"),
    }
    data = {
        "model": "gpt-4o-audio-preview",
        "temperature": 0,
        "prompt": "الرجاء تقديم تفريغ دقيق خالٍ من الأخطاء وباللهجة العربية إن وجدت."
    }

    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        files=files,
        data=data
    )

    try:
        return response.json()
    except:
        return jsonify({"error": "Invalid OpenAI response"}), 500


@app.route("/", methods=["GET"])
def home():
    return "Whisper Proxy is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
