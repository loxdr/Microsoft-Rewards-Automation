from datetime import datetime, timedelta
from json import load, loads
from multiprocessing import Process
from os.path import isfile
from random import randint,choice
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
from re import sub

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
        # options.add_argument('--headless')
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

def action_wait_to_load(xpath):
    WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))

_ = chrome_Instances()
bot = _.get_Browser()

# Random Movies
lit = []
movies = []
bot.get("https://www.wordgenerator.net/random-word-generator.php")

while len(movies) < 10000:
    action_wait_to_load('//*[@id="rname"]')
    word = bot.find_element_by_xpath('//*[@id="rname"]').text
    word = word.split()
    if len(word[0]) < 5:
        print('Too Short')
    else:
        print(word[0])
        movies.append(word[0])
    bot.find_element_by_xpath('//*[@id="rnames"]').click()

for i in movies:
    lit.append(i.text)
    
final = set(lit)
print(len(final))
with open('src/Support-Files/Random/words.txt', 'a', encoding='UTF-8') as f:
    for word in list(final):
        f.write(f"{word}\n")