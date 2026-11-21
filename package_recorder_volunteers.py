#!/usr/bin/env python3
"""Open-source Prompt Slicing & Volunteer Workspace Packaging Utility.

Splits large text prompt corpora into ready-to-use, zero-installation offline recorder apps.
"""

import os
import io
import csv
import json
import zipfile
import argparse
from pathlib import Path

def package_prompts(
    prompts_file: Path,
    recorder_html: Path,
    output_dir: Path,
    num_volunteers: int = 4,
    project_name: str = "Speech Recording Project",
    submission_email: str = "contributions@example.org"
):
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(prompts_file, "r", encoding="utf-8") as f:
        all_prompts = json.load(f)

    total_prompts = len(all_prompts)
    part_size = total_prompts // num_volunteers

    print(f"Project: {project_name}")
    print(f"Total Prompts: {total_prompts:,}")
    print(f"Splitting into {num_volunteers} parts of ~{part_size:,} prompts each...\n")

    with open(recorder_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    for v_idx in range(1, num_volunteers + 1):
        vol_id = f"contributor_{v_idx:02d}"
        vol_name = f"Contributor {v_idx:02d}"
        start_i = (v_idx - 1) * part_size
        end_i = v_idx * part_size if v_idx < num_volunteers else total_prompts
        vol_prompts = all_prompts[start_i:end_i]

        zip_filename = f"recorder_{vol_id}.zip"
        zip_out = output_dir / zip_filename

        # 1. prompts.js
        prompts_js = (
            f"window.SPEECH_RECORDER_DATA = {{\n"
            f"  title: {json.dumps(project_name)},\n"
            f"  volunteer_id: {json.dumps(vol_id)},\n"
            f"  total_prompts: {len(vol_prompts)},\n"
            f"  submission_email: {json.dumps(submission_email)},\n"
            f"  prompts: {json.dumps(vol_prompts, indent=2)}\n"
            f"}};\n"
        )

        # 2. prompts.csv
        csv_buf = io.StringIO()
        fieldnames = ["prompt_id", "text"]
        writer = csv.DictWriter(csv_buf, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for p in vol_prompts:
            writer.writerow(p)
        csv_content = csv_buf.getvalue()

        # 3. README.md
        readme_content = f"""# {project_name} — {vol_name}

Welcome to your dedicated offline voice recording workspace!

### Package Details:
- **Contributor**: {vol_name} ({vol_id})
- **Assigned Prompts**: {len(vol_prompts):,} sentences
- **Prompts Range**: #{start_i + 1:,} to #{end_i:,}

---

## How to Record (Zero Installation):
1. Extract this `.zip` file on your laptop.
2. Double-click **`index.html`** to open the recorder in your web browser (Chrome, Edge, Safari, Firefox).
3. Click **"Begin Recording"** and allow microphone access when prompted.
4. All your assigned prompts are already pre-loaded into the studio!

---

## Keyboard Shortcuts:
- **`Spacebar`**: Toggle Record / Stop
- **`Tab`**: Play back your recorded take to check audio clarity
- **`R`**: Retake current sentence
- **`Ctrl + Enter`**: Mark **[✓ Done]** and advance to the next prompt!
- **`Alt + Left`**: Return to previous prompt

---

## Submitting Your Audio:
- When you finish recording your prompts, click **"Export Recordings (.ZIP)"** on the top bar.
- The app will package all your pristine 16-bit PCM WAV audio files and `metadata.csv` into a single zip.
- Upload your exported zip archive to your coordinator or email to: **{submission_email}**

Thank you for contributing your voice!
"""

        with zipfile.ZipFile(zip_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
            zf.writestr("speech-recorder/index.html", html_content)
            zf.writestr("speech-recorder/prompts.js", prompts_js)
            zf.writestr("speech-recorder/prompts.csv", csv_content)
            zf.writestr("speech-recorder/README.md", readme_content)

        print(f"Created: {zip_filename} ({len(vol_prompts):,} prompts, {zip_out.stat().st_size / (1024**2):.1f} MB)")

    print(f"\nSuccessfully created all {num_volunteers} ready-to-use recorder packages in {output_dir}/!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package prompts into offline recorder bundles.")
    parser.add_argument("--prompts-file", type=Path, default=Path("prompts.json"), help="Path to prompts JSON file")
    parser.add_argument("--recorder-html", type=Path, default=Path("index.html"), help="Path to recorder index.html")
    parser.add_argument("--output-dir", type=Path, default=Path("recorder-packages"), help="Output directory")
    parser.add_argument("--num-volunteers", type=int, default=4, help="Number of volunteer slices")
    parser.add_argument("--project-name", type=str, default="Speech Recording Studio", help="Project display name")
    parser.add_argument("--submission-email", type=str, default="contributions@example.org", help="Submission email")
    args = parser.parse_args()

    if not args.prompts_file.exists():
        print(f"Error: Prompts file not found at {args.prompts_file}")
        exit(1)

    package_prompts(
        prompts_file=args.prompts_file,
        recorder_html=args.recorder_html,
        output_dir=args.output_dir,
        num_volunteers=args.num_volunteers,
        project_name=args.project_name,
        submission_email=args.submission_email
    )
