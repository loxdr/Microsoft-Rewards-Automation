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
    print(search_Terms)
search_Term_Generation()