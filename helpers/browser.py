# Imports
from time import sleep
from helpers.browser_config import BrowserConfig
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
from dotenv import load_dotenv
load_dotenv()

# random imports for testing


class Browser():
    '''  Contains All The methods regarding to borwser action '''

    def __init__(self) -> None:
        ''' initializing Browser and  setting up configs for it '''

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-logging")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-popup-blocking")

        # This is for getting headless browser
        # options.add_argument(BrowserConfig.browser_type.value)

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        # this is for custom window application
        # self.driver.set_window_size(
        #     BrowserConfig.browser_width.value, BrowserConfig.browser_height.value)
        # self.driver.set_script_timeout(90)

    def check_and_goto_url(self, url):
        ''' Goes to url '''
        try:
            self.driver.get(url)
        except Exception as e:
            print(e)

    def find_provider(self):
        ''' Find provider'''
        try:
            if self.driver.current_url.find("https://enter.ipsosinteractive.com/") != -1:
                return "cortex"
            elif self.driver.current_url.find("https://staging01.ipsosinteractive.com/") != -1:
                return "main_script"
            else:
                return None
        except Exception as e:
            return "something went wrong"

    def manage_cortex(self):

        # Accept the conditions
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//a/span[contains(text(), 'Accept and take the survey')]"))).click()

        # check for are you question

        gender_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h3"))).text

        if gender_text.lower().find("are you") != -1:

            # selecting random gender question

            # WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            #     (By.XPATH, f'//input[@type="radio"][@data-test-id="_{random.randint(1,4)}"]')))[0].click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, f'//input[@type="radio"][@data-test-id="_2"]')))[0].click()

            # clicking on submit

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()

    def manage_provider(self):
        if self.find_provider() == "cortex":
            self.manage_cortex()
        elif self.find_provider() == "main_script":
            self.manage_main_script()

    def manage_main_script(self):
        # click on next button
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@class="mrNext"][@value="Next"]'))).click()


if __name__ == "__main__":
    pass
