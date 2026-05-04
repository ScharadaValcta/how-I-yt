#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
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
    first_iteration = True

    while d:
        step = []
        to_delete = []

        for key in list(d.keys()):
            step.append(d[key][0])
            if len(d[key]) == 1:
                to_delete.append(key)
            else:
                d[key].pop(0)

        first, second = [], []

        for f in step:
            parts = Path(f).parts
            if len(parts[0]) == 8 and parts[0].isdigit():
                first.append(f)
            else:
                second.append(f)

        first.sort(reverse=reverse)
        second.sort(reverse=reverse)

        merged = first + second
        result.extend(merged)

        if first_iteration:
            try:
                if reverse:
                    write_playlist("playlist_one_new.txt", list(reversed(merged)))
                else:
                    write_playlist("playlist_one.txt", sorted(merged))
            except:
                pass
            first_iteration = False

        for k in to_delete:
            d.pop(k, None)

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
# WORD PLAYLISTS
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
# BASH REPLACEMENT
# ----------------------------

def generate_account_playlists():
    accounts = [
        "Podcast","20youtube","CatchMe 4","ASSASSIN'S CREED ROGUE",
        "ASSASSIN'S CREED： SHADOWS","ASSASSIN'S CREED UNITY","CATCH ME",
        "Adventure Buddies","Timberborn","Snippet","Out Now",
        "Ccamp 2023","GPN 21","_music","SURVIVAL SQUAD","Otto beim KSK"
    ]

    all_files = [str(f) for f in Path(".").rglob("*.mp4")]

    for acc in accounts:
        matched = [f for f in all_files if acc.lower() in f.lower()]
        matched.sort()
        write_playlist(f"playlist_{len(matched):04d}_{acc}.txt", matched)


def cleanup_empty_dirs():
    for path in Path(".").rglob("*"):
        if path.is_dir():
            try:
                if not any(path.iterdir()):
                    path.rmdir()
            except:
                pass


def merge_small_playlists():
    small = sorted(Path(".").glob("playlist_000*.txt"))
    with open("playlist_000.txt", "a", encoding="utf-8") as out:
        for f in small:
            try:
                out.write(f.read_text())
            except:
                pass

    small2 = sorted(Path(".").glob("playlist_0001_*.txt"))
    lines = []
    for f in small2:
        try:
            lines += f.read_text().splitlines()
        except:
            pass

    lines.sort()
    write_playlist("playlist_0001.txt", lines)


def top_bottom_size_lists():
    try:
        lines = Path("playlist_nach_größe_gk.txt").read_text().splitlines()

        write_playlist("playlist_nach_größe_gk_10.txt", lines[:10])
        write_playlist("playlist_nach_größe_kg_10.txt", list(reversed(lines))[:10])

        filtered = [l for l in lines if "20youtube" not in l]

        write_playlist("playlist_nach_größe_gk_10_500.txt", filtered[:10])
        write_playlist("playlist_nach_größe_kg_10_500.txt", list(reversed(filtered))[:10])
    except:
        pass


def remove_empty_playlists():
    for f in Path(".").glob("playlist*"):
        try:
            if f.is_file() and f.stat().st_size == 0:
                f.unlink()
        except:
            pass


def delete_fragments():
    patterns = [
        "*.f642.mp4","*.f625.mp4","*.f617.mp4","*.f616.mp4","*.f614.mp4",
        "*.f609.mp4","*.f605.mp4","*.f401.mp4","*.f400.mp4","*.f399.mp4",
        "*.f398.mp4","*.f315.webm","*.f313.webm","*.f308.webm","*.f303.webm",
        "*.f302.webm","*.f299.mp4","*.f298.mp4*","*.f271.webm","*.f270.mp4",
        "*.f251-1.webm","*.f251.webm","*.f248.webm","*.f247.webm",
        "*.f244.webm","*.f243.webm","*.f234.mp4","*.f231.mp4",
        "*.f140.m4a","*.f137.mp4","*.f136.mp4","*.f135.mp4",
        "*.f134.mp4","*.f133.mp4"
    ]

    for pattern in patterns:
        for f in Path(".").rglob(pattern):
            try:
                print("Delete fragment:", f)
                f.unlink()
            except:
                pass

