from datetime import datetime, timedelta
from json import load, loads
from multiprocessing import Process
from os.path import isfile
from random import choice, randint
from re import search, sub
from sys import exit, platform
from time import sleep

from requests import get
from requests.exceptions import ChunkedEncodingError, RequestException
from selenium import webdriver
from selenium.common.exceptions import (TimeoutException, UnexpectedAlertPresentException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class chrome_Instances():
    def __init__(self):
        self.platform_Checker()
        self.chrome_Init()

    def platform_Checker(self):
        self.platform = platform
        if self.platform == "linux" or self.platform == "linux2":
            self.os = "Linux"
        if self.platform == "darwin":
            self.os = "Mac"
        if self.platform == "win32":
            self.os = "Windows"
    
    def chrome_Init(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("--disable-logging")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--log-level=3")
        if self.os == 'Windows':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/Chrome-Files/chromedriver.exe", options=options)
        if self.os == 'Mac':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/Chrome-Files/chromedriver", options=options)
        if self.os == 'Linux':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/Chrome-Files/chromedriver-linux", options=options)
        return self.browser
    
    def get_Browser(self):
        return self.browser
    
    def action_key(self, xpath, keys):
        temp = self.browser.find_element_by_xpath(xpath=xpath)
        temp.send_keys(keys)
    
class Microsoft_Rewards_Automation():
    def __init__(self):
        # Variables
        self.accounts_Using = 1
        self.search_Terms = []
        
        # Functions
        self.data_Management()
        self.platform_Checker()
        self.search_Term_Generation()

    def platform_Checker(self):
        self.platform = platform
        if self.platform == "linux" or self.platform == "linux2":
            self.os = "Linux"
        if self.platform == "darwin":
            self.os = "Mac"
        if self.platform == "win32":
            self.os = "Windows"

    def data_Management(self):
        if isfile('src/Support-Files/data.json') != True:
            try:
               open("src/Support-Files/data.json", "x")
            except PermissionError:
                print("Unable to complete as this program does not have the required permissions")
                exit()
            except:
                print("Unexpected Error Occured")
                exit()
            print("\n\n\n  >>  You need to enter usernames and passwords into data.json")
            print("  >>  An example is in example-json.txtn\n\n\n")
            exit()
        else:
            with open("src/Support-Files/data.json", "r") as document:
                try:
                    data = load(document)
                except:
                    print("\n\n\n  >>  You need to enter usernames and passwords into data.json")
                    print("  >>  An example is in example-json.txtn\n\n\n")
                    exit()
                self.account_1_email = data['Account-1']['Email-1']
                self.account_1_pass = data['Account-1']['Password-1']
                self.account_2_email = data['Account-2']['Email-2']
                self.account_2_pass = data['Account-2']['Password-2']
                self.account_3_email = data['Account-3']['Email-3']
                self.account_3_pass = data['Account-3']['Password-3']
                self.account_4_email = data['Account-4']['Email-4']
                self.account_4_pass = data['Account-4']['Password-4']
                self.account_5_email = data['Account-5']['Email-5']
                self.account_5_pass = data['Account-5']['Password-5']
                self.account_Email_List = [self.account_1_email,self.account_2_email,self.account_3_email,self.account_4_email,self.account_5_email]
                self.account_Password_List = [self.account_1_pass,self.account_2_pass,self.account_3_pass,self.account_4_pass, self.account_5_pass]

    def search_Term_Generation(self):
        words = ["What is the definition of 5", '5', "Etymology of 5", "What is the meaning of 5", "What country did the word 5 come from?", "What are some synonyms of 5", "What are some antonyms of 5", "Synonym of 5", "Antonym of 5", "Meaning of 5", "Where did the word 5 come from?"]
        maths = ["What is the answer to: 5", "How do you solve: 5", "5 is equal to", "5"]
        maths_signs = ['*', '/', "+", '-', ' plus ', ' minus ', ' times ', ' divided by ', ' over ', ' to the power of ']
        movies_terms, states_terms, cities_terms, prefix_terms, words_terms, teams_terms, names_terms, country_terms, mountain_terms, iphone_terms, airport_code_terms, airport_name_terms = [], [], [], [], [], [], [], [], [], [], [], []
        movies = ['Who are the main actors in 5', 'Who is the main character in 5', 'What is the plot of 5', 'When was 5 released', 'When was the movie 5 released', '5','Who produced 5', 'What is the storyine in 5', 'How is the plot resolved in 5']
        states = ['Where is 5', 'Who is the governer of 5', 'Whats the area of 5', '5 election', 'Who is the home NFL team for 5', 'What are the attractions in 5', '5', 'who are the native people in 5', 'Whats the capital of 5']
        names = ['Which country is the name 5 from', 'How popular is 5', 'Origin of the name 5', 'Is the name 5 popular', 'Names like 5', 'Other names like 5', '5']
        countries = ['Where is 5', 'What is the currency in 5', 'What is the annual inflation rate for 5', 'Currency of 5', 'What are the neiboring countries of 5', 'Nearest country of 5', 'Capital of 5', 'Government of 5', 'Average internet speed in 5']
        mountains = ['Where is 5 located', 'Latitude and Longitude of the mountain 5','What country is 5 in', 'What is the height of 5', 'What is the width of 5', 'Time to climb 5', 'Has anyone died climbing 5', 'Altitude of 5', '5']
        teams = ['Score for 5', 'Where is 5 on the ladder', 'Ladder 5', '5', 'Top five players in 5', 'Average pay of player in 5', 'Most popular player in 5', 'Highest paid player in 5', '5 goalkeeper']
        cities = ['Where is 5', 'What continent is 5', 'Whats the population of 5', 'How many pepole live in 5', 'Average household size in 5']
        airport_Codes = ['Airport data for 5', 'Whats the active runway for 5', 'When was 5 made', 'Who operates 5', 'Operation time of 5', 'Open hours of 5', 'Open date of 5', 'What airlines fly to 5', 'Airport charts for 5']
        airport_Names = ['Airport data for 5', 'Whats the active runway for 5', 'When was 5 made', 'Who operates 5', 'Operation time of 5', 'Open hours of 5', 'Open date of 5', 'What airlines fly to 5', 'Airport charts for 5']
        iphones = ['When was the 5 released', 'Camera quality of the 5', '5', 'Battery life of the 5', 'Screen size of the 5', 'Screen replacement for 5', 'ifixit.com 5']
        prefixes = ['What is the meaning of 5', '5', 'Metric prefix 5', 'What number is 5', '5 in numbers']
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
        with open('src/Support-Files/Random/cities.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                cities_terms.append(i)
        with open('src/Support-Files/Random/airport_Names.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                airport_name_terms.append(i)
        with open('src/Support-Files/Random/airport_Codes.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                airport_code_terms.append(i)
        
        while len(self.search_Terms) < 500:
            rng = randint(1,13)
            if rng == 1: # English
                # English
                english_Term = sub('5', choice(words_terms), choice(words))
                int = randint(1,4)
                if int == 1: english_Term = english_Term.upper()
                if int == 2: english_Term = english_Term.lower()
                if int == 3: english_Term = english_Term.title()
                if int == 4: english_Term = english_Term.capitalize()
                self.search_Terms.append(english_Term)
                pass
            if rng == 2: # Maths
                # Maths
                x,y = randint(1,999), randint(1,999)
                maths_Term = str(x)+choice(maths_signs)+str(y)
                maths_Term = sub('5', maths_Term, choice(maths))
                self.search_Terms.append(maths_Term)
                pass
            if rng == 3: # Movies
                # Movies
                movie_Term = sub('5', choice(movies_terms), choice(movies))
                int = randint(1,4)
                if int == 1: movie_Term = movie_Term.upper()
                if int == 2: movie_Term = movie_Term.lower()
                if int == 3: movie_Term = movie_Term.title()
                if int == 4: movie_Term = movie_Term.capitalize()
                self.search_Terms.append(movie_Term)
                pass
            if rng == 4: # States
                # States
                state_Term = sub('5', choice(states_terms), choice(states))
                int = randint(1,4)
                if int == 1: state_Term = state_Term.upper()
                if int == 2: state_Term = state_Term.lower()
                if int == 3: state_Term = state_Term.title()
                if int == 4: state_Term = state_Term.capitalize()
                self.search_Terms.append(state_Term)
                pass
            if rng == 5: # Names
                name_Term = sub('5', choice(names_terms), choice(names))
                int = randint(1,4)
                if int == 1: name_Term = name_Term.upper()
                if int == 2: name_Term = name_Term.lower()
                if int == 3: name_Term = name_Term.title()
                if int == 4: name_Term = name_Term.capitalize()
                self.search_Terms.append(name_Term)
                pass
            if rng == 6: # Countries
                country_Term = sub('5', choice(country_terms), choice(countries))
                int = randint(1,4)
                if int == 1: country_Term = country_Term.upper()
                if int == 2: country_Term = country_Term.lower()
                if int == 3: country_Term = country_Term.title()
                if int == 4: country_Term = country_Term.capitalize()
                self.search_Terms.append(country_Term)
                pass
            if rng == 7: # Mountains
                mountain_Term = sub('5', choice(mountain_terms), choice(mountains))
                int = randint(1,4)
                if int == 1: mountain_Term = mountain_Term.upper()
                if int == 2: mountain_Term = mountain_Term.lower()
                if int == 3: mountain_Term = mountain_Term.title()
                if int == 4: mountain_Term = mountain_Term.capitalize()
                self.search_Terms.append(mountain_Term)
                pass
            if rng == 8: # Soccer Teams
                team_Term = sub('5', choice(teams_terms), choice(teams))
                int = randint(1,4)
                if int == 1: team_Term = team_Term.upper()
                if int == 2: team_Term = team_Term.lower()
                if int == 3: team_Term = team_Term.title()
                if int == 4: team_Term = team_Term.capitalize()
                self.search_Terms.append(team_Term)
                pass
            if rng == 9: # Iphone
                iphone_Term = sub('5', choice(iphone_terms), choice(iphones))
                int = randint(1,4)
                if int == 1: iphone_Term = iphone_Term.upper()
                if int == 2: iphone_Term = iphone_Term.lower()
                if int == 3: iphone_Term = iphone_Term.title()
                if int == 4: iphone_Term = iphone_Term.capitalize()
                self.search_Terms.append(iphone_Term)
                pass
            if rng == 10: # Prefixes
                prefix_Term = sub('5', choice(prefix_terms), choice(prefixes))
                int = randint(1,4)
                if int == 1: prefix_Term = prefix_Term.upper()
                if int == 2: prefix_Term = prefix_Term.lower()
                if int == 3: prefix_Term = prefix_Term.title()
                if int == 4: prefix_Term = prefix_Term.capitalize()
                self.search_Terms.append(prefix_Term)
                pass
            if rng == 11: # Cities
                Cities_Term = sub('5', choice(cities_terms), choice(cities))
                int = randint(1,4)
                if int == 1: Cities_Term = Cities_Term.upper()
                if int == 2: Cities_Term = Cities_Term.lower()
                if int == 3: Cities_Term = Cities_Term.title()
                if int == 4: Cities_Term = Cities_Term.capitalize()
                self.search_Terms.append(Cities_Term)
                pass  
            if rng == 12: # Airport Codes
                airport_Code_Term = sub('5', choice(airport_code_terms), choice(airport_Codes))
                int = randint(1,4)
                if int == 1: airport_Code_Term = airport_Code_Term.upper()
                if int == 2: airport_Code_Term = airport_Code_Term.lower()
                if int == 3: airport_Code_Term = airport_Code_Term.title()
                if int == 4: airport_Code_Term = airport_Code_Term.capitalize()
                self.search_Terms.append(airport_Code_Term)
                pass
            if rng == 13: # Airport Names
                airport_Name_Term = sub('5', choice(airport_name_terms), choice(airport_Names))
                int = randint(1,4)
                if int == 1: airport_Name_Term = airport_Name_Term.upper()
                if int == 2: airport_Name_Term = airport_Name_Term.lower()
                if int == 3: airport_Name_Term = airport_Name_Term.title()
                if int == 4: airport_Name_Term = airport_Name_Term.capitalize()
                self.search_Terms.append(airport_Name_Term)
                pass
            
        self.search_Terms = set(self.search_Terms)
        self.search_Terms = list(self.search_Terms)
        print(self.search_Terms)
        exit()
    def sts(self, set, instance):

        # 10 - 15 daily searches
        
        terms = list(self.search_Terms)
        st_Length = len(terms)
        ct_Allocation = st_Length / self.accounts_Using
        ct_Allocation = round(ct_Allocation)
        ct_End = ct_Allocation * set
        ct_Start = ct_End - ct_Allocation
        split_Terms = terms[int(ct_Start):int(ct_End)]
        if instance == 1:
            return split_Terms[0:5]
        if instance == 2:
            return split_Terms[5:10]
        if instance == 3:
            return split_Terms[10:15]
        if instance == 4:
            return split_Terms[15:20]
        if instance == 5:
            return split_Terms[20:25]

    def chrome_Search_Ctrl(self, username, password, searches, set, iter):
        _ = chrome_Instances()
        bot = _.get_Browser()

        def action_wait_to_load(xpath):
            try:
                WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                print("Element not visible time'd out")
                bot.refresh()

        def send_input(xpath, input, input2=None):
            action_wait_to_load(xpath=xpath)
            el = bot.find_element_by_xpath(xpath)
            el.send_keys(input)
            if input2 != None:
                el.send_keys(input2)

        def send_click(xpath):
            action_wait_to_load(xpath=xpath)
            bot.find_element_by_xpath(xpath).click()

        bot.get(f"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253ftoWww%253d1%2526redig%253dAF8B0709957742A59F1C53FD761AD3DA%2526wlexpsignin%253d1%26sig%3d044D59BFAF21608C38B14956AEBE617B&wp=MBI_SSL&lc=1033&CSRFToken=cc871eeb-d801-4a42-bcff-4826edd0f1f0&aadredir=1")
        send_input(f"//input[@type='email']", username, Keys.RETURN)
        send_input(f"//input[@type='password']", password, Keys.RETURN)
        send_click(f"//input[@type='button']")
        action_wait_to_load(f"//input[@type='search']")
        for term in searches:
            bot.get(f"https://www.bing.com/search?q="+term)
            action_wait_to_load(f"/html/body/header/nav")
            sleep(3)
    
    def main(self):
        if __name__ == '__main__':
            self.data,processes = [],[]
            for w in range(self.accounts_Using):
                x = w + 1
                for y in range(3): 
                    z = y + 1
                    temp = (self.account_Email_List[w], self.account_Password_List[w], self.sts(x,z), x, z)
                    self.data.append(temp)
            for tuple in self.data:
                y = Process(target=self.chrome_Search_Ctrl,args=tuple)
                y.start()
                processes.append(y)
            for item in processes:
                item.join()

    def dailies(username,password,set,iter):
        #open_offers = self.browser.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
        pass

MSRA = Microsoft_Rewards_Automation()
MSRA.main()
