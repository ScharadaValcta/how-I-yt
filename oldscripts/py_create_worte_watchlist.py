import os
import re
from collections import defaultdict

BASE_DIR = "."
VIDEO_EXTENSIONS = {".mp4"}
UNWANTED_WORDS = ["the", "und", "der", "die", "das", "ist", "dein", "auch", "doch", "durch", "ende", "kein", "noch", "euch", "dich", "wird", "will", "sich", "mein", "eine", "über", "habe", "best", "meine", "this", "your", "nach", "with", "oder", "sind", "what", "into", "werden", "back", "einfach", "geht", "kann", "more", "they", "wirklich", "about", "eigentlich", "last", "open", "engineering", "alles", "wegen"]

playlists = defaultdict(list)

# 1️⃣ Dateien einsammeln
for root, dirs, files in os.walk(BASE_DIR):
    for filename in files:
        name, ext = os.path.splitext(filename)

        if root.startswith("./music") or root.startswith("./.git") or root.startswith("./config") or root == ".":
            continue
        #else:
        #	print(root)

        if ext.lower() not in VIDEO_EXTENSIONS:
            continue

        words = re.split(r'[^A-Za-z0-9ÄäÖöÜüß]+', name)
        relative_path = os.path.relpath(os.path.join(root, filename), BASE_DIR)

        for word in words:
            if len(word) <= 2:
                continue

            lowerword = word.lower()
            if lowerword in UNWANTED_WORDS:
                continue

            playlists[lowerword].append(relative_path)

# 2️⃣ Playlists nach gleichem Inhalt mergen
merged = defaultdict(list)

for word, files in playlists.items():
    key = tuple(sorted(set(files)))  # eindeutiger Inhalt
    merged[key].append(word)

# 3️⃣ Playlist-Dateien schreiben
for files, words in merged.items():
    count = len(files)
    if count <= 9:
        continue
    count_str = f"{count:04d}"
    name_part = "-".join(sorted(words))
    if len(name_part) <= 3:
      continue 
    playlist_name = f"playlist_{count_str}_{name_part}.txt"

    with open(playlist_name, "w", encoding="utf-8") as f:
        for file in files:
            f.write(file + "\n")

print("Rekursive, gemergte Playlists wurden erstellt.")
