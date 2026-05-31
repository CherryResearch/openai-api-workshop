# Demo Package

Python demo scripts for the 15-minute Codex-first OpenAI API workshop.

## Install

```powershell
cd ..
poetry install
$env:OPENAI_API_KEY="your_api_key_here"
```

If `OPENAI_API_KEY` is already exported, skip the API key line.

## Launch Workshop Pages

```powershell
poetry run workshop-pages
```

This starts a local server from the repository root and opens the workshop
landing page. Press `Ctrl+C` when you are done.

Optionally set a model:

```powershell
$env:OPENAI_MODEL="gpt-5.5"
```

## Idea Generator

```powershell
poetry run hack-idea "vibe coding for hackathons"
poetry run hack-idea "vibe coding for hackathons" --format json
```

## Speech-To-Text Teaser

```powershell
poetry run transcribe-audio path\to\audio.mp3
```

This defaults to `whisper-1` for a simple file transcription demo. For live
audio, use the Realtime transcription path from the OpenAI docs.
