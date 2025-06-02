
./py_create_watchlist_py.py 2>/dev/null

accounts=("ASSASSIN'S CREED REVELATIONS" "ASSASSIN'S CREED ROGUE" "ASSASSIN'S CREED： SHADOWS" "ASSASSIN'S CREED UNITY" "ASSASSIN'S CREED IV" "ASSASSIN'S CREED 3" "Assassin's Creed： Brotherhood" "CATCH ME" "38C3" "Adventure Buddies" "KRAFTKLUB" "Timberborn" "Snippet" "Out Now" "Trailer" "Teaser" "Ccamp 2023" "GPN 21" "EH21" "37C3" "Proxmox" "shorts" "linux" "rocket league" "windows" "music" "Internet" "lost" "Raspberry")

for i in "${accounts[@]}"; do
    find ./20youtub*/* ./* -type f -name "*.mp4" -ipath "*$i*" 2>/dev/null | sort >> "playlist_$i.txt"
done

find ./20youtub*/* ./* -type d -empty -delete 2>/dev/null

cat playlist_000* 2>/dev/null >> playlist_000.txt
cat playlist_0001_* 2>/dev/null >> playlist_0001.txt

cat playlist_nach_größe_gk.txt | head -10 >> playlist_nach_größe_gk_10.txt
tac playlist_nach_größe_gk.txt | head -10 >> playlist_nach_größe_kg_10.txt

cat playlist_nach_größe_gk.txt | grep -v "20youtube" | head -10 >> playlist_nach_größe_gk_10_500.txt
tac playlist_nach_größe_gk.txt | grep -v "20youtube" | head -10 >> playlist_nach_größe_kg_10_500.txt

echo "Entferne Playlist duplicate"
fdupes -r -n -A -S -t -d -N -p .  

echo "Warning Remove empty Playlists"
find -type f -name "playlist*" -empty
find -type f -name "playlist*" -empty -delete

echo "Warning possible inkomplette"
find -type f -name "*.temp.*" 

#Deletion of fragments
find -type f -name "*.f625.mp4" -delete
find -type f -name "*.f617.mp4" -delete
find -type f -name "*.f616.mp4" -delete
find -type f -name "*.f614.mp4" -delete
find -type f -name "*.f605.mp4" -delete
find -type f -name "*.f401.mp4" -delete
find -type f -name "*.f399.mp4" -delete
find -type f -name "*.f315.webm" -delete
find -type f -name "*.f313.webm" -delete
find -type f -name "*.f308.webm" -delete
find -type f -name "*.f303.webm" -delete
find -type f -name "*.f302.webm" -delete
find -type f -name "*.f299.mp4" -delete
find -type f -name "*.f298.mp4*" -delete
find -type f -name "*.f271.webm" -delete
find -type f -name "*.f270.mp4" -delete
find -type f -name "*.f251.webm" -delete
find -type f -name "*.f248.webm" -delete
find -type f -name "*.f247.webm" -delete
find -type f -name "*.f244.webm" -delete
find -type f -name "*.f243.webm" -delete
find -type f -name "*.f234.mp4" -delete
find -type f -name "*.f231.mp4" -delete
find -type f -name "*.f140.m4a" -delete
find -type f -name "*.f137.mp4" -delete
find -type f -name "*.f136.mp4" -delete
find -type f -name "*.f135.mp4" -delete
find -type f -name "*.f134.mp4" -delete
find -type f -name "*.f133.mp4" -delete

echo "Warning possible fragments"
find -type f -name "*.part" | sort
find -type f -name "*.ytdl" | sort 
find -type f -name "*\.f*" | sort
