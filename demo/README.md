# Demo Package

Python demo scripts for the 15-minute Codex-first OpenAI API workshop.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
$env:OPENAI_API_KEY="your_api_key_here"
```

Optionally set a model:

```powershell
$env:OPENAI_MODEL="gpt-5.5"
```

## Idea Generator

```powershell
hack-idea "vibe coding for hackathons"
hack-idea "vibe coding for hackathons" --format json
```

## Speech-To-Text Teaser

```powershell
transcribe-audio path\to\audio.mp3
```

This defaults to `whisper-1` for a simple file transcription demo. For live
audio, use the Realtime transcription path from the OpenAI docs.

