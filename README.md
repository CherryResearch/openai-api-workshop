# Codex-First OpenAI API Workshop

A 15-minute hackathon workshop package for showing how to build with the OpenAI
API using Codex as the live coding partner.

## What Is Included

- `slides.html` - polished browser slides with keyboard navigation, setup
  steps, copy buttons, and sample run outputs.
- `speaker-notes.md` - minute-by-minute talk track and demo recovery notes.
- `attendee-handout.md` - copy/paste setup and prompts for attendees.
- `demo/` - Python demo package with the main idea-generator CLI and a
  speech-to-text teaser.

## Fastest Way To Present

1. Open a terminal at the repo root.
2. Run:

```powershell
poetry install
```

3. Launch the workshop pages:

```powershell
poetry run workshop-pages
```

4. Make sure your API key is exported when you are ready for the API demo:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

If `OPENAI_API_KEY` is already exported in your shell, you are good. You can
also copy `.env.example` to `.env` as a local fallback.

5. Demo:

```powershell
poetry run hack-idea "vibe coding for hackathons"
poetry run hack-idea "vibe coding for hackathons" --format json
```

The slides include the setup commands, API key note, starter prompt, demo
commands, and a local button-driven API chain for text -> image -> voice, so
the handout is optional during the live workshop.

## Backup Demo

If the network or key is not ready, use the slides and show the scripts. The
talk still works because the core message is the builder loop:

```text
Prompt -> Patch -> Run -> Verify -> Commit
```

## Official Docs Referenced

- OpenAI API Quickstart: https://developers.openai.com/api/docs/quickstart
- Text generation: https://developers.openai.com/api/docs/guides/text
- Image generation: https://developers.openai.com/api/docs/guides/image-generation
- Speech to text: https://developers.openai.com/api/docs/guides/speech-to-text
- Audio and speech: https://developers.openai.com/api/docs/guides/audio
- Realtime: https://developers.openai.com/api/docs/guides/realtime
- Codex Quickstart: https://developers.openai.com/codex/quickstart
