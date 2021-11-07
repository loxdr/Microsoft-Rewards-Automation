import requests, time, random, json
from requests.exceptions import RequestException
from datetime import datetime, timedelta

def search_Term_Generation():
    dates = []
    for i in range(0, 5):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime('%Y%m%d'))
    search_Terms = []
    for date in dates:
        try:
            url = f'https://trends.google.com/trends/api/dailytrends?hl=en-US&ed={date}&geo=US&ns=15'
            request = requests.get(url)
            response = json.loads(request.text[5:])
            for topic in response['default']['trendingSearchesDays'][0]['trendingSearches']:
                search_Terms.append(topic['title']['query'].lower())
                for related_topic in topic['relatedQueries']:
                    search_Terms.append(related_topic['query'].lower())
            print("Finished cycle")
            time.sleep(random.randint(1, 3))
        except RequestException:
            print('Error retrieving google trends json.')
    search_Terms = set(search_Terms)
    return search_Terms

temp_terms = search_Term_Generation()


# Start Here
accounts_Using = 5
set = 3
instance = 2

# Seperating from pack
terms = list(temp_terms)
st_Length = len(terms)
ct_Allocation = st_Length / accounts_Using
ct_Allocation = round(ct_Allocation)
ct_End = ct_Allocation * set
ct_Start = ct_End - ct_Allocation
split_Terms = terms[int(ct_Start):int(ct_End)]

# Separating into 3 groups of 5 and discarding the rest
if instance == 1:
    print(split_Terms[0:5])
if instance == 2:
    print(split_Terms[5:10])
if instance == 3:
    print(split_Terms[10:15])
if instance == 4:
    print(split_Terms[15:20])
if instance == 5:
    print(split_Terms[20:25])