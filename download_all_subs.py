import os
import re
import subprocess
import sys

URLS_FILE = "sensebar_ai_urls.txt"
SUBTITLES_DIR = "subtitles"
CLIPPING_DIR = "Clipping"


def clean_vtt_content(raw_text):
    lines = raw_text.split("\n")
    cleaned_lines = []
    prev_line = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:"):
            continue
        if line.startswith("Language:"):
            continue

        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue

        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue

        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'<c[^>]*>', '', line)
        line = re.sub(r'</c>', '', line)
        line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', line)

        line = line.strip()

        if not line:
            continue

        if line == prev_line:
            continue

        cleaned_lines.append(line)
        prev_line = line

    return "\n\n".join(cleaned_lines)


def download_subtitles(url):
    print(f"  Downloading subtitles for: {url}")
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--skip-download",
                "--write-auto-subs",
                "--sub-langs", "en,zh-Hans,zh-Hant,ja",
                "--sub-format", "vtt",
                "--output", os.path.join(SUBTITLES_DIR, "%(title)s.%(ext)s"),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"    [WARN] yt-dlp returned non-zero: {result.stderr[:200]}")
        print(f"    [INFO] {result.stdout[-300:]}" if result.stdout else "")
        return True
    except FileNotFoundError:
        print("    [ERROR] yt-dlp not found. Install with: pip install yt-dlp")
        return False
    except subprocess.TimeoutExpired:
        print("    [ERROR] yt-dlp timed out")
        return False
    except Exception as e:
        print(f"    [ERROR] {e}")
        return False


def process_vtt_files():
    if not os.path.exists(SUBTITLES_DIR):
        print(f"[ERROR] {SUBTITLES_DIR}/ directory not found.")
        return

    os.makedirs(CLIPPING_DIR, exist_ok=True)

    vtt_files = [f for f in os.listdir(SUBTITLES_DIR) if f.endswith(".vtt")]
    print(f"  Found {len(vtt_files)} .vtt files to process.")

    for vtt_file in vtt_files:
        vtt_path = os.path.join(SUBTITLES_DIR, vtt_file)
        print(f"  Cleaning: {vtt_file}")

        try:
            with open(vtt_path, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
        except Exception as e:
            print(f"    [ERROR] Reading {vtt_file}: {e}")
            continue

        title = os.path.splitext(vtt_file)[0]
        title_clean = re.sub(r'\.(en|zh-Hans|zh-Hant|ja)$', '', title)
        title_clean = re.sub(r'[^\w\s\-_()\u4e00-\u9fff]', '', title_clean)

        cleaned = clean_vtt_content(raw)

        youtube_url = ""
        url_file = URLS_FILE
        if os.path.exists(url_file):
            with open(url_file, "r", encoding="utf-8") as uf:
                lines = uf.readlines()
                if lines:
                    youtube_url = lines[0].strip()

        md_content = f"# {title_clean}\n\n"
        if youtube_url:
            md_content += f"> **Source**: [{youtube_url}]({youtube_url})\n\n"
        md_content += cleaned

        md_filename = title_clean.replace(" ", "_") + ".md"
        md_path = os.path.join(CLIPPING_DIR, md_filename)

        try:
            with open(md_path, "w", encoding="utf-8") as mf:
                mf.write(md_content)
            print(f"    [OK] Written to {CLIPPING_DIR}/{md_filename}")
        except Exception as e:
            print(f"    [ERROR] Writing {md_filename}: {e}")


def main():
    print("=" * 60)
    print("AI Agent Knowledge Vault Builder")
    print("=" * 60)

    if not os.path.exists(SUBTITLES_DIR):
        os.makedirs(SUBTITLES_DIR)
        print(f"[INFO] Created {SUBTITLES_DIR}/ directory")

    urls_file = URLS_FILE
    if not os.path.exists(urls_file):
        print(f"[ERROR] {urls_file} not found. Run extract_videos.py first.")
        print("[INFO] Creating sample URL file for manual editing...")
        with open(urls_file, "w", encoding="utf-8") as f:
            f.write("# Add YouTube video URLs below, one per line\n")
            f.write("# Example:\n")
            f.write("# https://www.youtube.com/watch?v=xxxxxxxxxxx\n")
        print(f"[INFO] Created sample {urls_file}. Add URLs and re-run.")
        sys.exit(1)

    with open(urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        print(f"[ERROR] No URLs found in {urls_file}")
        sys.exit(1)

    print(f"[Step 2] Downloading subtitles for {len(urls)} videos...")
    for i, url in enumerate(urls):
        print(f"  [{i+1}/{len(urls)}] Processing...")
        download_subtitles(url)

    print(f"\n[Step 3] Cleaning VTT files and writing Markdown...")
    process_vtt_files()

    print(f"\n{'=' * 60}")
    print(f"[DONE] Knowledge base updated!")
    print(f"  - Raw subtitles: {SUBTITLES_DIR}/")
    print(f"  - Cleaned transcripts: {CLIPPING_DIR}/")
    print(f"  - Use AGENTS.md to instruct AI agent for vault maintenance")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
