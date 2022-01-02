from datetime import datetime
from json import dump, load, loads
from shutil import rmtree

from multiprocessing import Process, Queue
from os import path, mkdir
from os.path import isfile
from random import choice, randint
from re import search, sub
from sys import exit, platform
from time import sleep, time

from discord_webhook import DiscordEmbed, DiscordWebhook
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        ElementNotVisibleException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException,
                                        WebDriverException,
                                        StaleElementReferenceException
                                        )
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Support_Files.driver_update import download_driver
from Support_Files.send_email import send_email


class chrome_Instances():
    def __init__(self, agent, headless = False):
        self.agent = agent
        self.headless = headless
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
        if self.headless:
            options.add_argument('--headless')
        options.add_argument(f"user-agent={self.agent}")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-crash-reporter")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")
        if self.os == 'Windows':
            self.browser = webdriver.Chrome(executable_path=r"Chromedriver/chromedriver.exe", options=options)
        if self.os == 'Mac':
            self.browser = webdriver.Chrome(executable_path=r"Chromedriver/chromedriver", options=options)
        if self.os == 'Linux':
            self.browser = webdriver.Chrome(executable_path=r"Chromedriver/chromedriver", options=options)
        return self.browser
    
    def get_Browser(self):
        return self.browser
    
class Microsoft_Rewards_Automation():
    def __init__(self):
        self.search_Terms = []
        self.daily_links = []
        self.stats = []
        self.chromedriver_Version = None
        self.accounts_Using = None
        self.accounts_Using = 0
        self.search_clients = 5
        self.daily_clients = 1
        self.max_retries = 2
        self.retries = 0
        self.max_signin_retries = 3
        self.signin_retries = 0
        self.headless = True
        self.webhook_Emoji = ['<:greencheck:854879476693467136>', '<:redcross:854879487129157642>']
        self.platform_Checker()
        self.chrome_Management()
        self.search_Term_Generation()
        self.data_Management()

    # Program Init
    def platform_Checker(self):
        """
            Checks what the platform is
        """
        self.platform = platform
        if self.platform == "linux" or self.platform == "linux2":
            self.os = "Linux"
        elif self.platform == "darwin":
            self.os = "Mac"
        elif self.platform == "win32":
            self.os = "Windows"

    def data_Management(self):
        """Checks if support files are present and correctly formatted
        """
        def error(string = 'Steps to run this bot'):
            print("\033[1m" + f"\n  >> {string}" + "\033[0m")
            sleep(1)
            print("  1) Open the newly generated data.json file")
            sleep(1.5)
            print("  2) Fill in as many accounts as you like")
            sleep(1)
            print("  2a) Make sure to follow the correct structure")
            sleep(1)
            print("  2b) It is shown in the readme and in the json file")
            sleep(1)
            print("  2c) Make sure to include commas in the correct areas")
            sleep(1)
            print("  3) Relaunch this program")
            sleep(10)
            exit()
        print("Checking if data.json exists")
        if isfile('data.json') != True:
            try:
                print('Doesnt exist. Creating File')
                with open("data.json", "w") as f:
                    print('Created file')
                    template = {
                        "MS Rewards Accounts":[
                            {"Email": "email@example.com", "Password": "example"},
                            {"Email": "email@example.com", "Password": "example"},
                            {"Email": "email@example.com", "Password": "example"}],
                        "General Config":[
                            {"Discord_Webhook_URL": ""}]}
                    dump(template, f, indent=4)
                with open('LICENCE', 'w') as f:
                    f.write('''MIT License
Copyright (c) 2021 loxdr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''
)
            except PermissionError:
                print("Unable to create file: Dont have required permissions")
                exit()
            error()
        else:
            jam = False
            print('File exists')
            with open("data.json") as r:
                try:
                    self.json_File = load(r)
                    for p in range(len(self.json_File["MS Rewards Accounts"])):
                        x = self.json_File["MS Rewards Accounts"][p]['Email']
                        if x == 'email@example.com':
                            jam = True
                            error("Make sure to fill in the json file")
                    self.accounts_Using = len(self.json_File["MS Rewards Accounts"])
                except:
                    if jam:
                        exit()
                    else:
                        print('File formatted incorrectly')
                        with open("data.json", "w") as f:
                            template = {
                                "MS Rewards Accounts":[
                                    {"Email": "email@example.com", "Password": "example"},
                                    {"Email": "email@example.com", "Password": "example"},
                                    {"Email": "email@example.com", "Password": "example"}],
                                "General Config":[
                                    {"Discord_Webhook_URL": ""}]}
                            dump(template, f, indent=4)
                        error('Make sure to format the json file correctly')
        print('Checking if \'log\' directory exists')
        if path.isdir('log'):
            if path.isfile('stash.json'):
                print('Found log folder and stash.json file')
        else:
            print('\'log\' directory does not exist')
            mkdir('log')
            print('Creating log directory and stash.json file')
            with open('log/stash.json', 'x') as f:
                f.close()
        print(f'MSRA Ready: Using {len(self.json_File["MS Rewards Accounts"])} account (s)')
        for i in self.json_File['MS Rewards Accounts']: print(i['Email'])
    
    def chrome_Management(self):
        """
            Deletes all Chromedriver files and Reinstalls latest version
        """
        print('Attempting to delete Chromedriver')
        try: 
            rmtree('Chromedriver')
            print('Deleted Chromedriver')
        except OSError:
            pass
        except: 
            print('Failed Deleting Chromedriver, check permissions or anti-virus')
            exit()
        print('Rebuilding Chromedriver Directory')
        try:
            mkdir('Chromedriver')
            print('Rebuilt Chromedriver Directory')
        except:
            print('Failed Creating Chromedriver Directory, check permissions or anti-virus')
            exit()
        print('Reinstalling latest version of Chromedriver')
        if self.os == "Linux":
            res = download_driver(r'Chromedriver/chromedriver', self.os)
        if self.os == "Mac":
            res = download_driver(r'Chromedriver/chromedriver', self.os)
        if self.os == "Windows":
            res = download_driver(r'Chromedriver\chromedriver.exe', self.os)
        if res[0]:
            print('Succesfully reinstalled Chromedriver')
            print(f'Using version {res[1]} of Chromedriver')
            self.chromedriver_Version = res[1]
        else:
            print("Failed installing Chromedriver, check permissions or anti-virus")
    # Program Init
         
    # Search              
    def search_Term_Generation(self):
        words = ["What is the definition of 5", '5', "Etymology of 5", "What is the meaning of 5", "What country did the word 5 come from?", "What are some synonyms of 5", "What are some antonyms of 5", "Synonym of 5", "Antonym of 5", "Meaning of 5", "Where did the word 5 come from?"]
        maths = ["What is the answer to: 5", "How do you solve: 5", "5 is equal to", "5"]
        maths_signs = ['*', '/', "+", '-', ' plus ', ' minus ', ' times ', ' divided by ', ' over ', ' to the power of ']
        movies = ['Who are the main actors in 5', 'Who is the main character in 5', 'What is the plot of 5', 'When was 5 released', 'When was the movie 5 released', '5','Who produced 5', 'What is the storyine in 5', 'How is the plot resolved in 5']
        states = ['Where is 5', 'Pictures of 5', 'Who is the governer of 5', 'Whats the area of 5', '5 election', 'Who is the home NFL team for 5', 'What are the attractions in 5', '5', 'who are the native people in 5', 'Whats the capital of 5']
        names = ['Which country is the name 5 from', 'How popular is 5', 'Origin of the name 5', 'Is the name 5 popular', 'Names like 5', 'Other names like 5', '5']
        countries = ['Where is 5', 'Pictures of 5', 'What is the currency in 5', 'What is the annual inflation rate for 5', 'Currency of 5', 'What are the neiboring countries of 5', 'Nearest country of 5', 'Capital of 5', 'Government of 5', 'Average internet speed in 5']
        mountains = ['Where is 5 located', 'Pictures of 5', 'Latitude and Longitude of the mountain 5','What country is 5 in', 'What is the height of 5', 'What is the width of 5', 'Time to climb 5', 'Has anyone died climbing 5', 'Altitude of 5', '5']
        teams = ['Score for 5', 'Pictures of 5', 'Where is 5 on the ladder', 'Ladder 5', '5', 'Top five players in 5', 'Average pay of player in 5', 'Most popular player in 5', 'Highest paid player in 5', '5 goalkeeper']
        cities = ['Where is 5', 'Pictures of 5', 'What continent is 5', 'Whats the population of 5', 'How many pepole live in 5', 'Average household size in 5']
        airport_Codes = ['Airport data for 5', 'Whats the active runway for 5', 'When was 5 made', 'Who operates 5', 'Operation time of 5', 'Open hours of 5', 'Open date of 5', 'What airlines fly to 5', 'Airport charts for 5']
        airport_Names = ['Airport data for 5', 'Pictures of 5', 'Whats the active runway for 5', 'When was 5 made', 'Who operates 5', 'Operation time of 5', 'Open hours of 5', 'Open date of 5', 'What airlines fly to 5', 'Airport charts for 5']
        iphones = ['When was the 5 released', 'Pictures of 5', 'Camera quality of the 5', '5', 'Battery life of the 5', 'Screen size of the 5', 'Screen replacement for 5', 'ifixit.com 5']
        prefixes = ['What is the meaning of 5', '5', 'Metric prefix 5', 'What number is 5', '5 in numbers']
        movies_terms, states_terms, cities_terms, prefix_terms, words_terms, teams_terms, names_terms, country_terms, mountain_terms, iphone_terms, airport_code_terms, airport_name_terms = [], [], [], [], [], [], [], [], [], [], [], []
        print("Generating Search Terms")
        with open('Dictionaries/movies.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                movies_terms.append(i)
        with open('Dictionaries/states.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                states_terms.append(i)
        with open('Dictionaries/words.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                words_terms.append(i)
        with open('Dictionaries/names.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                names_terms.append(i)
        with open('Dictionaries/countries.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                country_terms.append(i)
        with open('Dictionaries/mountains.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                mountain_terms.append(i)
        with open('Dictionaries/teams.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                teams_terms.append(i)
        with open('Dictionaries/phones.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                iphone_terms.append(i)
        with open('Dictionaries/prefixes.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                prefix_terms.append(i)
        with open('Dictionaries/cities.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                cities_terms.append(i)
        with open('Dictionaries/airport_Names.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                airport_name_terms.append(i)
        with open('Dictionaries/airport_Codes.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for i in lines:
                i = sub('\n', '', i)
                airport_code_terms.append(i)
        
        while len(self.search_Terms) < 750:
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

    def sts(self, set, instance, mobile = False):
        ct_Allocation = len(list(self.search_Terms)) / self.accounts_Using
        ct_Allocation = round(ct_Allocation)
        ct_End = ct_Allocation * set
        ct_Start = ct_End - ct_Allocation
        split_Terms = list(self.search_Terms)[int(ct_Start):int(ct_End)]
        if mobile == True:
            return split_Terms[60:90]
        if mobile != True:
            if instance == 1:
                return split_Terms[0:20]
            if instance == 2:
                return split_Terms[20:40]
            if instance == 3:
                return split_Terms[40:60]
        
    def search_Handler(self, username, password, searches, set, iter, mobile = False, edge = False, headless = True):
        mobile_Agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1']
        edge_Agents = ['Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136']
        desktop_Agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36']
        if mobile == True:
            device = 'mobile'
            chrome = chrome_Instances(choice(mobile_Agents), headless)
        if edge == True:
            device = 'edge'
            chrome = chrome_Instances(choice(edge_Agents), headless)
        if edge != True and mobile != True: 
            device = 'desktop'
            chrome = chrome_Instances(choice(desktop_Agents), headless)
        bot = chrome.get_Browser()
        
        def action_wait_to_load(xpath):
            try:
                WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                bot.refresh()
                sleep(5)

        def laction_wait(xpath):
            try:
                WebDriverWait(bot, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return False
            except (TimeoutException, UnexpectedAlertPresentException):
                return True

        def action_wait_to_go(xpath):
            try:
                WebDriverWait(bot, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                sleep(5)
        
        def send_input(xpath, input, input2=None):
            action_wait_to_load(xpath=xpath)
            el = bot.find_element_by_xpath(xpath)
            el.send_keys(input)
            if input2 != None:
                el.send_keys(input2)

        def send_click(xpath):
            action_wait_to_load(xpath=xpath)
            bot.find_element_by_xpath(xpath).click()  

        def signin():
            bot.get(f"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253ftoWww%253d1%2526redig%253dAF8B0709957742A59F1C53FD761AD3DA%2526wlexpsignin%253d1%26sig%3d044D59BFAF21608C38B14956AEBE617B&wp=MBI_SSL&lc=1033&CSRFToken=cc871eeb-d801-4a42-bcff-4826edd0f1f0&aadredir=1")
            send_input(f"//input[@type='email']", username, Keys.RETURN)
            send_input(f"//input[@type='password']", password, Keys.RETURN)
            for _ in range(3):
                sleep(2)
                x = laction_wait(f"//input[@type='button']")
                if x: break
                if x != True: send_click(f"//input[@type='button']")
            for _ in range(2):
                x = laction_wait(f'/html/body/div[5]/div[2]/button')
                if x: break
                if x != True: send_click(f'/html/body/div[5]/div[2]/button')
        
        def search(username): 
            for term in searches:
                # print(f'{username} searching with term: {term}')
                bot.get(f"https://www.bing.com/search?q="+term)
                bot.implicitly_wait(1)
                action_wait_to_go(f'//*[@id="sb_form_q"]')
                bot.implicitly_wait(1)
                html = bot.find_element_by_tag_name('html')
                for _ in range(1):
                    try:
                        html.send_keys(Keys.END)
                        sleep(1)
                        html.send_keys(Keys.HOME)
                        sleep(1)
                    except (StaleElementReferenceException, ElementNotInteractableException):
                        sleep(3)
            # print(f'{username} {device} {iter} Finished searches')
        
        # print(f'Starting Searches {username} {device} {iter}')
        signin()
        search(username) 
    # Search

    # Daily Challenges
    def dailies_Handler(self, username, password, set, iter, headless = False):
        desktop_Agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36']
        chrome = chrome_Instances(choice(desktop_Agents), headless)
        bot = chrome.get_Browser()
        
        def action_wait_to_load(xpath):
            try:
                WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                bot.refresh()
                sleep(5)

        def laction_wait(xpath):
            try:
                WebDriverWait(bot, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return False
            except (TimeoutException, UnexpectedAlertPresentException):
                return True

        def find_id(obj):
            return bot.find_elements_by_id(obj)

        def find_class(obj):
            return bot.find_elements_by_class_name(obj)
        
        def find_css(selector):
            return bot.find_elements_by_css_selector(selector)

        def click_class(selector):
            try:
                bot.find_element_by_class_name(selector).click()
            except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
                print(f'Send key by class to {selector} element not visible or clickable.')
            except WebDriverException:
                print(f'Webdriver Error for send key by class to {selector} object')

        def wait_until_visible(by_, selector, time_to_wait=10):
            start_time = time()
            while (time() - start_time) < time_to_wait:
                if bot.find_elements(by=by_, value=selector):
                    return True
                bot.refresh()  # for other checks besides points url
                sleep(2)
            return False

        def wait_until_clickable(by_, selector, time_to_wait=10):
            try:
                WebDriverWait(bot, time_to_wait).until(EC.element_to_be_clickable((by_, selector)))
            except (TimeoutException, UnexpectedAlertPresentException):
                print(f'{selector} element Not clickable - Timeout Exception')
                raise
            except WebDriverException:
                print(f'Webdriver Error for {selector} object')
                bot.refresh()
        
        def click_id(obj):
            try:
                bot.find_element_by_id(obj).click()
            except(ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
                print('Click by ID: element not visible or clickable')
            
        def action_wait_to_go(xpath):
            try:
                WebDriverWait(bot, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                sleep(5)
        
        def send_input(xpath, input, input2=None):
            action_wait_to_load(xpath=xpath)
            el = bot.find_element_by_xpath(xpath)
            el.send_keys(input)
            if input2 != None:
                el.send_keys(input2)

        def send_click(xpath):
            action_wait_to_load(xpath=xpath)
            bot.find_element_by_xpath(xpath).click()  

        def switch_to(window = -1):
            handles = bot.window_handles
            bot.switch_to.window(handles[window])

        def switch_back(window = 0):
            handles = bot.window_handles
            bot.switch_to.window(handles[window])

        def sign_In():
            bot.get(f'https://rewards.microsoft.com/Signin?idru=%2F')
            send_input(f"//input[@type='email']", username, Keys.RETURN)
            send_input(f"//input[@type='password']", password, Keys.RETURN)
            for _ in range(3):
                sleep(2)
                x = laction_wait(f"//input[@type='button']")
                if x: break
                if x != True: send_click(f"//input[@type='button']")
            for _ in range(2):
                x = laction_wait(f'/html/body/div[5]/div[2]/button')
                if x: break
                if x != True: send_click(f'/html/body/div[5]/div[2]/button')
        
        # Different Task Operations
        def task_Explore():
            try:
                html = bot.find_element_by_tag_name('html')
                for i in range(2):
                    html.send_keys(Keys.END)
                    sleep(0.75)
                    html.send_keys(Keys.HOME)
                    sleep(0.75)
                close_Window()
                switch_back()
            except TimeoutException:
                print('Explore Daily Timeout Exception.')
            except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
                print('Element not clickable or visible.')
            except WebDriverException:
                print('Error.')

        def task_Poll():
            choices = ['btoption0', 'btoption1']
            click_id(choice(choices))
            sleep(1)
            close_Window()
            switch_back()

        def task_Drag_Drop():
            def get_options_for_drag_drop():
                drag_options = find_class('rqOption')
                right_answers = find_class('correctAnswer')
                if right_answers:
                    drag_options = [x for x in drag_options if x not in right_answers]
                return drag_options
            
            for _ in range(100):
                if find_id('quizCompleteContainer'):
                    break
                drag_options = get_options_for_drag_drop()
                if not drag_options:
                    continue
                try:
                    choice_a = choice(drag_options)
                    drag_options.remove(choice_a)
                    choice_b = choice(drag_options)
                    ActionChains(bot).drag_and_drop(choice_a, choice_b).perform()
                except (WebDriverException, TypeError):
                    print('Unknown Error.')
                    continue
                sleep(1)

            sleep(0.1)
            close_Window()
            switch_back()

        def task_Lightning():
            for question_round in range(10):
                print(f'Round# {question_round}')
                if find_id('rqAnswerOption0'):
                    sleep(3)
                    for i in range(10):
                        if find_id(f'rqAnswerOption{i}'):
                            bot.execute_script(
                                f"document.querySelectorAll('#rqAnswerOption{i}').forEach(el=>el.click());")
                            print(f'Clicked {i}')
                            sleep(2)
                # let new page load
                sleep(1)
                if find_id('quizCompleteContainer'):
                    break
            close_Window()
            switch_back()

        def task_Click():
            while True:
                try:
                    if find_css('span[class="rw_icon"]'):
                        break
                    if find_css('.cico.btCloseBack'):
                        find_css('.cico.btCloseBack')[0].click()[0].click()
                        print('Quiz popped up during a click quiz...')
                    
                    choices = find_class('wk_Circle')
                    # click answer
                    if choices:
                        choice(choices).click()
                        sleep(3)
                    # click the 'next question' button
                    # wait_until_clickable(By.ID, 'check', 10)
                
                    wait_until_clickable(By.CLASS_NAME, 'wk_button', 10)
                    # click_by_id('check')
                    click_class('wk_button')
                    # if the green check mark reward icon is visible, end loop
                    sleep(3)
                    if find_css('span[class="rw_icon"]'):
                        break
                except:
                    break
            close_Window()
            switch_back()
        # Different Task Operations

        def test_Sign_In(dailies, number):
            sign_in_msg = find_class('simpleSignIn')
            if sign_in_msg:
                if self.max_signin_retries < self.signin_retries:
                    print(f"Could not complete sign in: retried to many times. Activity: {dailies[number]}")
                else:
                    close_Window()
                    switch_back()
                    self.signin_retries += 1
                    dailies[number].click()
                    switch_to()
                    sleep(5)
                    test_Sign_In(dailies, number)

        def close_Window():
            if bot.title == 'Rewards Dashboard':
                pass
            else:
                bot.close()

        def task_Function():
            dailies = bot.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
            number = -1
            for link in dailies:
                number += 1
                link.click()
                switch_to()
                sleep(5)
                test_Sign_In(dailies, number)
                if find_id('btoption0'):
                    print('Daily Poll Found')
                    task_Poll()
                elif find_id('rqStartQuiz'):
                    click_id('rqStartQuiz')
                    if find_id('rqAnswerOptionNum0'):
                        print('Drag and Drop Quiz identified')
                        task_Drag_Drop()
                    elif find_id('rqAnswerOption0'):
                        print('Lightning Quiz identified')
                        task_Lightning()
                elif find_class('wk_Circle'):
                    print('Click Quiz identified')
                    task_Click()
                else:
                    print('Generic Explore identified')
                    task_Explore()
                sleep(4)
                close_Window()
                switch_back()
            dailies = bot.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
            if dailies == []:
                print('Finished Dailies')
            else:
                if self.retries > self.max_retries:
                    print(f"Could not complete dailies: {len(dailies)} offers remaining")
                else:
                    self.retries += 1
                    task_Function()

        sign_In()
        task_Function()
    # Daily Challenges

    # Stat Generator
    def stat_Handler(self, username, password, position, queue, headless = True):
        """
            Position is either 1 or 0. 0 Being that it is the count before and 1 being the count after
            Returns: username, level, profile_points, pc_points, mobile_points, quiz_points, position
        """
        def action_wait_to_load(xpath):
            try:
                WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            except (TimeoutException, UnexpectedAlertPresentException):
                bot.refresh()
                sleep(5)

        def laction_wait(xpath):
            try:
                WebDriverWait(bot, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return False
            except (TimeoutException, UnexpectedAlertPresentException):
                return True
        
        def send_input(xpath, input, input2=None):
            action_wait_to_load(xpath=xpath)
            el = bot.find_element_by_xpath(xpath)
            el.send_keys(input)
            if input2 != None:
                el.send_keys(input2)

        def send_click(xpath):
            action_wait_to_load(xpath=xpath)
            bot.find_element_by_xpath(xpath).click()  
  
        def sign_In():
            bot.get(f'https://rewards.microsoft.com/Signin?idru=%2F')
            send_input(f"//input[@type='email']", username, Keys.RETURN)
            send_input(f"//input[@type='password']", password, Keys.RETURN)
            for _ in range(3):
                sleep(2)
                x = laction_wait(f"//input[@type='button']")
                if x: break
                if x != True: send_click(f"//input[@type='button']")
            for _ in range(2):
                x = laction_wait(f'/html/body/div[5]/div[2]/button')
                if x: break
                if x != True: send_click(f'/html/body/div[5]/div[2]/button')
        
        # Stat Generation
        def get_user_stats():
            js = bot.find_elements_by_xpath(
                '//script[text()[contains(., "userStatus")]]')
            if not js:
                return {}

            matches = search(
                r'(?=\{"userStatus":).*(=?\}\};)', js[0].get_attribute('text'))
            if not matches:
                return {}
            return loads(matches[0][:-1])

        def get_user_lvl(json):
            if json['userStatus']['levelInfo']['levels'][0]['active'] == True:
                # print('   User is Level 1')
                pass
                return 1
            else:
                return 2

        def get_pts_lvl(json):
            if 'userStatus' not in json:
                # print('   Cannot find key "userStatus"')
                pass
                return
            current_pts_lvl = json['userStatus']
            current_pts_lvl = int(current_pts_lvl['availablePoints'])
            # print(f'   Current points level: {str(current_pts_lvl)}')
            return current_pts_lvl
        
        def get_pts_pc(json):
            if 'pcSearch' not in json['userStatus']['counters']:
                # print('   Cannot find daily point levels: PC Search')
                pass
            pc_search = json['userStatus']['counters']['pcSearch'][0]
            pc_points = pc_search['pointProgress']
            pc_max_points = pc_search['pointProgressMax']
            pc_search = f'{str(pc_points)} / {str(pc_max_points)}'
            if pc_max_points == pc_points:
                # print(f'   Bot has generated max search points for today: {pc_search}')
                pass
            else:
                # print(f'   Current search points level: {str(pc_search)}')
                pass
            return pc_search

        def get_pts_quiz(json):
            if 'dailySetPromotions' not in json:
                # print("   Cannot find daily point levels: Daily Quiz")
                pass
            if 'morePromotions' not in json:
                # print("   Cannot find daily point levels: More Quiz")
                pass
            today = f'{datetime.now():%m/%d/%Y}'
            quiz_points = 0
            quiz_max_points = 0
            for daily in json['dailySetPromotions'][today]:
                quiz_points += int(daily['pointProgress'])
                quiz_max_points += int(daily['pointProgressMax'])
            for daily in json['morePromotions']:
                quiz_points += int(daily['pointProgress'])
                quiz_max_points += int(daily['pointProgressMax'])
            quiz = f'{str(quiz_points)} / {str(quiz_max_points)}'
            if quiz_points == quiz_max_points:
                # print(f'   Bot has generated max quiz points for today: {quiz}')
                pass
            else:
                # print(f'   Current quiz points level: {str(quiz)}')
                pass
            return quiz
            
        def get_pts_mobile(json):
            if 'mobileSearch' not in json['userStatus']['counters']:
                # print('   No mobile points as account is level 1')
                return 'N/A'
            mbs = json['userStatus']['counters']['mobileSearch'][0]
            mobile_search_progress = int(mbs['pointProgress'])
            mobile_search_max = int(mbs['pointProgressMax'])
            mobile_search = f'{str(mobile_search_progress)} / {str(mobile_search_max)}'
            if mobile_search == mobile_search_max:
                # print(f'   Bot has generated max mobile search points for today: {mobile_search}')
                pass
            else:
                # print(f'   Current mobile search points level: {str(mobile_search)}')
                pass
            return mobile_search   
        # Stat Generation

        print(f"Generating point levels: {username}")
        desktop_Agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36']
        chrome = chrome_Instances(choice(desktop_Agents), headless)
        bot = chrome.get_Browser()
        sign_In()

        f = get_user_stats()
        level = get_user_lvl(f)
        profile_points = get_pts_lvl(f)
        pc_points = get_pts_pc(f)
        mobile_points = get_pts_mobile(f)
        quiz_points = get_pts_quiz(f)

        x = [username, level, profile_points, pc_points, mobile_points, quiz_points, position]
        print(f"Putting {username} data into queue")
        queue.put(x)
    # Stat Generator

    # Main Function
    def processor(self, Searches = True, Dailies = True, Stats=False):
        def stats(position, queue):
            temp_data, processes = [], []
            for w in range(self.accounts_Using):
                x = (self.json_File['MS Rewards Accounts'][w]['Email'], self.json_File['MS Rewards Accounts'][w]['Password'], position, queue, self.headless)
                temp_data.append(x)
            for data in temp_data:
                y = Process(target=self.stat_Handler,args=data)
                y.start()
                processes.append(y)
            for item in processes:
                item.join()
            while not queue.empty():
                self.stats.append(queue.get())
        
        def stat_Splitter():
            """
            Returns: username, level, profile_points, pc_points, mobile_points, quiz_points, position
            """
            for i in range(len(self.stats)):
                username = self.stats[i][0]
                level = self.stats[i][1]
                points = self.stats[i][2]
                pc_Points = self.stats[i][3]
                mobile_Points = self.stats[i][4]
                quiz_Points = self.stats[i][5]
                position = self.stats[i][6]
                x = [username, level, points, pc_Points, mobile_Points, quiz_Points]
                if position == 0:
                    Lol = []
                    before_Stats.append(Lol)
                    before_Stats[i].append(x)
                elif position == 1:
                    Lol = []
                    after_Stats.append(Lol)
                    after_Stats[i].append(x)

        def searches():
            # Searches
            search_data, processes = [],[]
            for w in range(self.accounts_Using):
                x = w + 1
                print(f"Starting Searching For {self.json_File['MS Rewards Accounts'][w]['Email']}")
                for y in range(self.search_clients):
                    rang = y + 1  
                    if rang != 4 or rang != 5 : # Desktop
                        temp = (self.json_File['MS Rewards Accounts'][w]['Email'], self.json_File['MS Rewards Accounts'][w]['Password'], self.sts(x,rang), x, rang, False, False, self.headless)    
                    if rang == 4: # Mobile
                        temp = (self.json_File['MS Rewards Accounts'][w]['Email'], self.json_File['MS Rewards Accounts'][w]['Password'], self.sts(x,rang, mobile=True), x, rang, True, False, self.headless)
                    if rang == 5: # Edge
                        temp = (self.json_File['MS Rewards Accounts'][w]['Email'], self.json_File['MS Rewards Accounts'][w]['Password'], self.sts(x,rang, mobile=True), x, rang, False, True, self.headless)
                    search_data.append(temp)
            for tuple in search_data:
                y = Process(target=self.search_Handler, args=tuple)
                y.start()
                processes.append(y)
            for item in processes:
                item.join()

        def dailies():
            # Daily Challenges
            daily_data,processes = [], []
            for w in range(self.accounts_Using):
                print(f"Starting Dailies For {self.json_File['MS Rewards Accounts'][w]['Email']}")
                for y in range(self.daily_clients):
                    rang = y + 1  
                    temp = (self.json_File['MS Rewards Accounts'][w]['Email'], self.json_File['MS Rewards Accounts'][w]['Password'], w, rang, self.headless)
                    daily_data.append(temp)
            for tuple in daily_data:
                y = Process(target=self.dailies_Handler,args=tuple)
                y.start()
                processes.append(y)
            for item in processes:
                item.join()

        def webhook_Sender(username, complete_Stats, level, daily_Challenge_Stats, search_Stats_Mobile, search_Stats_PC, point_Stats):
            webhook = DiscordWebhook(url=self.json_File['General Config'][0]['Discord_Webhook_URL'])
            embed = DiscordEmbed(title=f"Account: {username}", description="", color='80b454')
            embed.add_embed_field(name="**Completed:**", value=F"{complete_Stats}", inline=True)
            embed.add_embed_field(name="**Searches - PC:**", value=F"{search_Stats_PC}", inline=True)
            embed.add_embed_field(name="**Searches - Mobile:**", value=F"{search_Stats_Mobile}", inline=True)
            embed.add_embed_field(name="**Daily Challenges:**", value=F"{daily_Challenge_Stats}", inline=True)
            embed.add_embed_field(name="**Level:**", value=F"{level}", inline=True)
            embed.add_embed_field(name="**Current Points:**", value=F"{point_Stats}", inline=True)
            embed.set_footer(text="Status Update")
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()

        queue = Queue()
        before_Stats = []
        after_Stats = []
        stats(0, queue)
        self.stats = []
        if Searches: searches()
        if Dailies: dailies()
        stats(1, queue)
        stat_Splitter()
        for i in after_Stats:
            username = i[0][0]
            complete_Stats = self.webhook_Emoji[0]
            level = i[0][1]
            daily_Challenge_Stats = i[0][5]
            search_Stats_PC = i[0][3]
            search_Stats_Mobile = i[0][4]
            points = i[0][2]
            if Stats: 
                webhook_Sender(username, complete_Stats, level, daily_Challenge_Stats, search_Stats_Mobile, search_Stats_PC, points)
                sleep(2)

if __name__ == '__main__':
    MSRA = Microsoft_Rewards_Automation()
    MSRA.processor(Searches = True, Dailies = True, Stats=False)

    MSRA2 = Microsoft_Rewards_Automation()
    MSRA2.processor(Searches=True, Dailies=True, Stats=True)