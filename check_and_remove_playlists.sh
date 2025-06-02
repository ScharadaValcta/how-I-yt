#!/bin/bash

# Schleife über alle Dateien, die mit "playlist" beginnen
for playlist in playlist*; do
    # Überprüfen, ob die Datei existiert und es sich um eine reguläre Datei handelt
    if [ -f "$playlist" ]; then
        # Anzahl der vorhandenen Dateien in der Playlist zählen
        file_count=$(awk '{gsub(/\$/, "\\$", $0); system("ls \"" $0 "\" 2>/dev/null")}' "$playlist" | wc -l)

        # Wenn keine Dateien existieren (file_count == 0), Playlist ausgeben und löschen
        if [ "$file_count" -eq 0 ]; then
            echo "$playlist ist leer und wird gelöscht"
            rm "$playlist"
        else
            echo "$file_count  Dateien noch in $playlist" 
        fi
    fi
done
