from os import chmod
from os.path import isfile
from sys import exit, platform
from json import load
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options <-- Future headless support
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import threading

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
        if self.os == 'Windows':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver.exe")
        if self.os == 'Mac':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver")
        if self.os == 'Linux':
            self.browser = webdriver.Chrome(executable_path=r"src/Support-Files/chromedriver-linux")

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
        self.data_Management()
        self.platform_Checker()

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

    def chrome_Ctrl(self):
        chrome_ac1_1 = []
        chrome_ac1_2 = []
        chrome_ac2_1 = []
        chrome_ac2_2 = []
        chrome_ac3_1 = []
        chrome_ac3_2 = []
        chrome_ac4_1 = []
        chrome_ac4_2 = []
        chrome_ac5_1 = []
        chrome_ac5_2 = []
        
        for i in range(5):
            chrome_ac1_1.append(chrome_Instances()) 
        

MSRA = Microsoft_Rewards_Automation()
MSRA.chrome_Ctrl()