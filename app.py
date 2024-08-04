

from flask import Flask, render_template, request, send_file, redirect, url_for
from elevenlabs.client import ElevenLabs
import os

app = Flask(__name__)
app.debug = True

# Use the temporary directory if running in a read-only file system
audio_folder = '/tmp/audio'
os.makedirs(audio_folder, exist_ok=True)

# Initialize the ElevenLabs client
client = ElevenLabs(
    api_key="sk_b08dcad52d5ee7fb2adc2c5eabd76d575bcdfedd428495fb"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    if text:
        try:
            # Generate the audio using ElevenLabs
            audio_generator = client.generate(
                text=text,
                voice="Adam",
                model="eleven_multilingual_v2"
            )

            # Save the audio file
            filename = os.path.join(audio_folder, 'tts_output.mp3')
            with open(filename, 'wb') as f:
                for chunk in audio_generator:
                    f.write(chunk)

            return send_file(filename, as_attachment=True)

        except Exception as e:
            print(f"Error occurred: {e}")
            return "An error occurred during audio generation.", 500

    return redirect(url_for('index'))
