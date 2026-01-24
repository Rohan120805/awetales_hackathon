
# AweTales Hackathon (Notebooks)

This repo contains two working notebooks:

- `project.ipynb`: English speech-to-text (Whisper) + translation to Telugu/Hindi (NLLB).
- `tts.ipynb`: Text-to-speech for Telugu/Hindi (Google Cloud TTS or free gTTS).

> Note: `voice_cloning_pipeline.ipynb` is intentionally **not** documented here (it’s experimental and not working reliably).

---

## Prerequisites (Windows)

- Python 3.10+ recommended
- Internet connection (models + TTS)
- **FFmpeg** (required for `project.ipynb` audio loading via `pydub`)
	- Option A (Chocolatey): `choco install ffmpeg`
	- Option B (Winget): `winget install Gyan.FFmpeg`
	- Verify: `ffmpeg -version`

If you don’t have package managers, install FFmpeg manually and add it to your PATH.

---

## 1) Create a virtual environment

From the project folder:

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

### CMD

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
```

Install Jupyter tooling:

```bat
pip install jupyter ipykernel
```

Optional (adds a dedicated kernel in Jupyter):

```bat
python -m ipykernel install --user --name awetales-hackathon --display-name "Python (awetales)"
```

---

## 2) Install dependencies for `project.ipynb` (Whisper + Translation)

This notebook imports: `torch`, `whisper` (OpenAI Whisper), `transformers`, `pydub`.

### Install PyTorch

CPU-only (most reliable):

```bat
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

If you have an NVIDIA GPU and want CUDA support, install the matching CUDA build from the official PyTorch selector.

### Install the rest

```bat
pip install -U openai-whisper transformers sentencepiece pydub
```

Common Windows note: if any package tries to compile and fails, install Microsoft C++ Build Tools.

---

## 3) Run `project.ipynb`

Start Jupyter:

```bat
jupyter notebook
```

Inside the notebook, set:

- `AUDIO_FILE` (example already points to `audio_files\dog.wav`)
- `OUTPUT_LANGUAGE` to either `telugu` or `hindi`

If you see errors like “ffmpeg not found”, fix your FFmpeg installation/PATH.

---

## 4) Install dependencies for `tts.ipynb` (Text-to-Speech)

This notebook supports two options:

### Option A (Recommended): Google Cloud Text-to-Speech

Install packages:

```bat
pip install -U google-cloud-texttospeech python-dotenv
```

Google Cloud setup (service account JSON — most standard for GCP):

1. Create a Google Cloud project
2. Enable **Text-to-Speech API**
3. Create a **Service Account** and download a JSON key
4. Set `GOOGLE_APPLICATION_CREDENTIALS` to the JSON file path (system env var or in the notebook cell)

Example (PowerShell):

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\credentials.json"
```

The notebook also tries to load `GOOGLE_API_KEY`/`API_KEY` from a `.env` file for an API-key-based client setup.
If you use that flow, create a `.env` next to the notebook:

```env
GOOGLE_API_KEY=your_key_here
```

### Option B (Simplest): gTTS (no API keys)

Install:

```bat
pip install -U gtts
```

This generates MP3 files into the `audio_files/` folder.

---

## 5) Run `tts.ipynb`

Start Jupyter if it’s not running:

```bat
jupyter notebook
```

Open `tts.ipynb` and run cells **top-to-bottom** (some example cells call helper functions that are defined later in the notebook).
Generated audio files are saved under `audio_files/`.

---

## Troubleshooting

- **`pydub` can’t find ffmpeg**: install FFmpeg and ensure `ffmpeg.exe` is on PATH.
- **Models are slow on CPU**: Whisper + translation models are heavy; GPU helps a lot.
- **Google TTS auth issues**: prefer `GOOGLE_APPLICATION_CREDENTIALS` service-account JSON setup.

