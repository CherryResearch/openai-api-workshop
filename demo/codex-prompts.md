# Codex Prompts

## Build From Scratch

```text
Create a Python CLI called hack_idea.py.
It should take a theme argument and call the OpenAI Responses API.
Return a project idea, user story, build steps, and demo script.
Use argparse. Add a helpful error if OPENAI_API_KEY is missing.
```

## Make It Demo-Ready

```text
Make the output structured JSON.
Add --format text|json.
Add a README with setup steps.
Run it and fix any errors.
```

## Add A Second API Surface

```text
Add a second Python script transcribe.py that takes an audio file path
and uses OpenAI speech-to-text. Keep it minimal and explain where
whisper-1 fits versus realtime transcription.
```

## Turn It Into A Product

```text
Turn this CLI into a tiny FastAPI app with one form field and one results page.
Keep the implementation small. Add setup instructions and run it locally.
```

