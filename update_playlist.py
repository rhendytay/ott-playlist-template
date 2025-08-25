import os
import re
import sys
import requests

SOURCE_URL = os.getenv("SOURCE_URL", "https://bit.ly/KITKATTV")

# Tambah semua kata kunci terkait MNC Group
BLOCK_KEYWORDS = os.getenv(
    "BLOCK_KEYWORDS",
    "RCTI,MNCTV,GTV,iNews,MNC,Vision,IDX"
)

OUTPUT_FILE = os.getenv("OUTPUT_FILE", "iptv_playlist.m3u")


def fetch_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PlaylistBot/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=45, allow_redirects=True)
    resp.raise_for_status()
    resp.encoding = resp.encoding or "utf-8"
    return resp.text


def build_pattern(block_keywords: str):
    # Ubah string "RCTI,MNCTV,..." jadi regex (case-insensitive)
    words = [w.strip() for w in block_keywords.split(",") if w.strip()]
    if not words:
        return None
    pattern = "(" + "|".join(re.escape(w) for w in words) + ")"
    return re.compile(pattern, flags=re.IGNORECASE)


def filter_m3u(text: str, pat: re.Pattern | None) -> tuple[str, int, int]:
    lines = text.splitlines()
    out = []
    if not lines or not lines[0].lstrip().startswith("#EXTM3U"):
        out.append("#EXTM3U")

    skip = False
    kept = 0
    removed = 0

    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            if pat and pat.search(line):
                skip = True
                removed += 1
                continue
            else:
                skip = False
                kept += 1
                out.append(line)
        else:
            if not skip:
                out.append(line)

    result = "\n".join(out).rstrip() + "\n"
    return result, kept, removed


def main():
    try:
        original = fetch_text(SOURCE_URL)
    except Exception as e:
        print(f"::error::Failed to fetch source playlist: {e}")
        sys.exit(1)

    pat = build_pattern(BLOCK_KEYWORDS)
    filtered, kept, removed = filter_m3u(original, pat)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(filtered)

    print(f"✅ Generated {OUTPUT_FILE} | kept: {kept}, removed: {removed}")

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as s:
            s.write(f"### Playlist Update Result\n")
            s.write(f"- Source: {SOURCE_URL}\n")
            s.write(f"- Output: `{OUTPUT_FILE}`\n")
            s.write(f"- Kept: **{kept}**\n")
            s.write(f"- Removed (blocked): **{removed}**\n")


if __name__ == "__main__":
    main()
