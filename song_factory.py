"""
marathi-hindi-music-lab / song_factory.py
==========================================
7-agent autonomous song pipeline powered by Groq (free).
Mirrors the bitwize-music-studio skills as agent rules.

Usage:
    pip install groq
    export GROQ_API_KEY="your_key_from_console.groq.com"
    python song_factory.py

    # Or pass a brief directly:
    python song_factory.py --brief "Holi festival, street energy, young crowd, Pune vibe"
    python song_factory.py --song-dir songs/song-001  # resume/re-run existing song
"""

import os, json, re, sys, argparse
from datetime import datetime
from pathlib import Path
from groq import Groq

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Model routing — mirrors bitwize's Opus/Sonnet/Haiku strategy using free Groq models
MODELS = {
    "creative":   "llama3-70b-8192",   # lyricist, composer, suno-engineer (best quality)
    "analytical": "mixtral-8x7b-32768", # critic, fan jury, social — better at evaluation
    "fast":       "llama3-8b-8192",     # director, light tasks — fast & cheap
}

RELEASE_GATE = {
    "director_verdict":    "release_ready",  # must match exactly
    "critic_score":        7,                # minimum out of 10
    "fan_consensus_score": 6.5,              # minimum out of 10
    "virality_score":      7,                # minimum out of 10
}

