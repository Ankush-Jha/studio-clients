# studio-clients (private)

Client data for Studio: `clients.json`, `assets/` (photos, logos, footers, `profile.md` standing briefs), `kits/` (built client kits + approved lessons), `library/` (past work, feedback, edits and pending lessons), `jobs/` (text track record of every piece: brief, concepts, script, checks, QA, critique, captions), `evals/` (briefs, spot-check reviews, scorecard history).

Keep this repository private: it holds clients' contact details, licence numbers and photos.

Use it inside the public `studio` repo:

```sh
cd studio
git clone https://github.com/Ankush-Jha/studio-clients.git private
sh setup.sh            # links private/ into place
```

After work, commit and push both repos (`git -C private add -A && git -C private commit -m "..." && git -C private push`), so the track record and everything Studio learned reach the other laptops.
