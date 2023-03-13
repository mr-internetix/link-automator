from helpers.browser import Browser
from time import sleep
from helpers.browser_config import Links


url = str(input('Enter Your Url => '))

my_browser = Browser()
my_browser.check_and_goto_url(url)
my_browser.manage_provider()