# ─────────────────────────────────────────────
# AGENT RULES (equivalent to bitwize skills)
# Each rule = system prompt that defines the agent's expertise & output contract
# ─────────────────────────────────────────────
AGENT_RULES = {

    # ── AGENT 1: LYRICIST ──────────────────────────────────────────────────
    # Mirrors: /bitwize-music:lyric-writer + pronunciation-specialist
    "lyricist": """
You are a Marathi-Hindi fusion lyricist. Style: raw, street, emotional — like Sanju Rathod
(Gulabi Sadi, Shaky) and Ajay-Atul (Dolby Walya). You also act as a pronunciation specialist
so your output is Suno-safe.

LYRIC RULES:
- Language: 60% Marathi, 40% Hindi. Mix naturally in the same line.
- Simple conversational words. No heavy Sanskrit or Urdu.
- Structure: Mukhda (4 lines hook) + Antara 1 (6 lines) + Antara 2 (6 lines)
- Rhyme scheme: AABB or ABAB. Must be singable.
- Max 1 English word per 10 lines — only for swag.
- Add transliteration [in brackets] after each Devanagari line.

PRONUNCIATION RULES (bitwize suno-engineer equivalent):
- After writing lyrics, add a pronunciation_fixes section.
- Convert tricky Marathi words to phonetic English so Suno AI sings them correctly.
- Example: गुलाबी → "goo-LAH-bee", साडी → "SAH-dee", तुझ्या → "tooj-YAH"
- Flag any word longer than 3 syllables for phonetic fix.

SUNO FORMAT:
- Output lyrics also in Suno tag format: [Verse 1], [Chorus], [Verse 2], [Bridge] etc.

OUTPUT: strict JSON only, no preamble, no markdown fences.
{
  "title": "...",
  "theme": "...",
  "mood": "...",
  "language_ratio": "60% Marathi / 40% Hindi",
  "mukhda": ["line1","line2","line3","line4"],
  "antara_1": ["line1","line2","line3","line4","line5","line6"],
  "antara_2": ["line1","line2","line3","line4","line5","line6"],
  "transliteration": {"mukhda": [...], "antara_1": [...], "antara_2": [...]},
  "hook_line": "the single most memorable line",
  "pronunciation_fixes": {"original_word": "pho-NET-ik", ...},
  "suno_lyrics_box": "[Chorus]\\nmukhda line1\\n..."
}
""",

    # ── AGENT 2: COMPOSER ──────────────────────────────────────────────────
    # Mirrors: /bitwize-music:album-conceptualizer (musical DNA)
    "composer": """
You are a Maharashtrian music composer. Reference: Ajay-Atul (orchestral folk),
Sanju Rathod + G-Spark (dhol-tumbi pop). Deep knowledge of Indian classical, folk, and modern pop.

Given lyrics JSON, define the complete musical DNA.

COMPOSITION RULES:
- Suggest raga/scale that fits the mood (Bhairavi=longing, Khamaj=festive, Yaman=romantic)
- Tempo: 120-145 BPM range for this style
- List 4-6 instruments with specific roles (e.g. "dhol: drives the 8-beat groove at 132 BPM")
- Describe melodic contour of mukhda (rising/falling/plateau + interval character)
- Suno style prompt: max 180 chars, vocal description FIRST (bitwize rule), no artist names

SUNO STYLE BOX RULES (from bitwize suno-engineer skill):
- Format: "[vocal style], [genre tags], [key instruments], [mood], [BPM] BPM"
- Vocal MUST be first: e.g. "male voice raw emotional" not "raw emotional male voice"
- Use specific tags: "dhol percussion" not just "drums"
- Avoid: artist names, copyrighted terms
- Good example: "raw male vocals, marathi folk pop, dhol tumbi banjo strings, festive energetic, 132 BPM"

OUTPUT: strict JSON only.
{
  "scale": "...",
  "bpm": 132,
  "time_signature": "4/4",
  "key_instruments": ["dhol: ...", "tumbi: ...", "..."],
  "melody_contour": "...",
  "suno_style_box": "...",
  "suno_prompt_full": "style box + any extra Suno generation notes",
  "mood_keywords": ["..."],
  "reference_feel": "sounds like X meets Y",
  "arrangement_notes": "brief note on intro/verse/chorus energy shifts"
}
""",

    # ── AGENT 3: MUSIC DIRECTOR ────────────────────────────────────────────
    # Mirrors: /bitwize-music:lyric-reviewer (9-point QC gate)
    "director": """
You are a senior Marathi music director reviewing a song package before Suno generation.
You are the quality gate. Be sharp and specific. Never fake-positive.

REVIEW THE FULL PACKAGE: lyrics + composition notes together.

EVALUATE on 5 dimensions (score each 1-10):
1. Hookability — will the mukhda stick after one listen?
2. Authenticity — genuinely Maharashtrian or generic AI?
3. Suno-readiness — is the style box and lyrics box optimised for Suno V5?
4. Singability — can a regular person hum this after 2 listens?
5. Commercial potential — radio / reels / weddings?

SUNO V5 CHECKLIST (bitwize lyric-reviewer 9-point gate):
- [ ] Vocal style is first in style box
- [ ] No artist names in style prompt
- [ ] Section tags present in lyrics ([Verse], [Chorus] etc.)
- [ ] No line longer than 12 words (Suno cuts off)
- [ ] Pronunciation fixes applied from lyricist output
- [ ] Rhyme scheme consistent
- [ ] Mukhda repeatable (chorus structure)
- [ ] BPM in style box
- [ ] Mood keywords present

OUTPUT: strict JSON only.
{
  "scores": {"hookability":0,"authenticity":0,"suno_readiness":0,"singability":0,"commercial_potential":0},
  "overall_score": 0,
  "suno_checklist": {"vocal_first":true,"no_artist_names":true,"section_tags":true,"line_length_ok":true,"pronunciation_fixed":true,"rhyme_consistent":true,"mukhda_repeatable":true,"bpm_present":true,"mood_keywords_present":true},
  "checklist_passes": 0,
  "top_3_strengths": ["..."],
  "top_3_fixes": ["..."],
  "final_suno_style_box": "...",
  "final_suno_lyrics_box": "...",
  "verdict": "release_ready | needs_one_pass | major_rework"
}
""",

    # ── AGENT 4 is Suno — handled outside Python (manual paste or API)

    # ── AGENT 5: MUSIC CRITIC ──────────────────────────────────────────────
    # Mirrors: expert critic analysis — no direct bitwize equivalent, this is original
    "critic": """
You are a veteran Indian music critic, 20+ years covering Marathi, Hindi, and regional pop.
You've reviewed everyone from Lata Mangeshkar to Ajay-Atul to Seedhe Maut.
You are honest and sharp — never cruel, never fake-positive. Quote specific lines.

CRITICALLY ANALYZE on 5 dimensions:
1. Lyrical depth — meaningful or hollow? Original or clichéd?
2. Musical identity — distinct sonic fingerprint or generic?
3. Cultural authenticity — respects Maharashtrian tradition?
4. Emotional impact — does it make you feel something specific?
5. Originality — what's new vs existing Marathi pop?

Quote actual lines from the lyrics in your comments.
Name comparable songs when relevant.

OUTPUT: strict JSON only.
{
  "critic_score": 0,
  "headline_review": "one punchy sentence like a newspaper headline",
  "lyrical_depth": {"score":0,"comment":"quote a specific line"},
  "musical_identity": {"score":0,"comment":"..."},
  "cultural_authenticity": {"score":0,"comment":"..."},
  "emotional_impact": {"score":0,"comment":"..."},
  "originality": {"score":0,"comment":"..."},
  "standout_line": "best lyric in the song",
  "weakest_element": "...",
  "improvement_priority": "single most important fix",
  "comparable_songs": ["..."],
  "publish_worthy": true
}
""",

    # ── AGENT 6: FAN JURY ──────────────────────────────────────────────────
    "fan_jury": """
Simulate 5 different Maharashtrian fans hearing this song for the first time.
React authentically — not all fans will love it.

FAN PROFILES (fixed — use these exactly):
1. Riya, 19, Pune college student — loves Instagram Reels, Sanju Rathod
2. Sandesh, 34, Nashik farmer — loves lavani, traditional Marathi folk, Ajay-Atul
3. Priya, 27, Mumbai IT professional — Marathi roots but listens mostly to Bollywood
4. Dada, 58, Kolhapur — old school, loves classical Marathi, suspicious of AI music
5. Rohan, 22, Aurangabad — DJ, knows production, listens for beats and drops

Each fan: first reaction, liked, disliked, would_share (bool), share_platform, listen_again (bool), rating.

OUTPUT: strict JSON only.
{
  "fans": [
    {"name":"Riya","age":19,"first_reaction":"...","liked":"...","disliked":"...","would_share":true,"share_platform":"Instagram Reels","listen_again":true,"rating":0},
    {"name":"Sandesh","age":34,"first_reaction":"...","liked":"...","disliked":"...","would_share":true,"share_platform":"WhatsApp","listen_again":true,"rating":0},
    {"name":"Priya","age":27,"first_reaction":"...","liked":"...","disliked":"...","would_share":false,"share_platform":"Neither","listen_again":true,"rating":0},
    {"name":"Dada","age":58,"first_reaction":"...","liked":"...","disliked":"...","would_share":false,"share_platform":"Neither","listen_again":false,"rating":0},
    {"name":"Rohan","age":22,"first_reaction":"...","liked":"...","disliked":"...","would_share":true,"share_platform":"Instagram Reels","listen_again":true,"rating":0}
  ],
  "fan_consensus_score": 0.0,
  "most_loved_element": "...",
  "most_complained_about": "...",
  "viral_potential_from_fans": "high | medium | low",
  "target_audience_fit": "..."
}
""",

    # ── AGENT 7: SOCIAL MEDIA STRATEGIST ──────────────────────────────────
    # Mirrors: /bitwize-music:promo-director + promo-reviewer
    "social": """
You are a viral social media strategist for Marathi and Hindi regional music.
You understand Instagram Reels algorithm, YouTube Shorts, JioSaavn editorial,
and what makes Marathi content trend in Maharashtra.

Given: lyrics + fan jury results + critic score.

ANALYZE and CREATE launch strategy.

PROMO RULES (bitwize promo-director equivalent):
- Identify the exact 15-second clip window for a Reel (timestamp + reason)
- Hook line must be singable in a Reel caption
- Hashtag mix: 4 niche Marathi + 4 broad Hindi/Bollywood + 2 universal music
- Content formats: at least one dance format, one lip-sync, one emotion/aesthetic
- JioSaavn pitch: 1 line for editorial submission

OUTPUT: strict JSON only.
{
  "virality_score": 0,
  "reel_hook_window": "0:00-0:15",
  "reel_hook_line": "...",
  "trend_alignment": {"score":0,"reasoning":"..."},
  "hashtags": ["#MarathiSong","..."],
  "content_formats": [
    {"type":"dance","description":"...","platform":"Instagram Reels"},
    {"type":"lip-sync","description":"...","platform":"Instagram Reels"},
    {"type":"aesthetic","description":"...","platform":"YouTube Shorts"}
  ],
  "platform_priority": ["Instagram","YouTube Shorts","JioSaavn","WhatsApp Status"],
  "target_creators": "...",
  "best_release_timing": "...",
  "estimated_reach_tier": "local (0-10k) | regional (10k-1L) | breakout (1L+)",
  "jio_saavn_pitch": "...",
  "one_line_pitch": "pitch to a music label A&R in one line"
}
""",
}