def show_warnings():
    print("\n⚠️ Possible incomplete files:")
    for p in Path(".").rglob("*.temp.*"):
        print(p)

    print("\n⚠️ Possible fragments:")
    for pattern in ["*.part", "*.ytdl", "*.f*"]:
        for p in Path(".").rglob(pattern):
            print(p)

    print("\n⚠️ Possible unwanted:")
    for pattern in ["*Gray Area*", "*Das Beste*"]:
        for p in sorted(Path(".").rglob(pattern)):
            print(p)

def hash_file(path):
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None


def remove_duplicate_playlists():
    print("Entferne Playlist duplicate")

    playlist_files = list(Path(".").glob("playlist*.txt"))

    playlist_files.sort(key=lambda f: f.stat().st_mtime)

    seen = {}
    duplicates = []

    for file in playlist_files:
        try:
            content_hash = hash_file(file)

            if content_hash in seen:
                duplicates.append(file)
            else:
                seen[content_hash] = file

        except Exception as e:
            print("Error:", file, e)

    for dup in duplicates:
        try:
            print("Delete duplicate playlist:", dup)
            dup.unlink()
        except Exception as e:
            print("Could not delete:", dup, e)


def run_bash_replacement_playlist():
    generate_account_playlists()
    merge_small_playlists()
    top_bottom_size_lists()

def run_bash_replacement_cleanup():
    cleanup_empty_dirs()
    remove_empty_playlists()
    remove_duplicate_playlists()
    delete_fragments()
    show_warnings()


# ----------------------------
# Main
# ----------------------------

def main():
    delete_old_playlists()

    files = collect_video_files()
    datum, longvid = split_files(files)

    # ------------------------
    # Dictionary Playlists
    # ------------------------

    dictionary = build_dictionary(datum, longvid)

    for key, items in dictionary.items():
        write_playlist(f"playlist_{pad_number(len(items))}_{key}.txt", items)

    # Freitag RCE
    write_playlist("playlist_RCE_Freitag.txt", filter_friday_rce(dictionary))

    # Interleave normal
    playlist = interleave(dictionary, reverse=False)
    write_playlist(f"playlist_{pad_number(len(playlist))}.txt", playlist)

    write_playlist("playlist.txt",[f for f in playlist if not f.startswith("20youtube")]
    )

    # ------------------------
    # Reverse
    # ------------------------

    dictionary_rev = build_dictionary(datum, longvid, reverse=True)
    playlist_rev = interleave(dictionary_rev, reverse=True)

    write_playlist(f"playlist_{pad_number(len(playlist_rev))}_new.txt", interleave(dictionary_rev, reverse=True))

    write_playlist(
        "playlist_new.txt",
        [f for f in playlist_rev if not f.startswith("20youtube")]
    )

    # ------------------------
    # Size / ffprobe section
    # ------------------------

    patterns = ["./20youtub*/*/*/*.mp4", "./20*/*/*.mp4"]
    files_size = []
    for p in patterns:
        files_size.extend([str(f) for f in Path(".").glob(p)])

    # 🔥 PARALLEL SCAN
    probe_all_videos(files_size, workers=8)

    # Size
    write_playlist("playlist_nach_größe_gk.txt", sorted(files_size, key=os.path.getsize, reverse=True))
    write_playlist("playlist_nach_größe_kg.txt", sorted(files_size, key=os.path.getsize))

    # Length
    write_playlist("playlist_nach_länge.txt", sorted(files_size, key=lambda f: video_cache[f]["length"], reverse=True))

    # MB/s
    files_mbps = sorted(files_size, key=lambda f: video_cache[f]["mbps"], reverse=True)
    write_playlist("playlist_nach_mb_pro_sekunde.txt", files_mbps)

    # Resolution
    res_dict = defaultdict(list)
    for f in files_size:
        res_dict[video_cache[f]["resolution"]].append(f)

    for res, flist in res_dict.items():
        flist.sort()
        write_playlist(f"playlist_auflösung_{res}.txt", flist)

    # Year playlists
    yeardict = defaultdict(list)
    for f in files_mbps:
        parts = Path(f).parts
        if len(parts[0]) == 8 and parts[0].isdigit():
            year = parts[0][:4]
        else:
            year = parts[1][:4]
        yeardict[year].append(f)

    for year, flist in yeardict.items():
        filename = f"playlist_{pad_number(len(flist))}_{year}.txt"
        write_playlist(filename, flist)

    run_bash_replacement_playlist()

    # word playlists
    generate_word_playlists()

    # bash replacement
    run_bash_replacement_cleanup()

if __name__ == "__main__":
    main()

