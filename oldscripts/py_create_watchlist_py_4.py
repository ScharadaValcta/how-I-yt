#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------
# CONFIG
# ----------------------------

VIDEO_EXTENSIONS = {".mp4"}
UNWANTED_WORDS = {
    "the","und","der","die","das","ist","dein","auch","doch","durch","ende",
    "kein","noch","euch","dich","wird","will","sich","mein","eine","über",
    "habe","best","meine","this","your","nach","with","oder","sind","what",
    "into","werden","back","einfach","geht","kann","more","they","wirklich",
    "about","eigentlich","last","open","engineering","alles","wegen"
}

# ----------------------------
# Utils
# ----------------------------

def pad_number(n):
    return str(n).zfill(4)


def write_playlist(filename, items):
    with open(filename, "w", encoding="utf-8") as f:
        for i in items:
            f.write(i + "\n")


def delete_old_playlists():
    for f in Path(".").glob("playlist*.txt"):
        try:
            f.unlink()
        except:
            pass


# ----------------------------
# File Collection
# ----------------------------

def collect_video_files(base="."):
    extensions = ("*.mp4", "*.webm", "*.mkv")
    files = []
    for ext in extensions:
        files.extend(Path(base).rglob(ext))
    return [str(f) for f in files]


def split_files(files):
    interesting = [f for f in files if Path(f).parts[0].startswith("20")]
    interesting.sort()

    datum, longvid = [], []

    for f in interesting:
        parts = Path(f).parts
        if len(parts[0]) == 8 and parts[0].isdigit():
            datum.append(f)
        else:
            longvid.append(f)

    return datum, longvid


def build_dictionary(datum, longvid, reverse=False):
    d = defaultdict(list)

    for f in datum:
        parts = Path(f).parts
        if reverse:
            d[parts[1]] = [f] + d[parts[1]]
        else:
            d[parts[1]].append(f)

    for f in longvid:
        parts = Path(f).parts
        if len(parts[1]) == 8:
            key = parts[2]
            if reverse:
                d[key] = [f] + d[key]
            else:
                d[key].append(f)

    return dict(d)


# ----------------------------
# Date / Filter
# ----------------------------

def weekday_from_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y%m%d")
        return d.weekday()
    except:
        return None


def filter_friday_rce(dictionary):
    return [
        f for f in dictionary.get("Real Civil Engineer", [])
        if weekday_from_date(f[:8]) == 4
    ]


# ----------------------------
# Interleave
# ----------------------------

def interleave(dictionary, reverse=False):
    d = {k: list(v) for k, v in dictionary.items()}
    result = []

    while d:
        step = []

        for key in list(d.keys()):
            step.append(d[key].pop(0))
            if not d[key]:
                del d[key]

        first, second = [], []

        for f in step:
            parts = Path(f).parts
            if len(parts[0]) == 8 and parts[0].isdigit():
                first.append(f)
            else:
                second.append(f)

        first.sort(reverse=reverse)
        second.sort(reverse=reverse)

        result.extend(first + second)

    return result


# ----------------------------
# Parallel ffprobe
# ----------------------------

video_cache = {}

def probe_video(file):
    if file in video_cache:
        return video_cache[file]

    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "format=duration:stream=width,height",
                "-of", "default=noprint_wrappers=1",
                file
            ],
            stdout=subprocess.PIPE,
            text=True
        )

        duration, width, height = 0, 0, 0

        for line in result.stdout.splitlines():
            if "duration=" in line:
                duration = float(line.split("=")[1])
            elif "width=" in line:
                width = int(line.split("=")[1])
            elif "height=" in line:
                height = int(line.split("=")[1])

        resolution = "hochkant" if height > width else "quer" if width else "unknown"
        size_mb = os.path.getsize(file) / (1024 * 1024)
        mbps = size_mb / duration if duration > 0 else 0

        video_cache[file] = {
            "length": duration,
            "resolution": resolution,
            "mbps": mbps
        }

    except:
        video_cache[file] = {"length": 0, "resolution": "unknown", "mbps": 0}

    return video_cache[file]


def probe_all_videos(files, workers=8):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        list(as_completed([executor.submit(probe_video, f) for f in files]))


# ----------------------------
# 🆕 WORD PLAYLISTS (Script 2)
# ----------------------------

def generate_word_playlists(base="."):
    playlists = defaultdict(list)

    for path in Path(base).rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in VIDEO_EXTENSIONS:
            continue

        rel = str(path.relative_to(base))

        if rel.startswith("music") or rel.startswith(".git") or rel.startswith("config"):
            continue

        words = re.split(r'[^A-Za-z0-9ÄäÖöÜüß]+', path.stem)

        for word in words:
            if len(word) <= 2:
                continue

            w = word.lower()
            if w in UNWANTED_WORDS:
                continue

            playlists[w].append(rel)

    merged = defaultdict(list)

    for word, files in playlists.items():
        key = tuple(sorted(set(files)))
        merged[key].append(word)

    for files, words in merged.items():
        if len(files) <= 9:
            continue

        name_part = "-".join(sorted(words))
        if len(name_part) <= 3:
            continue

        filename = f"playlist_{len(files):04d}_{name_part}.txt"
        write_playlist(filename, files)


# ----------------------------
# MAIN
# ----------------------------

def main():
    delete_old_playlists()

    files = collect_video_files()
    datum, longvid = split_files(files)

    dictionary = build_dictionary(datum, longvid)

    for key, items in dictionary.items():
        write_playlist(f"playlist_{pad_number(len(items))}_{key}.txt", items)

    write_playlist("playlist_RCE_Freitag.txt", filter_friday_rce(dictionary))

    playlist = interleave(dictionary)
    write_playlist("playlist.txt", [f for f in playlist if not f.startswith("20youtube")])

    # ------------------------
    # ffprobe parallel
    # ------------------------

    patterns = ["./20youtub*/*/*/*.mp4", "./20*/*/*.mp4"]
    files_size = []

    for p in patterns:
        files_size.extend([str(f) for f in Path(".").glob(p)])

    probe_all_videos(files_size, workers=8)

    write_playlist("playlist_nach_länge.txt",
        sorted(files_size, key=lambda f: video_cache[f]["length"], reverse=True))

    write_playlist("playlist_nach_mb_pro_sekunde.txt",
        sorted(files_size, key=lambda f: video_cache[f]["mbps"], reverse=True))

    # ------------------------
    # 🆕 WORD PLAYLISTS
    # ------------------------

    generate_word_playlists()


if __name__ == "__main__":
    main()