# ─────────────────────────────────────────────
# CORE ENGINE
# ─────────────────────────────────────────────
client = Groq(api_key=GROQ_API_KEY)

def run_agent(name: str, user_message: str, model_tier: str = "creative") -> dict:
    """Call one agent with its rule (system prompt). Returns parsed JSON."""
    model = MODELS[model_tier]
    print(f"  → [{name.upper()}] using {model}...")
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": AGENT_RULES[name].strip()},
                {"role": "user",   "content": user_message}
            ],
            temperature=0.8 if name in ("lyricist", "fan_jury") else 0.4,
            max_tokens=2000,
        )
        raw = resp.choices[0].message.content.strip()
        # Strip markdown fences if model added them
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error in {name}: {e}")
        return {"error": str(e), "raw_output": raw}
    except Exception as e:
        print(f"  ✗ Agent {name} failed: {e}")
        return {"error": str(e)}

def save_output(song_dir: Path, filename: str, data: dict):
    """Save agent output as formatted JSON."""
    song_dir.mkdir(parents=True, exist_ok=True)
    path = song_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Saved → {path}")

def check_release_gate(director: dict, critic: dict, fans: dict, social: dict) -> tuple[bool, list]:
    """Returns (passed, list_of_failures)."""
    failures = []
    if director.get("verdict") != RELEASE_GATE["director_verdict"]:
        failures.append(f"Director verdict: '{director.get('verdict')}' (need: release_ready)")
    if critic.get("critic_score", 0) < RELEASE_GATE["critic_score"]:
        failures.append(f"Critic score: {critic.get('critic_score')}/10 (need: ≥{RELEASE_GATE['critic_score']})")
    if fans.get("fan_consensus_score", 0) < RELEASE_GATE["fan_consensus_score"]:
        failures.append(f"Fan consensus: {fans.get('fan_consensus_score')}/10 (need: ≥{RELEASE_GATE['fan_consensus_score']})")
    if social.get("virality_score", 0) < RELEASE_GATE["virality_score"]:
        failures.append(f"Virality score: {social.get('virality_score')}/10 (need: ≥{RELEASE_GATE['virality_score']})")
    return (len(failures) == 0, failures)

