# AweTales Audio Translation - Presentation Content

---

## Slide 1: Title Slide

**Title:** AweTales Audio Translation System

**Subtitle:** Breaking Language Barriers with AI-Powered Speech Translation

**Team Members:** Rohan, Varshit, Samith, Vivian

---

## Slide 2: Problem Statement

**Title:** The Problem

**Content:**

- Over 1.4 billion people speak Hindi and Telugu in India
- Most digital audio content is available only in English
- Language barriers limit access to education, entertainment, and information
- Manual translation is slow, expensive, and not scalable
- Existing solutions lack real-time processing capabilities

**Key Stat:** Only 10% of Indians are fluent in English, yet 90% of online content is in English

---

## Slide 3: Our Solution

**Title:** Our Solution

**Content:**

- End-to-end audio translation pipeline
- Converts English speech to Telugu/Hindi with audio output
- Web-based interface - no installation required for users
- Three-step process:
  1. Speech Recognition (English)
  2. Text Translation (Telugu/Hindi)
  3. Speech Synthesis (Native Audio)

**Tagline:** "Speak English, Hear Telugu/Hindi"

---

## Slide 4: Key Features

**Title:** Key Features

**Content:**

- Real-time audio processing
- Support for multiple Indian languages (Telugu & Hindi)
- High-accuracy transcription using Whisper AI
- Natural-sounding Text-to-Speech output
- Download transcripts in text format
- Clean, intuitive web interface
- Works on CPU and GPU

---

## Slide 5: Architecture Overview

**Title:** System Architecture

**Content:**

```
User Interface (Browser)
         |
         v
   Flask Backend
         |
    +---------+---------+
    |         |         |
    v         v         v
Transcribe  Translate   TTS
(Whisper)  (Google)   (Gemini)
    |         |         |
    +---------+---------+
              |
              v
       File Storage
```

**Components:**
- Frontend: HTML/CSS/JavaScript
- Backend: Python Flask
- Storage: Local file system

---

## Slide 6: Technology Stack

**Title:** Technology Stack

**Content:**

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Speech-to-Text | faster-whisper (OpenAI Whisper) |
| Translation | Google Translate API (deep-translator) |
| Text-to-Speech | Google Gemini API |
| ML Framework | PyTorch |

---

## Slide 7: Data Flow Pipeline

**Title:** How It Works

**Content:**

**Step 1: Audio Upload**
- User uploads English audio file (.wav, .mp3)

**Step 2: Transcription**
- faster-whisper model converts speech to English text
- Uses VAD (Voice Activity Detection) for accuracy

**Step 3: Translation**
- Google Translate API converts English to Telugu/Hindi
- Handles long texts with intelligent chunking

**Step 4: Speech Synthesis**
- Google Gemini TTS generates natural audio
- Outputs high-quality WAV files

**Step 5: Delivery**
- User receives text + audio playback in browser

---

## Slide 8: Demo / Screenshots

**Title:** Demo

**Content:**

[Add screenshots of the web interface here]

**Demo Flow:**
1. Open browser at localhost:7860
2. Upload an English audio file
3. Select target language (Telugu/Hindi)
4. Enable TTS option
5. Click "Process Audio"
6. View transcription & translation
7. Play/Download generated audio

---

## Slide 9: Future Scope

**Title:** Future Enhancements

**Content:**

- **More Languages:** Add support for Tamil, Kannada, Malayalam, Bengali
- **Voice Cloning:** Preserve speaker's voice characteristics in translation
- **Real-time Streaming:** Live translation for video calls and meetings
- **Mobile App:** Android/iOS native applications
- **Offline Mode:** On-device models for privacy and offline use
- **API Service:** RESTful API for third-party integrations
- **Batch Processing:** Handle multiple files simultaneously

---

## Slide 10: Thank You

**Title:** Thank You!

**Content:**

**Project:** AweTales Audio Translation System

**Technologies Used:**
- Python | Flask | PyTorch
- faster-whisper | Google Translate | Google Gemini

**GitHub:** [Your Repository Link]

**Questions?**

---

# Speaker Notes

## Slide 1 Notes
- Introduce yourself and team
- Mention the hackathon name

## Slide 2 Notes
- Emphasize the scale of the problem
- Use statistics to make it relatable

## Slide 3 Notes
- Keep it simple - three steps
- Show enthusiasm about the solution

## Slide 4 Notes
- Highlight unique features
- Mention both technical and user-facing features

## Slide 5 Notes
- Walk through the architecture diagram
- Explain each component briefly

## Slide 6 Notes
- Mention why each technology was chosen
- Highlight open-source components

## Slide 7 Notes
- Use animation to show step-by-step flow
- Emphasize the speed of processing

## Slide 8 Notes
- Live demo is best if time permits
- Have a backup video ready

## Slide 9 Notes
- Show vision and roadmap
- Voice cloning is an exciting future feature

## Slide 10 Notes
- Thank the judges/audience
- Open floor for questions
