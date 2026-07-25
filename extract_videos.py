import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error

CHANNEL_URL = "https://www.youtube.com/@sensebar/videos"
FILTER_KEYWORDS = ["claude", "codex", "antigravity", "opencode", "agent", "ai agent", "knowledge"]
OUTPUT_FILE = "sensebar_ai_urls.txt"
VIDEO_METADATA_FILE = "sensebar_ai_videos.md"


def extract_video_ids_from_html(html):
    patterns = [
        r'watch\?v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})"',
        r'/embed/([a-zA-Z0-9_-]{11})',
    ]
    ids = set()
    for pattern in patterns:
        matches = re.findall(pattern, html)
        ids.update(matches)
    return list(ids)


def fetch_page(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return ""


def extract_video_metadata(html, video_id):
    title_match = re.search(
        r'<title>(.*?)</title>', html, re.DOTALL
    )
    title = title_match.group(1).strip() if title_match else f"Video {video_id}"
    title = re.sub(r"\s*-\s*YouTube\s*$", "", title)

    desc_match = re.search(
        r'<meta name="description" content="([^"]*)"',
        html,
    )
    description = desc_match.group(1) if desc_match else ""

    return {"id": video_id, "title": title, "description": description, "url": f"https://www.youtube.com/watch?v={video_id}"}


def matches_keywords(text, keywords):
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return True
    return False


def main():
    print(f"[Step 1] Fetching channel page: {CHANNEL_URL}")
    html = fetch_page(CHANNEL_URL)
    if not html:
        print("[ERROR] Could not fetch channel page. Using fallback URL list.")
        fallback_ids = []
        with open(OUTPUT_FILE, "w") as f:
            for vid in fallback_ids:
                f.write(f"https://www.youtube.com/watch?v={vid}\n")
        print(f"[DONE] Wrote {len(fallback_ids)} URLs to {OUTPUT_FILE}")
        return

    video_ids = extract_video_ids_from_html(html)
    print(f"  Found {len(video_ids)} video references in HTML.")

    matched_videos = []
    for i, vid in enumerate(video_ids):
        video_url = f"https://www.youtube.com/watch?v={vid}"
        print(f"  [{i+1}/{len(video_ids)}] Checking {vid}...")
        page_html = fetch_page(video_url)
        if not page_html:
            continue
        meta = extract_video_metadata(page_html, vid)
        combined_text = meta["title"] + " " + meta["description"]
        if matches_keywords(combined_text, FILTER_KEYWORDS):
            print(f"    [MATCH] {meta['title']}")
            matched_videos.append(meta)
        else:
            print(f"    [SKIP] {meta['title']}")

    matched_videos.sort(key=lambda x: x["title"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for mv in matched_videos:
            f.write(mv["url"] + "\n")
    print(f"\n[DONE] Wrote {len(matched_videos)} matched URLs to {OUTPUT_FILE}")

    with open(VIDEO_METADATA_FILE, "w", encoding="utf-8") as f:
        f.write("# Sensebar AI Videos Metadata\n\n")
        f.write(f"_Total matches: {len(matched_videos)}_\n\n")
        for mv in matched_videos:
            f.write(f"## {mv['title']}\n\n")
            f.write(f"- **Video ID**: {mv['id']}\n")
            f.write(f"- **URL**: [{mv['url']}]({mv['url']})\n")
            f.write(f"- **Description**: {mv['description'][:200]}{'...' if len(mv['description']) > 200 else ''}\n\n")
            f.write("---\n\n")
    print(f"[DONE] Wrote metadata to {VIDEO_METADATA_FILE}")


if __name__ == "__main__":
    main()
