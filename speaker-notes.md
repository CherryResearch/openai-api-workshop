# Speaker Notes

## Title

Build With The OpenAI API, Codex First

## Audience

Hackathon builders who want to make working AI features quickly. Assume mixed
experience: some Python, some no API experience, lots of product energy.

## Timing

### 0:00-1:30 - Slide 1: The Loop

Say:

"In a hackathon, the hard part is not writing every line by hand. The hard part
is keeping the loop tight enough that you can find the product before time runs
out. The loop is: idea, Codex, Python, run, improve, demo."

Point at the loop on the slide. Keep this crisp.

### 1:30-3:00 - Slide 2: Smallest Useful Python Call

Say:

"The smallest useful OpenAI API app is just a client, a model, an input, and a
response. Everything else is product design around that loop."

Show the Python snippet. Do not overexplain SDK setup.

### 3:00-4:00 - Slide 3: Codex Is The Builder

Say:

"The move is not: memorize every API shape. The move is: ask Codex to build the
smallest working thing, then keep it honest by running it immediately."

Then switch to terminal/editor.

### 4:00-10:00 - Live Demo

Use this prompt in Codex:

```text
Create a Python CLI called hack_idea.py.
It should take a theme argument and call the OpenAI Responses API.
Return a project idea, user story, build steps, and demo script.
Use argparse. Add a helpful error if OPENAI_API_KEY is missing.
```

If using the included package instead of building from scratch:

```powershell
poetry run hack-idea "vibe coding for hackathons"
```

Narration beats:

- "I am asking for behavior, not files."
- "Now I run it. If it fails, that is useful information."
- "Codex can fix errors because we feed it the real error text."
- "Now we make the output structured, because demos need reliability."

Upgrade prompt:

```text
Make the output structured JSON.
Add --format text|json.
Add a README with setup steps.
Run it and fix any errors.
```

### 10:00-12:00 - Slide 4: The API Is Not Just Text

Say:

"Text is the gateway drug, respectfully. But the API also gives you images,
audio, realtime interactions, transcription, and tool calling. For a hackathon,
that means one idea can become a product surface fast."

Use one quick example per tile.

### 12:00-14:00 - Teaser Demo

Show:

```powershell
poetry run transcribe-audio path\to\audio.mp3
```

Do not run unless you have an audio file and time. Say:

"This is the same pattern: a tiny Python wrapper, one API call, then Codex helps
turn it into a product feature."

### 14:00-15:00 - Closing Slide

Say:

"Your job is taste and direction. Codex's job is turning that into running code.
The API is the engine."

End on the reusable prompt.

## Recovery Notes

If `OPENAI_API_KEY` is missing:

- Show the friendly error.
- Say this is why we add guardrails before the demo.

If package install fails:

- Open `demo/hack_idea.py` and explain the code.
- Keep moving; the audience learns more from the loop than from perfect setup.

If the API call is slow:

- Ask: "What should we add next?"
- Use the wait time to explain JSON output and demo reliability.
