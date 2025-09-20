#!/usr/bin/env python

import glob
import os
import subprocess
from collections import defaultdict

#delete playlist*.txt
txt = glob.glob('playlist*.txt')
for i in txt:
    os.remove(i)

#all mp4
files = glob.glob('**/*.mp4', recursive=True)
files_webm = glob.glob('**/*.webm', recursive=True)
files_mkv = glob.glob('**/*.mkv', recursive=True)

files = files + files_webm + files_mkv

interessing_files = [file for file in files if file.startswith("20")]
sorted_files = sorted(interessing_files)

datum = []
longvid = []

for i in sorted_files:
    splited = i.split("/")
    if len(splited[0]) == 8 and splited[0].isnumeric():
        datum.append(i)
    else:
        longvid.append(i)

worddic = dict()
wordlist = ["the","das","der","auf","with","für","die","mit","von","und","ist","a","an","","die","the","of","s","im","to","das","in","so"]

dictionary = dict()

for i in datum:
    splited = i.split("/")
    if splited[1] in dictionary:
        dictionary[splited[1]] = dictionary[splited[1]] + [i]
    else:
        dictionary[splited[1]] = [i]

for i in longvid:
    splited = i.split("/")
    if len(splited[1]) == 8:
        if splited[2] in dictionary:
            dictionary[splited[2]] = dictionary[splited[2]] + [i]
        else:
            dictionary[splited[2]] = [i]
    else:
        print(i)

for i in dictionary:
    number = str(len(dictionary[i]))
    while len(number) <= 3:
        number = '0' + number

    file = "playlist_" + number + "_" + i + ".txt"
    with open(file, "w") as my_file:
        for k in dictionary[i]:
            my_file.write(k)
            my_file.write("\n")


list_for_sami = []
list_for_sami_reverse = []
one = 0

while dictionary:
    list_in_iteration = []
    list_in_iteration_reverse = []
    dictionaries_to_delete = []
    for i in dictionary:
        list_in_iteration.append(dictionary[i][0])
        if len(dictionary[i]) == 1:
            dictionaries_to_delete.append(i)
        else:
            del dictionary[i][0]
    first = []
    second = []
    for i in list_in_iteration:
        splited = i.split("/")
        if len(splited[0]) == 8 and splited[0].isnumeric():
            first.append(i)
        else:
            second.append(i)
    #playlist.txt
    list_in_iteration = sorted(first) + sorted(second)
    list_for_sami += list_in_iteration
    #playlist_new.txt
    f = sorted(first)
    f.reverse()
    s = sorted(second)
    s.reverse()
    list_in_iteration_reverse = f + s
    list_for_sami_reverse = list_in_iteration_reverse + list_for_sami_reverse

    for i in dictionaries_to_delete:
        silent = dictionary.pop(i)
    if one == 0:
        try:
            file = "playlist_one.txt"
            with open(file, "w") as my_file:
                for i in list_in_iteration:
                    my_file.write(i)
                    my_file.write("\n")
        except:
            pass
        one = 1

try:
    number = str(len(list_for_sami))
    while len(number) <= 3:
        number = '0' + number

    file = "playlist_" + number + ".txt"
    with open(file, "w") as my_file:
        for i in list_for_sami:
            my_file.write(i)
            my_file.write("\n")
except:
    pass

try:
    file = "playlist.txt"
    with open(file, "w") as my_file:
        for i in list_for_sami:
            if i.startswith("20youtube"):
                continue
            else:
                my_file.write(i)
                my_file.write("\n")
except:
    pass


#Start of reverse
dictionary = dict()

for i in datum:
    splited = i.split("/")
    if splited[1] in dictionary:
        dictionary[splited[1]] = [i] + dictionary[splited[1]]
    else:
        dictionary[splited[1]] = [i]

for i in longvid:
    splited = i.split("/")
    if len(splited[1]) == 8:
        if splited[2] in dictionary:
            dictionary[splited[2]] = dictionary[splited[2]] + [i]
        else:
            dictionary[splited[2]] = [i]
    else:
        print(i)

