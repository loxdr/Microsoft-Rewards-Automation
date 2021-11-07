from concurrent.futures import process
from concurrent.futures.process import ProcessPoolExecutor
import multiprocessing
from os.path import isfile
from sys import exit, platform
from json import load, loads
from selenium import webdriver
from datetime import datetime, timedelta
from time import sleep, perf_counter
from selenium.webdriver.chrome.options import Options #<-- Future headless support
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from requests import get
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
        #options.add_argument('--headless')
        options.add_argument("--disable-logging")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--log-level=3")
        if self.os == 'Windows':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver.exe", options=options)
        if self.os == 'Mac':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver", options=options)
        if self.os == 'Linux':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver-linux", options=options)
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

def chrome_Ctrl(username, password):
    _ = chrome_Instances()
    bot = _.get_Browser()
    bot.get("https://google.com")
    print(f"Username is> {username} Password is> {password}")
    sleep(3)

x = ["eshay1@gmail.com", "Jamie"]
y = ["eshay2@gmail.com", "Mark"]
z = ["eshay3@gmail.com", "Ovski"]
data = [x,y,z]
if __name__ == '__main__':
    processes = []

    for point in data:
        p = multiprocessing.Process(target=chrome_Ctrl,args=point)
        p.start()
        processes.append(p)
    for proces in processes:
        proces.join()
