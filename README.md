# Offline Speech Recorder & Voice Data Collection Studio

An open-source, browser-based offline voice recorder application designed for community speech dataset collection and acoustic prompt recording. Operates **100% offline** on any laptop in Chrome, Edge, Safari, or Firefox with **zero installation or Python dependencies**.

Directly encodes **16-bit uncompressed PCM WAV audio at 24kHz** via the browser's native Web Audio API, auto-saves recordings persistently in `IndexedDB`, and exports completed datasets into standardized `.zip` packages containing audio files and `metadata.csv`.

---

## 🌟 Key Features

- **100% Offline in Browser:** Runs locally via `index.html`. No terminal setup, no Python, no `pip install sounddevice`.
- **Studio-Quality 24kHz PCM WAV:** Directly encodes float32 audio samples into standard 16-bit mono PCM WAV buffers with proper 44-byte RIFF headers.
- **Prompt Focus View:** Displays sentence prompts one at a time in large, comfortable typography with live progress tracking (`Prompt 14 of 750 • 14 Done`).
- **Paced Workflow:** 3-second countdown before cueing each prompt, with auto-replay preview.
- **Persistent IndexedDB Storage:** Recorded takes are saved locally in the browser's persistent database. Refreshing the page or closing the laptop loses zero takes.
- **One-Click Export:** Exports a clean `.zip` archive containing:
  - `recordings/` folder with all uncompressed `.wav` files.
  - `metadata.csv` manifest (`audio_filename`, `prompt_id`, `sentence`, `duration_seconds`, `timestamp`, `volunteer_id`).

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Spacebar` | Start / Stop recording active prompt |
| `Tab` | Play / Pause recorded take preview |
| `R` | Retake current prompt |
| `Ctrl + Enter` | Mark `[✓ Done]` & advance to next prompt |
| `Alt + Left` | Return to previous prompt |

---

## 📦 Creating Volunteer Packages

Use `package_recorder_volunteers.py` to slice large text prompt datasets into self-contained volunteer bundles:
```bash
python package_recorder_volunteers.py \
    --prompts-file prompts.json \
    --num-volunteers 20 \
    --output-dir recorder_bundles
```

Each volunteer bundle contains:
```
speech-recorder/
├── index.html       # The single-file browser recorder studio (with inlined JSZip)
├── prompts.js       # Pre-loaded prompts for that contributor (window.SPEECH_RECORDER_DATA)
├── prompts.csv      # Standard CSV format of assigned prompts
└── README.md        # Step-by-step contributor instructions
```

---

## 📄 License
MIT License. Open-source speech technology under AfriSpeech.
