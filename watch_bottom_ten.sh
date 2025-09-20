#!/bin/bash

# Prüfen, ob eine Datei übergeben wurde
if [ -z "$1" ]; then
  echo "Usage: $0 <playlist_file>"
  exit 1
fi

# Bottom 10 Einträge (existierende Dateien aus Playlist)
awk '{gsub(/\$/, "\\$", $0); system("ls \"" $0 "\" 2>/dev/null")}' "$1" | tac | head -10 > playlist_remove.txt

# Zeige, was abgespielt wird
cat playlist_remove.txt

# Abspielen mit mpv
mpv --speed=2 --profile=fast --playlist=playlist_remove.txt

# Zeige erneut, was gespielt wurde
awk '{gsub(/\$/, "\\$", $0); system("ls \"" $0 "\" 2>/dev/null")}' playlist_remove.txt

# Löschen der abgespielten Dateien
awk '{gsub(/\$/, "\\$", $0); system("rm \"" $0 "\" 2>/dev/null")}' playlist_remove.txt
awk '{gsub(/\$/, "\\$", $0); system("ls \"" $0 "\" 2>/dev/null")}' "$1" | wc -l

