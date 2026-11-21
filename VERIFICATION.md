# VERIFICATION — the-poster-for-a-place-that-i-2-20261121-0539

## Entry
- Title: **ORVENNA — The Shadow of the Golden Sail**
- Concept followed (live #1 @mellow-ibis-55 "VALDORA — The Chapel of the
  Low Tide", 752021): invented place name in caps + ONE iconic landmark
  subtitle. Differentiator: our own place + landmark + atmosphere — a
  cliffside observatory town above a sea of clouds at dusk (NOT a tidal
  chapel, lantern isles, or tree city).
- Judge brief check: invented place name set big into the picture
  (ORVENNA, 148pt serif, tracked); one landmark (the great observatory
  dome); weather/light promise (setting sun, lamp-lit path, lit windows,
  crescent moon); no invented quotes, star ratings or other copy — only
  the name + the subtitle "THE OBSERVATORY ABOVE THE CLOUDS".
- Image checked at full size by eye (v4): name legible, no distortion,
  fills frame edge-to-edge, no empty bars, close POV on the landmark.

## Artifact
- entry.png: 1024x1024, 342492 bytes (< 1,048,576 cap)
- sha256: 1287448390778cf5eac59d99c7016d01d6149971adf40e33a6ebb0985a9cfedd
- render.py re-run reproduces byte-identical entry.png (fixed seed).
- main.py run twice (OUTPUT_DIR=/tmp/out1, /tmp/out2): byte-identical
  outputs, both pass the pinned size/sha/dimension checks. Runtime ~0.1 s.
- main.py: stdlib only, no network. entry.png is shipped in the repo and
  copied to /output/entry.png (same pattern as news-image-20261121 —
  the sandbox need not have PIL).

## Repo
- Local: ~/workspace/makefun/entries/the-poster-for-a-place-that-i-2-20261121-0539
- Commit: 78be1ffd7af02f43014c82a53cd97c8583a6d6f2 (sarzxy
  <235382442+sarzxy@users.noreply.github.com>, LICENSE MIT + SPDX)
- Planned GitHub repo: sarzxy/the-poster-for-a-place-that-i-2-20261121-0539
  (NOT created yet — no GitHub auth on this VM; coordinator creates it
  via browser and pushes this commit before submit).
- .makefun/owner.json: wallet HDG8gRVVJikqmpVM1LvPMr6ccPqBD6HjZHK939FpoUw5
- README carries the three make.fun badges (competition, rank, reward)
  with the planned repo name; GitHub About (website + topic makefun)
  must be set by the coordinator at repo creation (repo_about check).

## Pre-submit checklist (status at build time)
- [x] Top-1 concept followed + differentiator named (above)
- [x] Read-before-build done (RULES.txt, competition.yaml, BUILDERS.md,
      LESSONS.md judged-image sections)
- [x] Build session began after the competition opened (12:54 WIB;
      opens 12:39 WIB / 05:39 UTC)
- [x] Kit check 2026-11-21 ~13:11 WIB: 13 passed, 1 failed
      (thinking_priced — see coordinator steps), 5 skipped,
      5 checked at submission. license_osi PASS after SPDX line added.
      thinking_reproduces 93.6% (445/475), thinking_in_window PASS,
      transcripts_run_record PASS, thinking_own_work PASS.
- [x] Quota verified via CLI 2026-11-21 ~13:0x WIB:
      `status --competition` → entries_made 0, day cap 10 left (resets
      2026-11-22T00:00Z), can_submit true
- [x] Poster rendered 1024x1024, checked at full size by eye
- [ ] NOT SUBMITTED — image-report-first: Memeg must approve the poster
      first. Submit window 14:39–15:09 WIB, 21 Nov 2026.

## Bundle (STALE — coordinator must rebuild, see below)
- transcripts.tar.gz (this build): 194,217 bytes,
  sha256 edf5be965ea720a75ada14f5398ae8e0795386bad57fe18a4db0dbbe3ce11289
- Made with --session <builder session> --no-discover --mcp none
  --provider meta --model muse-spark-1.3 --effort default
  --prompt-file ~/workspace/makefun/poster-prompt-file.txt
  --prompt-origin scheduled --prompt-via "makefun-quest-watch cron run
  2026-11-21 12:47 WIB spawned the poster builder" + --redact terms
  (Nasar, Memeg, phone, address parts, DOB). Run record complete:
  scheduled prompt, system prompt uploaded, instructions collected (1),
  no MCP servers.
- KNOWN GAP: 0 usage rows (subagent rows are written only once this run
  completes) + parent session not in this bundle. Per skill.md the
  TOP-LEVEL agent re-bundles after the builder finishes.

## COORDINATOR STEPS (before submit, in order)
1. Show entry.png to Memeg; submit ONLY the approved version.
2. Create public GitHub repo sarzxy/the-poster-for-a-place-that-i-2-20261121-0539
   (no GitHub auth on this VM), push HEAD 78be1ff (or the final HEAD
   after this VERIFICATION.md commit), set About: website
   https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539
   + topic makefun. README already carries the three badges.
3. Run the usage SELECT (proven query) with agent ids
   02d36f55-aad3-4414-a469-9d9d6379b7ac (coordinator) AND
   72d46be9-bd7c-4906-9c2f-eaeaff73d9e3 (builder), write rows unchanged
   to ~/.makefun/muse-usage-the-poster-for-a-place-that-i-2-20261121-0539.jsonl:
   SELECT u.agent_id AS agent_id, u.message_id AS message_id,
   u.created_at AS created_at, u.input_tokens AS input_tokens,
   u.output_tokens AS output_tokens, a.model AS model
   FROM agent.agent_message_token_usage u
   JOIN agent.agents a ON a.agent_id = u.agent_id
   WHERE u.agent_id IN ('02d36f55-aad3-4414-a469-9d9d6379b7ac',
   '72d46be9-bd7c-4906-9c2f-eaeaff73d9e3')
   ORDER BY u.created_at DESC LIMIT 500
4. Re-bundle from the top level (takes the parent session too) with
   --muse-usage <file from step 3> + the same flags as above, re-run
   check (thinking_priced must pass), then submit in 14:39–15:09 WIB:
   node cli/makefun.mjs submit --competition
   the-poster-for-a-place-that-i-2-20261121-0539 --repo-url
   https://github.com/sarzxy/the-poster-for-a-place-that-i-2-20261121-0539
   --commit <GitHub HEAD> --title "ORVENNA — The Shadow of the Golden Sail"
   --bundle <rebuilt transcripts.tar.gz>
   --keypair ~/workspace/makefun/makefun-keypair.json
5. Post-submit: status --submission <id> until it leaves "checked".
