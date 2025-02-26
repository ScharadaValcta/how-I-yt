
./py_create_watchlist_py.py 

accounts=("CATCH ME" "38C3" "Adventure Buddies" "KRAFTKLUB" "Timberborn" "Snippet" "Out Now" "Trailer" "Teaser" "Ccamp 2023" "FSCK 2024" "GPN 21" "EH21" "IGER 2023" "OsmoDevCall" "37C3" "Proxmox" "shorts" "linux" "rocket league" "windows" "drawn_together" "music" "Internet" "lost" "Raspberry")

for i in "${accounts[@]}"; do
    find 20youtub*/* ./* -type f -name "*.mp4" -ipath "*$i*" | sort >> "playlist_$i.txt"
done

find 20youtub*/* ./* -type d -empty -delete

cat playlist_000* >> playlist_000.txt
cat playlist_0001_* >> playlist_0001.txt

du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9][0-9][G]"      | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9],[0-9][G]"     | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9][0-9][0-9][M]" | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9][0-9][M]"      | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9],[0-9][M]"     | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9][0-9][0-9][K]" | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9][0-9][K]"      | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
du -sh 20youtub*/*/*/*.mp4 202*/*/*.mp4 music/*/*.mp4 | grep "^[1-9],[0-9][K]"     | sort -r | awk '{$1=""; print $0 }' >> "playlist_nach_größe_gk.txt"
tac playlist_nach_größe_gk.txt >> playlist_nach_größe_kg.txt

tac playlist_nach_größe_gk.txt | head -10 >> playlist_nach_größe_kg_10.txt
cat playlist_nach_größe_gk.txt | head -10 >> playlist_nach_größe_gk_10.txt

tac playlist_nach_größe_gk.txt | grep -v "20youtube" | head -10 >> playlist_nach_größe_kg_10_500.txt
cat playlist_nach_größe_gk.txt | grep -v "20youtube" | head -10 >> playlist_nach_größe_gk_10_500.txt

cat playlist_nach_größe_gk.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Viva La Dirt League\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr\|Techtastisch" >> playlist_RobertMarcLehmann_nach_größe_gk.txt
cat playlist_nach_größe_gk.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|Viva La Dirt League\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr\|Techtastisch" >> playlist_OttoBulletproof_nach_größe_gk.txt
cat playlist_nach_größe_gk.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Viva La Dirt League\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr\|Techtastisch" >> playlist_FritzMeineke_nach_größe_gk.txt
cat playlist_nach_größe_gk.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Viva La Dirt League\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA"  >> playlist_lethamyr_nach_größe_gk.txt
cat playlist_nach_größe_gk.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr" >> playlist_Viva_La_Dirt_League_nach_größe_gk.txt
cat playlist_nach_größe_kg.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|WBS LEGAL\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr" >> playlist_Viva_La_Dirt_League_nach_größe_kg.txt
cat playlist_nach_größe_kg.txt | grep -v "Made with Layers (Thomas Sanladerer)\|Daily Dose Of Internet\|TomSka & Friends\|DerSebo\|LockPickingLawyer\|Cleo Abram\|ElectroBOOM\|RvNx Mango\|ruthe.de\|Vsauce\|Sido\|Damestream Records\|Davis Schulz\|Techtastisch\|Steve Mould\|achNina\|Tiemo Wölken\|MythosOfGaming\|Plankton\|Corridor Digital\|Marti Fischer\|Grand Hotel van Cleef\|deichkindTV\|MarcUweKling\|Alligatoah\|Robert Marc Lehmann\|3Blue1Brown\|euremuetterchannel\|OttoBulletproof\|Das Lumpenpack\|KRAFTKLUB\|sarahgansebeck\|i12bretro\|SemperVideo\|STRG_F\|Comedy Kollektiv\|Florian Dalwigk\|Bodo Wartke\|Stonedeafproduction\|Farideh\|media.ccc.de\|General Knowledge\|Simplicissimus\|Veritasium\|Chris Titus Tech\|Trailerpark\|ProfEngel\|extra 3\|unsympathischTV\|TechHut\|Vox\|RumbleBeast666\|Real Civil Engineer\|Fäascht Bänkler\|I3I2I6\|Why Does Nothing Work\|DorFuchs\|2 Bored Guys\|MDR SPASSZONE\|Kurzgesagt \|MAITHINK X\|Eure Videos Fahrnünftig\|7 vs. Wild\|/NA/\|Fritz Meinecke\|AltF4Games\|Joseph DeChangeman\|DIY Perks\|SKIP THE BLA\|Lethamyr\|Viva La Dirt League" >> playlist_WBS_nach_größe_kg.txt


echo "Warning Remove empty Playlists"
find -type f -name "playlist*" -empty
find -type f -name "playlist*" -empty -delete

echo "Warning Posible inkomplette"
find -type f -name "*.temp.*" 

#Deletion of fragments
find -type f -name "*.f614.mp4" -delete
find -type f -name "*.f251.webm" -delete
find -type f -name "*.f616.mp4" -delete
find -type f -name "*.f298.mp4*" -delete
find -type f -name "*.f140.m4a" -delete
find -type f -name "*.f625.mp4" -delete
find -type f -name "*.f244.webm" -delete
find -type f -name "*.f313.webm" -delete
find -type f -name "*.f248.webm" -delete
find -type f -name "*.f303.webm" -delete
find -type f -name "*.f617.mp4" -delete
find -type f -name "*.f247.webm" -delete
find -type f -name "*.f135.mp4" -delete
find -type f -name "*.f136.mp4" -delete
find -type f -name "*.f137.mp4" -delete
find -type f -name "*.f271.webm" -delete
find -type f -name "*.f243.webm" -delete
find -type f -name "*.f299.mp4" -delete
find -type f -name "*.f134.mp4" -delete
find -type f -name "*.f605.mp4" -delete
find -type f -name "*.f302.webm" -delete
find -type f -name "*.f315.webm" -delete
find -type f -name "*.f308.webm" -delete
find -type f -name "*.f133.mp4" -delete
find -type f -name "*.f231.mp4" -delete
find -type f -name "*.f401.mp4" -delete
find -type f -name "*.f399.mp4" -delete

