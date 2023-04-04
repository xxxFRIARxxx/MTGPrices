import ijson
import urllib.request
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

interests = "https://www.mtgstocks.com/interests"
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)
driver.get(interests)
market_button = driver.find_element("xpath", "/html/body/app-root/div/div/div/div/div[1]/ng-component/div[2]/div/tabset/ul/li[3]")
market_button.click()

matches = driver.find_element("tag name", "tbody")
matches2 = driver.find_element("css selector", "tbody")
# print(matches.tag_name)
# matches_attrib = matches.get_attribute("tbody")
# print(matches_attrib)
# for match in matches:
#     print(matches.text)
print(matches2.text)
# /html/body/app-root/div/div/div/div/div[1]/ng-component/div[2]/div/tabset/ul/li[3]