# Attendee Handout

## Goal

Build a tiny Python app that uses the OpenAI API, with Codex doing the code
assembly and you steering the product.

## Setup

```powershell
cd demo
poetry install
$env:OPENAI_API_KEY="your_api_key_here"
```

## Open The Workshop Pages

```powershell
poetry run workshop-pages
```

## Run

```powershell
poetry run hack-idea "AI tools for student builders"
poetry run hack-idea "AI tools for student builders" --format json
```

## Prompt Codex Like This

```text
I am building [thing] for [user].
Use Python and the OpenAI API.
Start with the smallest working version.
Create files, run them, and fix errors.
Explain the next 3 improvements after it works.
```

## Useful API Directions

- Text: summaries, planning, classification, app logic.
- Images: generated posters, avatars, product visuals, storyboards.
- Speech to text: transcripts, captions, notes, meeting search.
- Text to speech: narration, accessibility, generated voice responses.
- Realtime: voice agents, live tutoring, low-latency conversations.
- Tools/function calling: connect the model to your app actions and data.

## Official Docs

- Quickstart: https://developers.openai.com/api/docs/quickstart
- Text generation: https://developers.openai.com/api/docs/guides/text
- Images: https://developers.openai.com/api/docs/guides/image-generation
- Speech to text: https://developers.openai.com/api/docs/guides/speech-to-text
- Audio: https://developers.openai.com/api/docs/guides/audio
- Realtime: https://developers.openai.com/api/docs/guides/realtime
- Codex: https://developers.openai.com/codex/quickstart
