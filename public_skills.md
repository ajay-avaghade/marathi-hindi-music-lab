# 🔧 Public Skills & Tools You Can Leverage — Zero Cost

> Curated specifically for this pipeline. All free. All public. All battle-tested.

---

## 1. 🎵 Suno MCP — Direct API Access from Claude/Code

**Repo:** [AceDataCloud/SunoMCP](https://github.com/AceDataCloud/SunoMCP) ⭐ Top pick  
**What it does:** Lets Claude Code (or your Antigravity script) call Suno directly — generate music, extend songs, separate stems, get lyrics timing — without manually opening the browser.  
**Free tier:** AceDataCloud has a free API token.  
**Setup (3 commands):**
```bash
pip install mcp-suno
export ACEDATACLOUD_API_TOKEN="your_token_here"
mcp-suno
```
**Why it matters:** Your Agent 4 (Singer) becomes fully automated. Brief → lyrics → Suno track, all in one Python run.

---

## 2. 🎵 gcui-art/suno-api — Self-hostable Suno Wrapper

**Repo:** [gcui-art/suno-api](https://github.com/gcui-art/suno-api) ⭐ 1.8k stars  
**What it does:** Wraps Suno's web interface as an OpenAI-compatible API. Works with your existing Groq/OpenAI-style code patterns. Deploy free on Vercel.  
**Best for:** When you want to chain Suno generation inside your Antigravity Python script without manual copy-paste.  
**One-click Vercel deploy:** Available in the repo README.

---

## 3. 🎸 bitwize-music-studio/claude-ai-music-skills — Full Production Skillset

**Repo:** [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills)  
**What it does:** 51 pre-built Claude Code skills for music production — lyric writing with prosody rules, Suno prompt optimization, audio mastering, album concept planning. Has **72 genre guides** and a Python MCP server with 80+ tools.  
**Key skills to steal:**
- `lyric-writer` skill — has rhyme detection, syllable counting, section validation
- Suno prompt optimizer — improves your Agent 2 output before sending to Suno
- Audio mastering tool — makes downloaded Suno MP3s streaming-ready  
**Install:** `claude mcp add bitwize-music-studio/claude-ai-music-skills`

---

## 4. 🤖 Groq API — Free LLM for Antigravity Automation

**Site:** [console.groq.com](https://console.groq.com) — you already use this!  
**Free tier:** Very generous — Llama 3 70B, Gemma, Mixtral.  
**Why it matters:** Powers all 7 agents in your Antigravity script at zero cost.  
**Best model for this:** `llama3-70b-8192` — best balance of creativity + instruction following.  
**Tip:** Use `mixtral-8x7b-32768` for Agent 5 (Critic) — better at nuanced evaluation.

---

## 5. 🎤 Bark by Suno-AI — Free Local TTS / Vocal Synthesis

**Repo:** [suno-ai/bark](https://github.com/suno-ai/bark) ⭐ 39k stars  
**What it does:** Open-source text-to-audio model. Can generate singing-adjacent vocals, humming, and voice with emotion. Runs locally (free forever).  
**Use case:** Rapid vocal prototyping before you commit to a full Suno generation. Test how the mukhda sounds before spending a Suno credit.  
**Note:** Needs GPU for speed; CPU is slow but works.

---

## 6. 🎨 Adobe Firefly — Free Cover Art Generation

**Site:** [firefly.adobe.com](https://firefly.adobe.com)  
**Free tier:** 25 generative credits/month.  
**Why it beats Midjourney (for you):** Firefly images are commercially safe — important when uploading to streaming platforms. No copyright disputes.  
**Prompt style for Marathi covers:** `"Vibrant Maharashtrian woman in gulabi (pink) sadi, festive street background, bokeh lights, cinematic, Bollywood poster style"`

---

## 7. 🚀 RouteNote — Free Music Distribution

**Site:** [routenote.com](https://routenote.com)  
**Free plan:** Upload unlimited songs to Spotify, JioSaavn, Gaana, Apple Music, YouTube Music.  
**Revenue split:** RouteNote keeps 15%, you keep 85%.  
**Why not DistroKid:** DistroKid charges $22/year. RouteNote is free until you're earning.  
**Upgrade trigger:** When monthly streams > 50k, consider DistroKid for 100% revenue.

---

## 8. 📊 Soundcharts Free Tier — Trend Monitoring

**Site:** [soundcharts.com](https://soundcharts.com)  
**Free tier:** Basic chart tracking for Spotify, YouTube, Apple Music.  
**Use case:** Feed data to Agent 7 (Social Strategist) — "this type of song is trending on JioSaavn this week" as context in the prompt.

---

## 9. 🎬 CapCut Free — Reel Video Creation

**Site/App:** CapCut (free)  
**Why:** Auto-generates lyric videos and Reels from an audio file in minutes. Has Marathi font support. Agent 7's content strategy comes to life here — zero video editing skill needed.

---

## 10. 📋 n8n + MuAPI — Workflow Automation (Advanced)

**Repo:** [n8n community nodes for MuAPI](https://github.com/topics/suno) — search "muapi n8n"  
**What it does:** Visual workflow automation (like Zapier, but free self-hosted). Connect: song brief form → Groq API → Suno → save to GitHub → post to Instagram — all automatically.  
**Free:** Self-host on any VPS or even your local machine.  
**When to use:** After your first 5 songs are done manually. This is your full factory automation.

---

## Summary: Your Stack by Phase

| Phase | Tools |
|---|---|
| **Now (free, manual)** | Claude.ai free + Suno.com + RouteNote + GitHub + CapCut |
| **Antigravity (free, automated)** | Groq API + gcui-art/suno-api + bitwize-music-skills + GitHub Actions |
| **Scale (still mostly free)** | n8n + MuAPI + Soundcharts + Adobe Firefly |
| **Revenue reinvestment** | Suno paid ($8/mo) + DistroKid ($22/yr) |

**Total cost at every phase except the last: ₹0**
