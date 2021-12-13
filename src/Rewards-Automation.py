from json import load
from multiprocessing import Process
from os.path import isfile
from random import choice, randint
from re import sub
from sys import exit, platform
from time import perf_counter, sleep

from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
    
class Microsoft_Rewards_Automation():
    def __init__(self):
        self.accounts_Using = None
        self.search_Terms = []

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
                self.accounts_Using = len(data)
                self.account_Data = []
                for i in range(1, self.accounts_Using+1):
                    self.account_Data.append(data[f'Account-{i}'][f'Email-{i}'])
                    self.account_Data.append(data[f'Account-{i}'][f'Password-{i}'])

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
            return split_Terms[60:85]
        if mobile != True:
            if instance == 1:
                return split_Terms[0:20]
            if instance == 2:
                return split_Terms[20:40]
            if instance == 3:
                return split_Terms[40:60]
        
    def search_Handler(self, username, password, searches, set, iter, mobile = False, edge = False):
        mobile_Agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1']
        edge_Agents = ['Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136']
        desktop_Agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36']
        if mobile == True:
            device = 'mobile'
            chrome = chrome_Instances(choice(mobile_Agents))
        if edge == True:
            device = 'edge'
            chrome = chrome_Instances(choice(edge_Agents))
        if edge != True and mobile != True:
            device = 'desktop'
            chrome = chrome_Instances(choice(desktop_Agents))
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
        
        def search():
            for term in searches:
                bot.get(f"https://www.bing.com/search?q="+term)
                action_wait_to_go(f'//*[@id="sb_form_q"]')
                sleep(3)

        signin()
        search() 

    def dailies_Handler(self, username, password, set, iter):
        desktop_Agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36']
        chrome = chrome_Instances(choice(desktop_Agents))
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

        def switch_to(window = -1):
            handles = bot.window_handles
            bot.switch_to_window(handles[window])

        def switch_back(window = 0):
            handles = bot.window_handles
            bot.switch_to_window(handles[window])

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

        def scout():
            dailies = bot.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
            if dailies:
                upper_elements = [new.find_element_by_xpath('..//..//..//..') for new in dailies]
                links = [upper.find_element_by_xpath('div[3]/span') for upper in upper_elements]
                for link in links:
                    print('Detected offer!')
                    link.click()
                    switch_to()
                    sleep(1)
                    switch_back()
                    sleep(1)
                    switch_to()
                    sleep(1)
                    bot.close()
                    switch_back

                    
            
            # open_offers = bot.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
            # for i in open_offers:
            #     print(i)
            # if open_offers:
            #     # get common parent element of open_offers
            #     parent_elements = [open_offer.find_element_by_xpath('..//..//..//..') for open_offer in open_offers]
            #     # get points links from parent, # finds ng-transclude descendant of selected node
            #     offer_links = [parent.find_element_by_xpath('descendant::ng-transclude') for parent in parent_elements]
            # for link in offer_links:
            #         bot.get(link)
            # else:
            #     print('Completed all dailies!')
        
        sign_In()
        scout()
        #open_offers = self.browser.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')

    def processor(self):
        def searches():
            # Signin And Search
            if __name__ == '__main__':
                self.data_search,processes = [],[]
                for w in range(self.accounts_Using):
                    x = w + 1
                    for y in range(5):
                        rang = y + 1  
                        if rang != 4 or rang != 5 : # Desktop
                            temp = (self.account_Data[w*2], self.account_Data[(w*2)+1], self.sts(x,rang), x, rang, False)    
                        if rang == 4: # Mobile
                            temp = (self.account_Data[w*2], self.account_Data[(w*2)+1], self.sts(x,rang, mobile=True), x, rang, True)
                        if rang == 5: # Edge
                            temp = (self.account_Data[w*2], self.account_Data[(w*2)+1], self.sts(x,rang, mobile=True), x, rang, False, True)
                        self.data_search.append(temp)
                for tuple in self.data_search:
                    y = Process(target=self.search_Handler,args=tuple)
                    y.start()
                    processes.append(y)
                for item in processes:
                    item.join()

        def dailies():
            # Daily Challenges
            if __name__ == '__main__':
                self.data_daily,processes = [], []
                for w in range(self.accounts_Using):
                    x = w + 1
                    for y in range(3):
                        rang = y + 1  
                        temp = (self.account_Data[w*2], self.account_Data[(w*2)+1], w, rang)
                        self.data_daily.append(temp)
                for tuple in self.data_daily:
                    y = Process(target=self.dailies_Handler,args=tuple)
                    y.start()
                    processes.append(y)
                for item in processes:
                    item.join()
    
        # searches()
        dailies()

    def notification_Center(self):
        # Point Counter

        # Notification sender ((Discord Webhook, Email) Each includes - (Picture, Points, Status of account))
        status = ['<:greencheck:854879476693467136>', '<:redcross:854879487129157642>']
        def webhook_Sender(username, complete_Stats, general_Stats, sign_In_Stats, search_Stats, daily_Challenge_Stats, search_Gen_Stats, data_File_Manag_Stats, time_Stats, point_Stats):
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/917384579822784513/-R735zyONifkZWkkpa4deStsGu4pkWV4dWQcM9vwBEO8nvSWMJ9px0LacZp-HxdrcYgS')
            embed = DiscordEmbed(title="Microsoft Rewards Automation", description=f"**Account:** *{username}*", color='ffffff')
            embed.add_embed_field(name="**Completed:**", value=F"{complete_Stats}", inline=True)
            embed.add_embed_field(name="**General Status:**", value=F"{general_Stats}", inline=True)
            embed.add_embed_field(name="**Sign in:**", value=F"{sign_In_Stats}", inline=True)
            embed.add_embed_field(name="**Searches:**", value=F"{search_Stats}", inline=True)
            embed.add_embed_field(name="**Daily Challenges:**", value=F"{daily_Challenge_Stats}", inline=True)
            embed.add_embed_field(name="**Search Term Generaton:**", value=F"{search_Gen_Stats}", inline=True)
            embed.add_embed_field(name="**Data & File Management:**", value=F"{data_File_Manag_Stats}", inline=True)
            embed.add_embed_field(name="**Completed task in set time:**", value=F"{time_Stats}", inline=True)
            embed.add_embed_field(name="**Current Points:**", value=F"{point_Stats}", inline=True)
            embed.set_footer(text="Status Update")
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
            #          email                 completed all required tasks        completed with no error             signed with no error                searched with no error              daily challenges with no error      generated searches with no error    managed account info with no error   completed within set time          level of points
        webhook_Sender(self.account_Data[0], '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '<:greencheck:854879476693467136>', '16,323')
MSRA = Microsoft_Rewards_Automation()
MSRA.processor()