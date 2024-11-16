from flask import Flask, render_template, request
import googletrans
from googletrans import Translator
import gtts
from gtts import gTTS
import time
import os

app = Flask(__name__)

# Get supported languages from googletrans
language_codes = googletrans.LANGUAGES
languages = [{"code": code, "name": name} for code, name in language_codes.items()]

# Ensure the static directory exists
os.makedirs("static", exist_ok=True)

def translate_text(text, target_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        input_text = request.form.get("input_text")
        target_language = request.form.get("target_language")
        
        # Validate inputs
        if not input_text or not target_language:
            return render_template("index.html", languages=languages, error="Please provide text and select a language.")

        # Translate text
        translated_text = translate_text(input_text, target_language)
        if translated_text.startswith("Error:"):
            return render_template("index.html", languages=languages, input_text=input_text, error=translated_text)

        # Generate speech for the translated text
        timestamp = int(time.time())
        filename = f"static/op_{timestamp}.mp3"
        
        try:
            tts = gTTS(translated_text, lang=target_language)
            tts.save(filename)
        except Exception as e:
            return render_template("index.html", languages=languages, input_text=input_text, error=f"Error generating audio: {e}")
        
        return render_template("index.html", languages=languages, input_text=input_text, translated_text=translated_text, audio_filename=filename)

    return render_template("index.html", languages=languages)

if __name__ == "__main__":
    app.run(debug=True)
