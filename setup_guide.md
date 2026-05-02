# ⚡ Setup Guide — song_factory.py

> From zero to first song in 5 minutes. Free. No Claude Code needed.

---

## Prerequisites

- Python 3.10+ installed (`python3 --version`)
- Git (`git --version`)
- Your repo cloned locally

---

## Step 1 — Get Free Groq API Key (2 mins)

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up (free, no credit card)
3. Click **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)

You already did this for your Antigravity Resume Agent — same key works here.

---

## Step 2 — Clone & Setup (1 min)

```bash
git clone https://github.com/ajay-avaghade/marathi-hindi-music-lab
cd marathi-hindi-music-lab
pip install groq
```

That's the only dependency. No heavy installs.

---

## Step 3 — Set Your API Key

```bash
# Mac/Linux — add to ~/.zshrc or ~/.bashrc for permanence
export GROQ_API_KEY="gsk_your_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY = "gsk_your_key_here"

# Or create a .env file (add .env to .gitignore!)
echo 'GROQ_API_KEY=gsk_your_key_here' > .env
```

---

## Step 4 — Run Your First Song

```bash
# Interactive mode — it asks for the brief
python song_factory.py

# Or pass the brief directly
python song_factory.py --brief "Holi festival, street energy, young crowd, 132 BPM, Pune vibe"

# With more revision attempts (default is 2)
python song_factory.py --brief "your brief" --iterations 3
```

---

## What Happens When You Run It

```
🎵 marathi-hindi-music-lab — Song Factory
   Brief : Holi festival, street energy...
   Output: songs/song-20250502-1430

── Iteration 1 ──────────────────────────────────────
🎤 Agent 1 — Lyricist + Pronunciation Specialist
  → [LYRICIST] using llama3-70b-8192...
  ✓ Saved → songs/song-20250502-1430/01_lyrics.json

🎵 Agent 2 — Composer + Suno Engineer
  → [COMPOSER] using llama3-70b-8192...
  ✓ Saved → songs/song-20250502-1430/02_composition.json

🎛️  Agent 3 — Music Director (9-point QC gate)
  → [DIRECTOR] using llama3-8b-8192...
  ✓ Saved → songs/song-20250502-1430/03_director.json

🎙️  Agent 4 — SUNO (manual step)
  ┌─ Copy this to suno.com/create ──────────────────┐
  │ STYLE : raw male vocals, marathi folk pop, dhol tumbi...
  │ LYRICS: (see 03_director.json → final_suno_lyrics_box)
  └─────────────────────────────────────────────────┘

🎯 Agent 5 — Music Critic
  → [CRITIC] using mixtral-8x7b-32768...
  ✓ Saved → songs/song-20250502-1430/05_critic.json

👥 Agent 6 — Fan Jury
  → [FAN_JURY] using mixtral-8x7b-32768...
  ✓ Saved → songs/song-20250502-1430/06_fan_jury.json

📱 Agent 7 — Social Media Strategist
  → [SOCIAL] using mixtral-8x7b-32768...
  ✓ Saved → songs/song-20250502-1430/07_social.json

╔══════════════════════════════════════════════════════╗
  SONG REPORT — होळी रंगात रंगले
╚══════════════════════════════════════════════════════╝
  Director  : 8/10  [release_ready]
  Critic    : 7.5/10  — "A dhol-driven Holi anthem..."
  Fan jury  : 7.2/10  [high viral potential]
  Virality  : 8/10   [regional (10k-1L)]

  RELEASE GATE: ✅ PASSED

✅ All gates passed. Paste Suno boxes → download → RouteNote.
  ✓ RELEASE_TRACKER.md updated
```

---

## Output Files Per Song

```
songs/song-20250502-1430/
├── 01_lyrics.json          ← Full lyrics + transliteration + pronunciation fixes
├── 02_composition.json     ← Scale, BPM, instruments, Suno style box
├── 03_director.json        ← QC gate scores + FINAL Suno style+lyrics boxes ← USE THIS
├── 05_critic.json          ← Critical review with scores
├── 06_fan_jury.json        ← 5 fan reactions + consensus score
├── 07_social.json          ← Reel hook, hashtags, platform strategy
└── SUMMARY.json            ← Everything in one place + release gate result
```

---

## After the Script — Manual Steps

### Agent 4: Suno (1 min)
1. Open [suno.com/create](https://suno.com/create)
2. Open `03_director.json` → copy `final_suno_style_box` → paste into **Style** field
3. Copy `final_suno_lyrics_box` → paste into **Lyrics** field
4. Generate 2 versions → pick best → download MP3/WAV

### Distribution (5 mins)
1. Upload to [routenote.com](https://routenote.com) (free)
2. Select: Spotify, JioSaavn, Gaana, Apple Music, YouTube Music
3. Upload cover art (Adobe Firefly free → 25 credits/month)
4. Update `RELEASE_TRACKER.md` with the streaming links

---

## Common Issues

**`ModuleNotFoundError: No module named 'groq'`**
```bash
pip install groq
```

**`JSON parse error`** — model returned non-JSON
```bash
# Run again — LLMs occasionally break format. Happens <5% of the time.
python song_factory.py --brief "your brief"
```

**Gate fails repeatedly**
```bash
# Check which agent is scoring low
cat songs/song-XXX/SUMMARY.json

# Try with more iterations
python song_factory.py --brief "your brief" --iterations 3
```

**GROQ_API_KEY not found**
```bash
export GROQ_API_KEY="gsk_your_key_here"
# Then run again in the same terminal
```

---

## Adding .env Support (Optional)

```bash
pip install python-dotenv
```

Then add at the top of `song_factory.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Cost

| Component | Cost |
|---|---|
| Groq API (Llama 3 70B + Mixtral) | **Free** (generous daily limits) |
| Suno.ai | **Free** (10 songs/day) |
| RouteNote distribution | **Free** (85% revenue to you) |
| **Total per song** | **₹0** |