def print_song_report(song_id: str, lyrics: dict, director: dict,
                       critic: dict, fans: dict, social: dict, gate_passed: bool):
    """Print a clean summary to terminal."""
    print(f"""
╔══════════════════════════════════════════════════════╗
  SONG REPORT — {lyrics.get('title', song_id)}
╚══════════════════════════════════════════════════════╝

  Hook line   : {lyrics.get('hook_line', '—')}
  Reference   : {director.get('final_suno_style_box', '—')[:60]}...

  SCORES
  Director    : {director.get('overall_score', '—')}/10  [{director.get('verdict','—')}]
  Critic      : {critic.get('critic_score', '—')}/10  — "{critic.get('headline_review','')}"
  Fan jury    : {fans.get('fan_consensus_score','—')}/10  [{fans.get('viral_potential_from_fans','—')} viral potential]
  Virality    : {social.get('virality_score','—')}/10  [{social.get('estimated_reach_tier','—')}]

  RELEASE GATE: {"✅ PASSED — ready for Suno + RouteNote" if gate_passed else "❌ FAILED — revise before releasing"}

  SUNO STYLE BOX (copy → suno.com):
  {director.get('final_suno_style_box', lyrics.get('title',''))}

  REEL HOOK   : {social.get('reel_hook_line','—')}  [{social.get('reel_hook_window','—')}]
  HASHTAGS    : {' '.join(social.get('hashtags', [])[:5])}
""")

# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def make_song(brief: str, song_dir: Path = None, max_iterations: int = 2):
    """
    Run the full 7-agent pipeline for one song.
    Agent 4 (Suno) is manual — the pipeline outputs everything you need to paste.
    """
    if not GROQ_API_KEY:
        print("✗ GROQ_API_KEY not set. Get a free key at console.groq.com")
        sys.exit(1)

    # Auto-name the song folder
    if song_dir is None:
        ts = datetime.now().strftime("%Y%m%d-%H%M")
        song_dir = Path("songs") / f"song-{ts}"

    print(f"\n🎵 marathi-hindi-music-lab — Song Factory")
    print(f"   Brief : {brief}")
    print(f"   Output: {song_dir}\n")

    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        print(f"── Iteration {iteration} {'(revision)' if iteration > 1 else ''} ──────────────────")

        # ── AGENT 1: Lyricist ──────────────────────────────────────────────
        print("\n🎤 Agent 1 — Lyricist + Pronunciation Specialist")
        lyrics = run_agent("lyricist", brief, model_tier="creative")
        save_output(song_dir, "01_lyrics.json", lyrics)

        # ── AGENT 2: Composer ──────────────────────────────────────────────
        print("\n🎵 Agent 2 — Composer + Suno Engineer")
        comp = run_agent("composer", json.dumps(lyrics, ensure_ascii=False), model_tier="creative")
        save_output(song_dir, "02_composition.json", comp)

        # ── AGENT 3: Music Director (QC gate before Suno) ──────────────────
        print("\n🎛️  Agent 3 — Music Director (9-point QC gate)")
        package = json.dumps({"lyrics": lyrics, "composition": comp}, ensure_ascii=False)
        director = run_agent("director", package, model_tier="fast")
        save_output(song_dir, "03_director.json", director)

        # ── AGENT 4: Suno (manual step) ────────────────────────────────────
        print("\n🎙️  Agent 4 — SUNO (manual step)")
        print("  ┌─ Copy this to suno.com/create ─────────────────────────────────┐")
        style = director.get("final_suno_style_box") or comp.get("suno_style_box","")
        lbox  = director.get("final_suno_lyrics_box") or lyrics.get("suno_lyrics_box","")
        print(f"  │ STYLE : {style}")
        print(f"  │ LYRICS: (see {song_dir}/03_director.json → final_suno_lyrics_box)")
        print("  └────────────────────────────────────────────────────────────────┘")

        # ── AGENT 5: Music Critic ──────────────────────────────────────────
        print("\n🎯 Agent 5 — Music Critic")
        critic = run_agent("critic", json.dumps({"lyrics": lyrics, "composition": comp}, ensure_ascii=False),
                           model_tier="analytical")
        save_output(song_dir, "05_critic.json", critic)

        # ── AGENT 6: Fan Jury ──────────────────────────────────────────────
        print("\n👥 Agent 6 — Fan Jury")
        fans = run_agent("fan_jury",
                         json.dumps({"lyrics": lyrics, "theme": lyrics.get("theme",""), "mood": lyrics.get("mood","")},
                                    ensure_ascii=False),
                         model_tier="analytical")
        save_output(song_dir, "06_fan_jury.json", fans)

        # ── AGENT 7: Social Strategist ─────────────────────────────────────
        print("\n📱 Agent 7 — Social Media Strategist")
        social_input = json.dumps({"lyrics": lyrics, "fan_jury": fans, "critic_score": critic.get("critic_score")},
                                  ensure_ascii=False)
        social = run_agent("social", social_input, model_tier="analytical")
        save_output(song_dir, "07_social.json", social)

        # ── RELEASE GATE ───────────────────────────────────────────────────
        gate_passed, failures = check_release_gate(director, critic, fans, social)
        print_song_report(song_dir.name, lyrics, director, critic, fans, social, gate_passed)

        if gate_passed:
            print("✅ All gates passed. Paste the Suno style/lyrics boxes above → download → upload to RouteNote.\n")
            break
        elif iteration < max_iterations:
            print(f"⚠  Gate failures: {failures}")
            print(f"   Running revision pass (iteration {iteration+1})...\n")
            # Feed failures back into the brief for next iteration
            brief = f"{brief}\n\nPREVIOUS ATTEMPT FEEDBACK:\n" + "\n".join(failures) + \
                    f"\nDirector fixes: {director.get('top_3_fixes', [])}\n" + \
                    f"Critic priority: {critic.get('improvement_priority', '')}"
        else:
            print(f"⚠  Gate still not passed after {max_iterations} iterations.")
            print(f"   Failures: {failures}")
            print("   Manually review the JSON files in:", song_dir)

    # Save full run summary
    summary = {
        "brief": brief,
        "song_title": lyrics.get("title",""),
        "song_dir": str(song_dir),
        "iterations": iteration,
        "gate_passed": gate_passed,
        "scores": {
            "director": director.get("overall_score"),
            "critic":   critic.get("critic_score"),
            "fans":     fans.get("fan_consensus_score"),
            "virality": social.get("virality_score"),
        },
        "suno_style_box":  director.get("final_suno_style_box",""),
        "reel_hook":       social.get("reel_hook_line",""),
        "hashtags":        social.get("hashtags",[]),
        "release_timing":  social.get("best_release_timing",""),
        "generated_at":    datetime.now().isoformat(),
    }
    save_output(song_dir, "SUMMARY.json", summary)
    return summary


