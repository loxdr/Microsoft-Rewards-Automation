from os.path import isfile
from sys import exit, platform
from json import load, loads
from selenium import webdriver
from datetime import datetime, timedelta
from time import sleep
#from selenium.webdriver.chrome.options import Options <-- Future headless support
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
import requests
from requests.exceptions import RequestException

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
        options.add_argument('--headless')
        if self.os == 'Windows':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver.exe", chrome_options=options)
        if self.os == 'Mac':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver", chrome_options=options)
        if self.os == 'Linux':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver-linux", chrome_options=options)

    def action_get(self, url):
        self.browser.get(url)
    
    def action_click(self, xpath):
        temp = self.browser.find_element_by_xpath(xpath=xpath)
        temp.click()
    
    def action_key(self, xpath, keys):
        temp = self.browser.find_element_by_xpath(xpath=xpath)
        temp.send_keys(keys)
    
    def action_wait_to_load(self, xpath):
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

class Microsoft_Rewards_Automation():
    def __init__(self):
        # Variables
        self.ci_1 = []
        self.ci_2 = []
        self.ci_3 = []
        self.ci_4 = []
        self.ci_5 = []
        self.accounts_Using = 5
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

    def search_Term_Generation(self):
        dates = []
        for i in range(0, 5):
            date = datetime.now() - timedelta(days=i)
            dates.append(date.strftime('%Y%m%d'))
        for date in dates:
            try:
                url = f'https://trends.google.com/trends/api/dailytrends?hl=en-US&ed={date}&geo=US&ns=15'
                request = requests.get(url)
                response = loads(request.text[5:])
                for topic in response['default']['trendingSearchesDays'][0]['trendingSearches']:
                    self.search_Terms.append(topic['title']['query'].lower())
                    for related_topic in topic['relatedQueries']:
                        self.search_Terms.append(related_topic['query'].lower())
                sleep(randint(1, 3))
                print("Starting")
            except RequestException:
                print('Error retrieving google trends json.')
        self.search_Terms = set(self.search_Terms)
    
    def sts(self, set, instance):
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

MSRA = Microsoft_Rewards_Automation()