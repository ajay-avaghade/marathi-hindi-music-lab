# 🚀 Antigravity Handoff Guide

> When your Claude/ChatGPT free credits run low, this doc tells you exactly how to wire up an autonomous multi-agent pipeline that runs the song factory on its own — same pattern as your Antigravity-Resume-Agent.

---

## What Antigravity Does Here

Instead of you manually copy-pasting between Claude → Suno → GitHub, an Antigravity agent:

1. Reads a song brief from a file (or a simple form)
2. Calls an LLM API (Groq free tier — same as your Resume Agent) to generate lyrics
3. Calls another LLM pass to generate composition notes + Suno prompt
4. Optionally auto-submits to Suno via its API (when available)
5. Saves all outputs to your repo folder structure automatically
6. Updates `RELEASE_TRACKER.md`

---

## Step-by-Step: Building the Agent

### Step 1 — Clone your existing pattern
```bash
git clone https://github.com/ajay-avaghade/Antigravity-Resume-Agent
# Study the multi-agent loop in that repo — same structure applies here
```

### Step 2 — Free LLM API (no cost)
Use **Groq API** — free tier, fast, supports Llama 3.  
Sign up: https://console.groq.com  
You already use this in your Resume Agent. Same API key, same pattern.

```python
from groq import Groq
client = Groq(api_key="YOUR_GROQ_KEY")
```

### Step 3 — Agent definitions (paste these as system prompts)

**Lyricist Agent**
```
You are a Marathi-Hindi fusion lyricist. Style: raw, street, festive — like Sanju Rathod's Gulabi Sadi. 
Write a mukhda (4 lines) and two antaras (6 lines each).
Language: 60% Marathi, 40% Hindi. Use simple words. Include transliteration in brackets.
Output format: JSON with keys: mukhda, antara_1, antara_2, theme, mood.
```

**Composer Agent**
```
You are a Maharashtrian music composer. Given song lyrics, suggest:
- Scale/raga (e.g. Bhairavi, Khamaj, or simple major/minor)
- Tempo (BPM)
- Key instruments: dhol pattern, tumbi riff, string line
- A Suno.ai text prompt (max 200 chars) that captures this arrangement
Output: JSON with keys: scale, bpm, instruments, suno_prompt.
```

**Music Director Agent**
```
You are a music director reviewing a Marathi-Hindi song production.
Given: lyrics, composition notes, and a Suno output description.
Evaluate: Does it match the brief? What to adjust in the next Suno generation?
Output: JSON with keys: score (1-10), feedback, revised_suno_prompt.
```

### Step 4 — Minimal Python orchestrator

```python
# song_factory.py
import json
from groq import Groq

client = Groq(api_key="YOUR_GROQ_KEY")
AGENTS = {
    "lyricist": "...paste lyricist system prompt...",
    "composer": "...paste composer system prompt...",
    "director": "...paste director system prompt..."
}

def run_agent(agent_name, user_message):
    resp = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": AGENTS[agent_name]},
            {"role": "user",   "content": user_message}
        ]
    )
    return json.loads(resp.choices[0].message.content)

def make_song(brief: str):
    print("🎤 Lyricist generating...")
    lyrics = run_agent("lyricist", brief)
    
    print("🎵 Composer arranging...")
    composition = run_agent("composer", json.dumps(lyrics))
    
    print("🎛️ Music Director reviewing...")
    review = run_agent("director", json.dumps({**lyrics, **composition}))
    
    # Save to repo folder
    song_id = "song-XXX"  # auto-increment or UUID
    with open(f"songs/{song_id}/LYRICS.md", "w") as f:
        f.write(str(lyrics))
    with open(f"songs/{song_id}/COMPOSITION.md", "w") as f:
        f.write(str(composition))
    with open(f"songs/{song_id}/PRODUCTION.md", "w") as f:
        f.write(f"Suno prompt: {composition['suno_prompt']}\nDirector score: {review['score']}/10\nFeedback: {review['feedback']}")
    
    print(f"\n✅ Done! Suno prompt ready:\n{composition['suno_prompt']}")
    print(f"Director score: {review['score']}/10")

# Run
make_song("Write a festive Holi song with street energy, joy, colours. Young crowd vibe.")
```

### Step 5 — Run it
```bash
pip install groq
python song_factory.py
```

Paste the Suno prompt output into **suno.com** → download the track → upload to RouteNote. Done.

---

## Cost Breakdown (Full Antigravity Mode)

| Item | Cost |
|---|---|
| Groq API (Llama 3) | Free (generous limits) |
| Suno.ai | Free (10 songs/day) |
| RouteNote distribution | Free forever plan |
| GitHub | Free |
| **Total** | **₹0** |

---

## When to Upgrade (Optional)

Only spend money when you have revenue coming in:
- **Groq paid** → if you're making 20+ songs/month
- **Suno paid ($8/mo)** → for commercial rights + more generations
- **DistroKid ($22/yr)** → if RouteNote's revenue share feels too high

---

## Files the Agent Auto-Creates

```
songs/song-XXX/
├── BRIEF.md        ← your input
├── LYRICS.md       ← lyricist output
├── COMPOSITION.md  ← composer output
└── PRODUCTION.md   ← director review + final Suno prompt
```

Commit with: `git add . && git commit -m "song-XXX: [theme]" && git push`
