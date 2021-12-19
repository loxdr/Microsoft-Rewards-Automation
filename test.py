import datetime
import json

retuned_values = ['markhjasadog123@outlook.com', 1, 3464, '0 / 30', 'N/A', '160 / 160', 1]

if retuned_values[6] == 1: pos = 'After'
elif retuned_values[6] == 0: pos = 'Before'
else: pos = 'Undefined'
today = f'{datetime.datetime.now():%d/%m/%Y}'

data_account = {}
data_core = {}
data_position = {}
data_date = {}
data_file = {}
data_core['Level'] = retuned_values[1]
data_core['Points'] = retuned_values[2]
data_core['PC Search'] = retuned_values[3]
data_core['Mobile Search'] = retuned_values[4]
data_core['Daily Challenges'] = retuned_values[5]
data_position[f'{pos}'] = data_core
data_account[f'{retuned_values[0]}'] = data_position
data_date[f'{today}'] = data_account
data_file = data_date

with open('log/stash.json', "r") as f:
    stash = json.load(f)

stash = dict(stash)
keys = stash.keys()
for i in keys:
    key = stash[i].keys()
    for x in key:
        ke = stash[i][x].keys()
        for z in ke:
            k = stash[i][x][z].keys()
    with open('log/stash.json', 'w') as f:
        json.dump(stash, f, indent=3)