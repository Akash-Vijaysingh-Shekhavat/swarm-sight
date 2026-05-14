# SwarmSight — Hackathon Submission Checklist
# Deadline: June 7 (midnight)

---

## 1. Required Deliverables

### □ Deliverable 1 — Project Deck (PDF)
- **Filename:** `[YourTeamName]_Deck.pdf`
- **Format:** PDF only
- **Limit:** Max 10 slides, max 20MB
- **Content:** See `docs/pitch_deck_outline.md` for slide-by-slide content

| Status | Item |
|---|---|
| ✅ Done | Slide content written (`docs/pitch_deck_outline.md`) |
| ✅ Done | Speaker notes included for each slide |
| ⬜ TODO | Create slides in presentation tool (Google Slides / PowerPoint / Canva) |
| ⬜ TODO | Export to PDF and rename to `[YourTeamName]_Deck.pdf` |
| ⬜ TODO | Verify file is under 20MB |

---

### □ Deliverable 2 — Demo Video
- **Format:** MP4
- **Length:** Max 3 minutes
- **Platform:** YouTube (unlisted link)
- **Quality:** Minimum 720p

| Status | Item |
|---|---|
| ⬜ TODO | Record screen demo using SwarmSight with `data/samples/sales_data.csv` |
| ⬜ TODO | Show: upload CSV → set goal → swarm runs → live feed → final report |
| ⬜ TODO | Keep video under 3 minutes (aim for 2:30) |
| ⬜ TODO | Upload to YouTube as **Unlisted** |
| ⬜ TODO | Copy YouTube URL for submission form |

**Suggested demo script:**
1. Open SwarmSight at your Render URL
2. Upload `sales_data.csv`
3. Type goal: *"Find top-performing regions and any anomalous orders"*
4. Click Launch Swarm — narrate the live agent feed as it runs
5. Walk through the report: metrics, key insights, recommendations
6. Download the cleaned CSV
7. Close with the architecture slide (30 seconds)

---

### □ Deliverable 3 — GitHub Repository
- **Visibility:** Must be **public**
- **URL:** https://github.com/Akash-Vijaysingh-Shekhavat/swarm-sight

| Status | Item |
|---|---|
| ✅ Done | Git repo initialized |
| ✅ Done | `.gitignore` created (Python/Streamlit) |
| ✅ Done | `README.md` complete with all 7 required sections |
| ✅ Done | `agents/` folder with all 5 agent stubs |
| ✅ Done | `utils/` folder with schemas, logger, helpers |
| ✅ Done | `data/samples/` with 3 test CSVs |
| ✅ Done | `tests/` with test_agents.py and test_data.py |
| ✅ Done | `docs/` with architecture, pitch deck, checklist |
| ✅ Done | Deployment config (render.yaml, Procfile, runtime.txt) |
| ⬜ TODO | Push all latest changes to GitHub (`git add . && git commit && git push`) |
| ⬜ TODO | Verify repo is **public** (Settings → Change visibility) |
| ⬜ TODO | Confirm README renders correctly on GitHub |
| ⬜ TODO | Fill in all agent `run()` implementations before demo |

---

### □ Deliverable 4 — Prototype Live Link
- **URL:** https://swarm-sight.onrender.com *(replace before submission)*
- **Requirements:** URL must be working, no login required

| Status | Item |
|---|---|
| ⬜ TODO | Deploy to Render.com (connect GitHub repo) |
| ⬜ TODO | Add `ANTHROPIC_API_KEY` in Render environment variables |
| ⬜ TODO | Verify app loads at the live URL |
| ⬜ TODO | Test full pipeline with `sales_data.csv` on the live URL |
| ⬜ TODO | Update README live demo link with actual URL |
| ⬜ TODO | Test in an incognito browser (no login required check) |

---

## 2. What Cowork Cannot Do (Needs Human Action)

These items require you to do them manually:

- 🎥 **Record the demo video** — screen record the live app in action
- 📄 **Export pitch deck to PDF** — build slides from `docs/pitch_deck_outline.md`, export as PDF
- 🚀 **Deploy to Render** — connect your GitHub repo, add the API key, click deploy
- 🔗 **Get the live URL** — copy from Render dashboard after deploy succeeds
- 📹 **Upload video to YouTube** — upload as Unlisted and copy the link
- 💻 **Implement agent `run()` functions** — fill in the 5 agent files in `agents/`
- 🔑 **Add your real API key** — copy `.env.example` to `.env` and add `ANTHROPIC_API_KEY`

---

## 3. Final 3-Day Pre-Submission Schedule

### June 5 (Day 1) — Content Finalization
- [ ] Finish implementing all 5 agent `run()` functions
- [ ] Test full pipeline locally with sample CSVs
- [ ] Run test suite: `python -m pytest tests/ -v`
- [ ] Record demo video (max 3 minutes)
- [ ] Build pitch deck slides from `docs/pitch_deck_outline.md`
- [ ] Export deck to PDF, verify ≤10 slides and ≤20MB

### June 6 (Day 2) — Deployment & Polish
- [ ] Deploy to Render.com (follow README deployment section)
- [ ] Verify live URL works end-to-end
- [ ] Update README live demo link with actual Render URL
- [ ] Upload demo video to YouTube (Unlisted)
- [ ] Final `git add . && git commit -m "Final submission" && git push`
- [ ] Verify GitHub repo is public

### June 7 (Day 3) — Submit
- [ ] Final check: all 4 deliverables ready?
- [ ] Submit on HackerEarth **before midnight**
  - GitHub repo URL
  - Live demo URL
  - YouTube video URL (unlisted)
  - PDF deck (upload file)
- [ ] Confirm submission receipt email

---

## 4. File Naming

| File | Required Name |
|---|---|
| Pitch deck PDF | `[YourTeamName]_Deck.pdf` |
| Demo video | `[YourTeamName]_Demo.mp4` |

Replace `[YourTeamName]` with your actual team name (no spaces — use underscores or camelCase).

Example: `SwarmSight_Deck.pdf` and `SwarmSight_Demo.mp4`

---

## Quick Pre-Submit Sanity Check

Run this before hitting submit:

```bash
# 1. All tests pass?
python -m pytest tests/ -v

# 2. App runs locally?
streamlit run ui/app.py

# 3. Git is up to date?
git status
git log --oneline -5

# 4. Repo is public?
# Check: https://github.com/Akash-Vijaysingh-Shekhavat/swarm-sight
# Settings → Danger Zone → Change visibility → Public
```
