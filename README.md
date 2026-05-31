# Codex-First OpenAI API Workshop

A 15-minute hackathon workshop package for showing how to build with the OpenAI
API using Codex as the live coding partner.

## What Is Included

- `slides.html` - polished browser slides with keyboard navigation.
- `speaker-notes.md` - minute-by-minute talk track and demo recovery notes.
- `attendee-handout.md` - copy/paste setup and prompts for attendees.
- `demo/` - Python demo package with the main idea-generator CLI and a
  speech-to-text teaser.

## Fastest Way To Present

1. Open `slides.html` in a browser.
2. Open a terminal in `demo/`.
3. Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
copy .env.example .env
```

4. Put your API key in the terminal:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

5. Demo:

```powershell
hack-idea "vibe coding for hackathons"
hack-idea "vibe coding for hackathons" --format json
```

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

