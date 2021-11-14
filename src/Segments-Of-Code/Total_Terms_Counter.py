from re import sub
from random import randint, choice

words = ["What is the definition of 5", '5', "Etymology of 5", "What is the meaning of 5", "What country did the word 5 come from?", "What are some synonyms of 5", "What are some antonyms of 5", "Synonym of 5", "Antonym of 5", "Meaning of 5", "Where did the word 5 come from?"]
maths = ["What is the answer to: 5", "How do you solve: 5", "5 is equal to", "5"]
maths_signs = ['*', '/', "+", '-', ' plus ', ' minus ', ' times ', ' divided by ', ' over ', ' to the power of ']
movies_terms, states_terms, prefix_terms, words_terms, teams_terms, names_terms, country_terms, mountain_terms, iphone_terms = [], [], [], [], [], [], [], [], []
movies = ['Who are the main actors in 5', 'Who is the main character in 5', 'What is the plot of 5', 'When was 5 released', 'When was the movie 5 released', '5','Who produced 5', 'What is the storyine in 5', 'How is the plot resolved in 5']
states = ['Where is 5', 'Who is the governer of 5', 'Whats the area of 5', '5 election', 'Who is the home NFL team for 5', 'What are the attractions in 5', '5', 'who are the native people in 5', 'Whats the capital of 5']
names = ['Which country is the name 5 from', 'How popular is 5', 'Origin of the name 5', 'Is the name 5 popular', 'Names like 5', 'Other names like 5', '5']
countries = ['Where is 5', 'What is the currency in 5', 'What is the annual inflation rate for 5', 'Currency of 5', 'What are the neiboring countries of 5', 'Nearest country of 5', 'Capital of 5', 'Government of 5', 'Average internet speed in 5']
mountains = ['Where is 5 located', 'Latitude and Longitude of the mountain 5','What country is 5 in', 'What is the height of 5', 'What is the width of 5', 'Time to climb 5', 'Has anyone died climbing 5', 'Altitude of 5', '5']

# Maths terms are generated as needed so no need for txt file
with open('src/Support-Files/Random/movies.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        movies_terms.append(i)
with open('src/Support-Files/Random/states.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        states_terms.append(i)
with open('src/Support-Files/Random/words.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        words_terms.append(i)
with open('src/Support-Files/Random/names.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        names_terms.append(i)
with open('src/Support-Files/Random/countries.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        country_terms.append(i)
with open('src/Support-Files/Random/mountains.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        mountain_terms.append(i)
with open('src/Support-Files/Random/teams.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        teams_terms.append(i)
with open('src/Support-Files/Random/phones.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        iphone_terms.append(i)
with open('src/Support-Files/Random/prefixes.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for i in lines:
        i = sub('\n', '', i)
        prefix_terms.append(i)
        
total_Terms = []
for i in words_terms:
    for x in words:
        english_Term = sub('5', i, x)
        for z in range(1,5):
            if z == 1: 
                english_Term = english_Term.upper()
                total_Terms.append(english_Term)
            if z == 2: 
                english_Term = english_Term.lower()
                total_Terms.append(english_Term)
            if z == 3: 
                english_Term = english_Term.title()
                total_Terms.append(english_Term)
            if z == 4: 
                english_Term = english_Term.capitalize()
                total_Terms.append(english_Term)

# for d in maths:
#     for i in range(1,1000):
#         for x in range(1,1000):
#             for z in maths_signs:
#                 math = str(i)+z+str(x)
#                 maths_Term = sub('5', math, d)
#                 total_Terms.append(maths_Term)

print(len(total_Terms))