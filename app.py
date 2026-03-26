"""
AweTales Hackathon - Audio Translation API
Transcribe English audio, translate to Telugu/Hindi, and generate speech
Optimized for speed using faster-whisper and Google Translate API
"""

import os
import warnings
import time
import wave
import torch
from flask import Flask, request, jsonify, send_file, render_template
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask app setup with explicit static/template paths
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['AUDIO_FOLDER'] = os.path.join(BASE_DIR, 'audio_files')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
print(f"Using device: {device.upper()}")

# Global model variables
whisper_model = None

# Language codes for Google Translate
LANG_CODES = {
    'Telugu': 'te',
    'Hindi': 'hi'
}


def initialize_models():
    """Load whisper model"""
    global whisper_model

    print("Loading faster-whisper model (small)...")
    from faster_whisper import WhisperModel
    whisper_model = WhisperModel("small", device=device, compute_type=compute_type)
    print("Model loaded successfully!")


def transcribe_audio(audio_path):
    """Transcribe audio using faster-whisper with improved accuracy"""
    if whisper_model is None:
        initialize_models()

    segments, info = whisper_model.transcribe(
        audio_path,
        language='en',
        beam_size=10,
        best_of=5,
        temperature=0.0,
        condition_on_previous_text=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    # Combine all segments
    text = " ".join([segment.text.strip() for segment in segments])
    return text


def translate_text(text, target_language):
    """Translate text using Google Translate API"""
    if not text or not text.strip():
        return ""

    try:
        from deep_translator import GoogleTranslator

        target_code = LANG_CODES.get(target_language)
        if not target_code:
            raise ValueError(f"Language must be 'Telugu' or 'Hindi', got: {target_language}")

        translator = GoogleTranslator(source='en', target=target_code)

        # Split text into chunks if too long (Google Translate limit is ~5000 chars)
        max_chunk = 4500
        if len(text) <= max_chunk:
            return translator.translate(text)

        # Process in chunks
        words = text.split()
        chunks = []
        current_chunk = []
        current_len = 0

        for word in words:
            if current_len + len(word) + 1 > max_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_len = len(word)
            else:
                current_chunk.append(word)
                current_len += len(word) + 1

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        # Translate each chunk
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        return ' '.join(translated_chunks)

    except Exception as e:
        print(f"Translation error: {e}")
        return f"[Translation failed: {str(e)}]"


def text_to_speech(text, language, output_file='output.wav'):
    """Convert text to speech using Google Gemini API"""
    try:
        from google import genai
        from google.genai import types

        api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            return None, "Google API key not found. Please set GOOGLE_API_KEY in .env file."

        client = genai.Client(api_key=api_key)

        # Create prompt with language instruction
        if language == 'Telugu':
            prompt = f"Speak the following Telugu text naturally: {text}"
        elif language == 'Hindi':
            prompt = f"Speak the following Hindi text naturally: {text}"
        else:
            prompt = text

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                        )
                    )
                ),
            )
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        output_path = os.path.join(app.config['AUDIO_FOLDER'], output_file)

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_data)

        return output_path, "Audio generated successfully!"

    except Exception as e:
        return None, f"TTS Error: {str(e)}"


def process_audio(audio_path, target_language, generate_tts):
    """Main processing function - optimized for speed"""
    # Transcribe entire audio at once (no segmentation)
    english_text = transcribe_audio(audio_path)

    if not english_text:
        return {
            'english_text': '',
            'translated_text': '',
            'tts_audio': None,
            'tts_status': 'No speech detected in audio'
        }

    # Translate
    translated_text = translate_text(english_text, target_language)

    # Generate TTS if requested
    tts_audio_path = None
    tts_status = ""

    if generate_tts and translated_text:
        timestamp = int(time.time())
        tts_audio_path, tts_status = text_to_speech(
            translated_text,
            target_language,
            f'output_{target_language.lower()}_{timestamp}.wav'
        )

    return {
        'english_text': english_text,
        'translated_text': translated_text,
        'tts_audio': os.path.basename(tts_audio_path) if tts_audio_path else None,
        'tts_status': tts_status
    }


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def api_process():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400

    target_language = request.form.get('language', 'Telugu')
    generate_tts = request.form.get('tts', 'true').lower() == 'true'

    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(filepath)

    try:
        result = process_audio(filepath, target_language, generate_tts)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


@app.route('/api/download/transcript', methods=['POST'])
def download_transcript():
    data = request.json
    english_text = data.get('english', '')
    translated_text = data.get('translated', '')
    language = data.get('language', 'Telugu')

    transcript = f"=== English Transcription ===\n\n{english_text}\n\n"
    transcript += f"=== {language} Translation ===\n\n{translated_text}\n"

    filename = f'transcript_{int(time.time())}.txt'
    filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(transcript)

    return send_file(filepath, as_attachment=True, download_name=filename)


@app.route('/api/audio/<filename>')
def get_audio(filename):
    filepath = os.path.join(app.config['AUDIO_FOLDER'], secure_filename(filename))
    if os.path.exists(filepath):
        mimetype = 'audio/wav' if filename.endswith('.wav') else 'audio/mpeg'
        return send_file(filepath, mimetype=mimetype)
    return jsonify({'error': 'File not found'}), 404


if __name__ == "__main__":
    print("Starting AweTales Audio Translation Server (Optimized)...")
    print("=" * 60)

    try:
        initialize_models()
    except Exception as e:
        print(f"Warning: Could not pre-load models: {e}")
        print("Models will be loaded on first use.")

    app.run(host='127.0.0.1', port=7860, debug=True)
