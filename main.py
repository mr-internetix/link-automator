from helpers.browser import Browser
from time import sleep
from helpers.browser_config import Links  # => cortex , main_script

my_browser = Browser()
my_browser.check_and_goto_url(
    "https://enter.ipsosinteractive.com/landing/?rType=0&id=&ci=en-us&pid=S23007177&redirectStage=1&routerID=78&supplierID=1090&surveyid=882325&testCortex=1")

my_browser.manage_provider()

sleep(1000)


my_browser.manage_main_script()