list_for_sami = []
list_for_sami_reverse = []
one = 0

while dictionary:
    list_in_iteration = []
    list_in_iteration_reverse = []
    dictionaries_to_delete = []
    for i in dictionary:
        list_in_iteration.append(dictionary[i][0])
        if len(dictionary[i]) == 1:
            dictionaries_to_delete.append(i)
        else:
            del dictionary[i][0]
    first = []
    second = []
    for i in list_in_iteration:
        splited = i.split("/")
        if len(splited[0]) == 8 and splited[0].isnumeric():
            first.append(i)
        else:
            second.append(i)
    #playlist.txt

    first.reverse()
    second.reverse()

    list_in_iteration = first + second
    list_for_sami += list_in_iteration

    for i in dictionaries_to_delete:
        silent = dictionary.pop(i)

    if one == 0:
        try:
            number = str(len(list_in_iteration))
            while len(number) <= 3:
                number = '0' + number
            file = "playlist_one_new.txt"
            with open(file, "w") as my_file:
                for i in list_in_iteration:
                    my_file.write(i)
                    my_file.write("\n")
        except:
            pass
        one = 1

try:
    number = str(len(list_for_sami))
    while len(number) <= 3:
        number = '0' + number

    file = "playlist_" + number + "_new.txt"
    with open(file, "w") as my_file:
        for i in list_for_sami:
            my_file.write(i)
            my_file.write("\n")
except:
    pass

try:
    file = "playlist_new.txt"
    with open(file, "w") as my_file:
        for i in list_for_sami:
            if i.startswith("20youtube"):
                continue
            else:
                my_file.write(i)
                my_file.write("\n")
except:
    pass

patterns = ["./20youtub*/*/*/*.mp4", "./20*/*/*.mp4"]
files = []
for pattern in patterns:
    files.extend(glob.glob(pattern))

sorted_files_gk = sorted(files, key=os.path.getsize, reverse=True)
sorted_files_kg = sorted(files, key=os.path.getsize, reverse=False)
    
with open("playlist_nach_größe_gk.txt", "w") as f:
    for file in sorted_files_gk:
        f.write(file + "\n")

with open("playlist_nach_größe_kg.txt", "w") as f:
    for file in sorted_files_kg:
        f.write(file + "\n")

def get_video_length(filename):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip())
    except Exception:
        return 0

sorted_files_length = sorted(files, key=get_video_length, reverse=True)

with open("playlist_nach_länge.txt", "w") as f:
    for file in sorted_files_length:
        f.write(file + "\n")


def get_video_resolution(filename):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        #return result.stdout.strip().replace(",", "x")
        width, height = map(int, result.stdout.strip().split(","))
        return "hochkant" if height > width else "quer"
    except Exception:
        return "unknown"

# Dictionary für die Playlists nach Auflösung
resolution_dict = defaultdict(list)

for file in files:
    resolution = get_video_resolution(file)
    resolution_dict[resolution].append(file)
    resolution_dict[resolution].sort()

# Für jede Auflösung eine eigene Playlist erstellen
for resolution, file_list in resolution_dict.items():
    playlist_filename = f"playlist_auflösung_{resolution}.txt"
    with open(playlist_filename, "w") as f:
        for file in file_list:
            f.write(file + "\n")

#playlist_$number_$year.txt
yeardict = dict()
for i in sorted_files:
    splited = i.split("/")
    if len(splited[0]) == 8 and splited[0].isnumeric():
        year = splited[0][0:4]
    else:
        year = splited[1][0:4]
    if year not in yeardict:
        yeardict[year] = []
    yeardict[year].append(i)

for year, file_list in yeardict.items():
    number = str(len(file_list))
    while len(number) <= 3:
        number = '0' + number

    playlist_filename = f"playlist_{number}_{year}.txt"
    with open(playlist_filename, "w") as f:
        for file in file_list:
            f.write(file + "\n")
