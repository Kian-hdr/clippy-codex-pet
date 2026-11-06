# Copy-paste setup prompt

Copy the text below into Codex:

```text
Install and select the Clippy pet from Kian-hdr/clippy-codex-pet release v1.0.0.

Download these exact release assets:
https://github.com/Kian-hdr/clippy-codex-pet/releases/download/v1.0.0/Clippy_Codex_Pet_v1.0.0.zip
https://github.com/Kian-hdr/clippy-codex-pet/releases/download/v1.0.0/SHA256SUMS.txt

Verify the ZIP's SHA-256 against the published checksum. Inspect the archive before extracting it; reject absolute paths or parent-directory traversal entries. Read the package's README, ARTWORK_NOTICE.md, and install.py. The character artwork is a non-commercial fan recreation with third-party rights unresolved; do not interpret the code license as a Microsoft character license.

Install the pet files with the installer and Python 3. If the target Codex desktop app is closed, use --select --size 192 to persist selection for the next launch. If this chat is running in the same active Codex app, do not quit the app or edit its on-disk selection behind its live settings store; use the supported pet picker to select Clippy and change its size instead. If that interface is unavailable, finish file installation and give the exact remaining manual selection step, without claiming selection succeeded. Respect my active CODEX_HOME, or use the standard Codex home when it is unset. Preserve other pets, settings, credentials, and unrelated files. If a different clippy pet already exists, preserve it and report the conflict; do not force an overwrite or reset the configuration.

Verify the installed v2 manifest and exact 1536x2288 sprite sheet. Confirm the running Codex instance discovers custom:clippy. Select Clippy through the supported setting or pet picker and verify the visible selection. Reload Codex if required. Do not invent a setting name or claim that copying files proves runtime selection.

Check idle/blink, both movement directions, greeting, jump/celebration, failure, waiting, active work/thinking, review, and all sixteen gaze directions using the supplied previews and the runtime where supported. Report what you actually checked, the Codex version, and anything unavailable.

Use the lossless previews when judging artwork. Native 192-pixel display size can avoid fractional downsampling, but the app may still use pixelated sampling; do not enlarge the fixed-size atlas or patch the app bundle. Finish with the installed location, selected pet ID, validation results, and any rendering limitation.
```
