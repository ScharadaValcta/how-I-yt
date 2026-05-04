#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------
# Utils
# ----------------------------

def pad_number(n):
    s = str(n)
    while len(s) <= 3:
        s = "0" + s
    return s


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
        return d.weekday()  # 4 = Freitag
    except:
        return None


def filter_friday_rce(dictionary):
    result = []
    for f in dictionary.get("Real Civil Engineer", []):
        if weekday_from_date(f[:8]) == 4:
            result.append(f)
    return result


# ----------------------------
# Core Algorithm
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
            stderr=subprocess.PIPE,
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

        resolution = "unknown"
        if width and height:
            resolution = "hochkant" if height > width else "quer"

        size_mb = os.path.getsize(file) / (1024 * 1024)
        mbps = size_mb / duration if duration > 0 else 0

        video_cache[file] = {
            "length": duration,
            "resolution": resolution,
            "mbps": mbps
        }

    except Exception:
        video_cache[file] = {
            "length": 0,
            "resolution": "unknown",
            "mbps": 0
        }

    return video_cache[file]


def probe_all_videos(files, workers=8):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(probe_video, f): f for f in files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print("Fehler bei:", file, e)


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

    write_playlist(f"playlist_{pad_number(len(playlist_rev))}_new.txt", playlist_rev)

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
    write_playlist("playlist_nach_mb_pro_sekunde.txt", sorted(files_size, key=lambda f: video_cache[f]["mbps"], reverse=True))

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


if __name__ == "__main__":
    main()

