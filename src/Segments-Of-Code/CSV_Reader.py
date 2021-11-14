import csv
# codes = []
# names = []
cities = []
with open("src/Support-Files/Random/airports.csv", 'r', encoding='UTF-8') as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    for row in csvreader:
        cities.append(f"{row[0]}, {row[2]}")

with open("src/Support-Files/Random/cities.txt", 'a', encoding='UTF-8') as f:
    for i in cities:
        f.write(f'{i}\n')

# with open("src/Support-Files/Random/airport_Names.txt", 'a', encoding='UTF-8') as f:
#     for i in names:
#         f.write(f'{i}\n')

# with open("src/Support-Files/Random/airport_Codes.txt", 'a', encoding='UTF-8') as f:
#     for i in codes:
#         f.write(f'{i}\n')