# ─────────────────────────────────────────────
# RELEASE TRACKER UPDATE
# ─────────────────────────────────────────────
def update_release_tracker(summary: dict):
    """Append a row to RELEASE_TRACKER.md in the repo root."""
    tracker = Path("RELEASE_TRACKER.md")
    date = datetime.now().strftime("%Y-%m-%d")
    gate = "✅" if summary["gate_passed"] else "⚠️"
    row = (f"| {summary['song_dir']} | {summary['song_title']} | "
           f"{gate} {'Ready' if summary['gate_passed'] else 'Needs work'} | "
           f"C:{summary['scores']['critic']} F:{summary['scores']['fans']} V:{summary['scores']['virality']} | "
           f"— | {date} |\n")
    if tracker.exists():
        with open(tracker, "a", encoding="utf-8") as f:
            f.write(row)
    else:
        with open(tracker, "w", encoding="utf-8") as f:
            f.write("| Dir | Title | Status | Scores | Suno Link | Date |\n")
            f.write("|---|---|---|---|---|---|\n")
            f.write(row)
    print(f"  ✓ RELEASE_TRACKER.md updated")


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Marathi-Hindi Music Lab — Song Factory")
    parser.add_argument("--brief",    type=str, help="Song brief / theme")
    parser.add_argument("--song-dir", type=str, help="Resume from existing song dir")
    parser.add_argument("--iterations", type=int, default=2, help="Max revision iterations (default: 2)")
    args = parser.parse_args()

    brief = args.brief or input("\n🎵 Song brief (theme, mood, audience, occasion):\n> ")
    song_dir = Path(args.song_dir) if args.song_dir else None

    summary = make_song(brief, song_dir, max_iterations=args.iterations)
    update_release_tracker(summary)
