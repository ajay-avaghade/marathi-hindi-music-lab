# marathi-hindi-music-lab
Marathi High enerrgy songs creator
# 🎵 marathi-hindi-music-lab

> A multi-agent AI music production pipeline for raw Maharashtrian-Hindi fusion songs — inspired by Gulabi Sadi, Sanju Rathod, and Ajay-Atul's sound. Built by [@ajay-avaghade](https://github.com/ajay-avaghade).

---

## 🎯 Project Goal

Produce and release a catalogue of original Marathi-Hindi fusion songs using a 4-agent AI pipeline — Lyricist, Composer, Music Director, Singer — with zero upfront cost. Upload to streaming platforms (JioSaavn, Spotify, YouTube Music) and earn royalties.

**Sound reference:** Gulabi Sadi · Shaky (Sanju Rathod) · Dolby Walya (Ajay-Atul)  
**Language mix:** ~60% Marathi · ~40% Hindi  
**Tempo range:** 120–145 BPM  
**Instruments:** Dhol, tumbi, banjo, strings, synth bass

---

## 🤖 The 4-Agent Pipeline

| Agent | Role | Free Tool |
|---|---|---|
| **Lyricist** | Writes mukhda + antara in Marathi-Hindi mix | Claude.ai (free tier) |
| **Composer** | Suggests melody, scale, chord progression | Claude.ai + Gemini (free) |
| **Music Director** | Generates full instrumental track | Suno.ai (free tier) |
| **Singer** | Renders vocal on the melody | Suno.ai vocals / your own voice |

---

## 🗂️ Repository Structure

```
marathi-hindi-music-lab/
│
├── README.md                  ← You are here
├── STYLE_GUIDE.md             ← Sound DNA, language rules, mood palette
├── AGENT_PROMPTS.md           ← Reusable prompts for each agent
├── RELEASE_TRACKER.md         ← Song status, streaming links, revenue log
│
├── songs/
│   └── song-001-template/
│       ├── BRIEF.md           ← Theme, emotion, occasion
│       ├── LYRICS.md          ← Final lyrics (Marathi + Hindi + transliteration)
│       ├── COMPOSITION.md     ← Scale, tempo, chord notes, melody description
│       ├── PRODUCTION.md      ← Suno prompt used, output links, mix notes
│       └── RELEASE.md         ← Cover art link, distributor, streaming URLs
│
├── agent_prompts/
│   ├── lyricist_system.md
│   ├── composer_system.md
│   ├── music_director_system.md
│   └── singer_system.md
│
└── assets/
    └── cover_art/             ← Song cover images (generated via Adobe Firefly free)
```

---

## ⚡ Free Tool Stack (Zero Cost)

| Need | Free Tool | Link |
|---|---|---|
| Lyrics + composition | Claude.ai free tier | claude.ai |
| Lyrics backup | ChatGPT free / Gemini free | gemini.google.com |
| Music generation | Suno.ai free (10 songs/day) | suno.com |
| Music alternative | Udio.com free tier | udio.com |
| Cover art | Adobe Firefly free / Canva free | firefly.adobe.com |
| Distribution | RouteNote (free forever plan) | routenote.com |
| Royalty registration | IPRS India (one-time free) | iprs.org |
| Repo / docs | GitHub free | github.com |

---

## 🚀 How to Make a Song (Quick Steps)

1. Copy `songs/song-001-template/` → rename to `song-002-yourtheme/`
2. Fill `BRIEF.md` (5 mins)
3. Paste brief into Claude → get lyrics → save to `LYRICS.md`
4. Paste lyrics + style guide into Claude → get composition notes → save to `COMPOSITION.md`
5. Use composition notes to craft a Suno prompt → generate track → save link in `PRODUCTION.md`
6. Download best Suno output → upload to RouteNote
7. Update `RELEASE_TRACKER.md` with streaming links

**Total active effort per song: ~2–3 hours**

---

## 🤖 Taking This Further with Antigravity

When Claude credits run low or you want to automate the pipeline end-to-end, use [Antigravity](https://github.com/ajay-avaghade/Antigravity-Resume-Agent) style multi-agent orchestration.

See **[ANTIGRAVITY_HANDOFF.md](./ANTIGRAVITY_HANDOFF.md)** for exact steps.

---

## 📊 Release Tracker

| # | Song Name | Status | Suno Link | Streaming | Revenue |
|---|---|---|---|---|---|
| 001 | — | 🟡 In progress | — | — | — |

---

## 📄 License

All original lyrics and compositions © Ajay Avaghade. AI-generated audio via Suno is subject to [Suno's commercial terms](https://suno.com/terms).
