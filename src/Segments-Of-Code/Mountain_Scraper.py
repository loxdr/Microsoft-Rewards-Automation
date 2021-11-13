from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path=r"src/Support-Files/Chrome-Files/chromedriver")
browser.get('https://github.com/APonce73/Mountains/blob/master/Mountains.csv')
time.sleep(5)
mountains = []
for x in range(2,1337):
    mountain = browser.find_element_by_xpath(f'//*[@id="LC{x}"]/td[4]').text
    mountains.append(mountain)
    print(mountain)
with open('src/Support-Files/Random/mountains.txt', 'a', encoding='UTF-8') as f:
    for i in mountains:
        f.write(f"{i}\n")