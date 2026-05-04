#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
import os

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

        # entspricht playlist_one.txt
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
# ffprobe helpers (cached!)
# ----------------------------

_length_cache = {}

def get_video_length(file):
    if file in _length_cache:
        return _length_cache[file]

    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        val = float(result.stdout.strip())
    except:
        val = 0

    _length_cache[file] = val
    return val


def get_mb_per_second(file):
    try:
        size_mb = os.path.getsize(file) / (1024 * 1024)
        length = get_video_length(file)
        return size_mb / length if length > 0 else 0
    except:
        return 0


def get_video_resolution(file):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error",
             "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        parts = result.stdout.strip().split(",")
        width, height = map(int, parts[:2])
        return "hochkant" if height > width else "quer"
    except:
        return "unknown"


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
        filename = f"playlist_{pad_number(len(items))}_{key}.txt"
        write_playlist(filename, items)

    # Freitag RCE
    rce = filter_friday_rce(dictionary)
    write_playlist("playlist_RCE_Freitag.txt", rce)

    # Interleave normal
    playlist = interleave(dictionary, reverse=False)
    write_playlist(f"playlist_{pad_number(len(playlist))}.txt", playlist)

    write_playlist(
        "playlist.txt",
        [f for f in playlist if not f.startswith("20youtube")]
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
    # Size sorting
    # ------------------------

    patterns = ["./20youtub*/*/*/*.mp4", "./20*/*/*.mp4"]
    files_size = []
    for p in patterns:
        files_size.extend([str(f) for f in Path(".").glob(p)])

    files_gk = sorted(files_size, key=os.path.getsize, reverse=True)
    files_kg = sorted(files_size, key=os.path.getsize)

    write_playlist("playlist_nach_größe_gk.txt", files_gk)
    write_playlist("playlist_nach_größe_kg.txt", files_kg)

    # ------------------------
    # Length sorting
    # ------------------------

    files_len = sorted(files_size, key=get_video_length, reverse=True)
    write_playlist("playlist_nach_länge.txt", files_len)

    # ------------------------
    # MB/s sorting
    # ------------------------

    files_mbps = sorted(files_size, key=get_mb_per_second, reverse=True)
    write_playlist("playlist_nach_mb_pro_sekunde_with_values.txt", files_mbps)

    # ------------------------
    # Resolution playlists
    # ------------------------

    res_dict = defaultdict(list)
    for f in files_size:
        res = get_video_resolution(f)
        res_dict[res].append(f)

    for res, flist in res_dict.items():
        flist.sort()
        write_playlist(f"playlist_auflösung_{res}.txt", flist)

    # ------------------------
    # Year playlists
    # ------------------------

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

