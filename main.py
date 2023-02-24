from helpers.browser import Browser
from time import sleep
from helpers.browser_config import Links  # => cortex , main_script


my_browser = Browser()

my_browser.check_and_goto_url(Links.cortex.value)
my_browser.manage_provider()
# my_browser.manage_main()

sleep(100)
