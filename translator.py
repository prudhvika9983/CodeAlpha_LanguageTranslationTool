from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    audio_file = None

    if request.method == "POST":
        text = request.form["text"]
        source_lang = request.form["source_lang"]
        target_lang = request.form["target_lang"]

        if source_lang == target_lang and source_lang != "auto":
            translated_text = "Source and Target languages are the same."
        else:
            # Translate text
            translated_text = GoogleTranslator(
                source=source_lang,
                target=target_lang
            ).translate(text)
        # Text-to-Speech
        tts = gTTS(text=translated_text, lang=target_lang)
        filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join("static", filename)
        tts.save(audio_path)
        audio_file = filename

    return render_template(
        "index.html",
        translated_text=translated_text,
        audio_file=audio_file
    )

if __name__ == "__main__":
    app.run(debug=True)