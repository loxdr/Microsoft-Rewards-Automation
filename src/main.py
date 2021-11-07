from datetime import datetime, timedelta
from json import load, loads
from multiprocessing import Process
from os.path import isfile
from random import randint
from sys import exit, platform
from time import sleep

from requests import get
from requests.exceptions import RequestException
from selenium import webdriver
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
        self.accounts_Using = 2
        self.search_Terms = []
        
        # Functions
        self.data_Management()
        self.platform_Checker()
        #self.search_Term_Generation()

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
        dates = []
        for i in range(0, 5):
            date = datetime.now() - timedelta(days=i)
            dates.append(date.strftime('%Y%m%d'))
        for date in dates:
            try:
                url = f'https://trends.google.com/trends/api/dailytrends?hl=en-US&ed={date}&geo=US&ns=15'
                request = get(url)
                response = loads(request.text[5:])
                for topic in response['default']['trendingSearchesDays'][0]['trendingSearches']:
                    self.search_Terms.append(topic['title']['query'].lower())
                    for related_topic in topic['relatedQueries']:
                        self.search_Terms.append(related_topic['query'].lower())
                print('generating terms')
                sleep(randint(1, 3))
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

    def chrome_Ctrl(self, username, password, searches, set, iter):
        _ = chrome_Instances()
        bot = _.get_Browser()
        bot.get("https://google.com")
        print(f'Google {set} {iter}')
        bot.get("https://youtube.com")
        print(f'Youtube {set} {iter}')
        bot.get("https://reddit.com")
        print(f'Reddit {set} {iter}')

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
                y = Process(target=self.chrome_Ctrl,args=tuple)
                y.start()
                processes.append(y)
            for item in processes:
                item.join()

MSRA = Microsoft_Rewards_Automation()
MSRA.main() 
