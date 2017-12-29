
from selenium import webdriver

browser = webdriver.Chrome('/Users/ReginaGurung/Downloads/chromedriver')

browser.get('http://www.seleniumhq.org/')

element = browser.find_element_by_link_text('Download')

element.text

element.get_attribute('href')
element.click()

element = browser.find_element_by_link_text('Projects')
element.click()

searchbar = browser.find_element_by_id('q')

# To populate the search bar:
searchbar.send_keys('download something')

# To enter the words import Keys
from selenium.webdriver.common.keys import Keys

searchbar.send_keys(Keys.ENTER)
