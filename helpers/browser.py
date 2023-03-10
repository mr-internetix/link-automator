# Imports
from helpers.cortex import Cortex
from helpers.helper_functions import Helpers
from helpers.main_script import MainScript
import openpyxl
from time import sleep
from helpers.browser_config import BrowserConfig
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# random imports for testing


class Browser(Cortex, Helpers, MainScript):
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

    def switch_to_main_frame(self):
        ''' switches to main frame'''
        #  main frame
        try:
            main_frame = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainFrame")))
            # switching to main frame
            self.driver.switch_to.frame(main_frame)
        except Exception as e:
            pass

    def manage_random_select(self, question_value, question_elements):
        # display element on screen
        self.driver.execute_script('''
                function display_select() {
                            select_tags = document.getElementsByTagName(
                                "select");

                            Array.from(select_tags).forEach((element) => {
                                element.style.display = "block";
                            });
                            }

                          display_select()

                             ''')

        all_select = (WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "select"))))

        for select in all_select:
            current_select = Select(select)
            try:
                random_value = random.randint(
                    7 if 13 == len(current_select.options) else 23, 30 if 15 < len(current_select.options) else len(current_select.options)-1)
                current_select.select_by_index(random_value)
            except Exception as e:
                pass

        # clicking on submit
        if self.find_provider() == "cortex":
            self.press_cortex_next()
        else:
            print("i am in main_script")
            self.switch_to_main_frame()

            # click on next
            self.press_main_next()

    def manage_provider(self):
        ''' Checks the provider and calls the respective functions'''
        if self.find_provider() == "cortex":
            self.manage_cortex()
        elif self.find_provider() == "main_script":
            self.manage_main()

    def manage_cortex(self):

        # Accept the conditions
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//a/span[contains(text(), 'Accept and take the survey')]"))).click()

        # check for are you question
        while True:
            if self.find_provider() == "cortex":
                # getting question text
                question_text = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
                question_value = self.find_question_excel(question_text)
                question = self.check_question_type_cortex()
                question_type = None
                question_elements = None

                if question != None:
                    question_type = list(question.keys())[0]
                    question_elements = question[list(question.keys())[0]]

                if question_value != False:

                    if question_type == "select":

                        self.manage_random_select(
                            question_value, question_elements)

                        # punch according to data
                    elif question_type == "single_select":
                        self.manage_cortex_single_select(
                            question_value, question_elements)

                    elif question_type == "text_box":
                        self.manage_cortex_text_box(
                            question_value, question_elements)

                else:

                    if question_text == "single_select":

                        # showing all options in need
                        self.showAllOptions()

                        # we dont have question punching randomly
                        print("we dont have question punching randomly")

                        self.manage_cortex_single_select(
                            question_value, question_elements)

                        # clicking on submit
                        self.press_cortex_next()

                        #  sleeping for 10 seconds
                        sleep(10)

                    elif question_type == "text_box":
                        print("text Box question")

                        self.manage_cortex_text_box(
                            question_value, question_elements)

                    elif question_type == "select":

                        # showing all options in need
                        self.showAllOptions()

                        print("select block")

                        self.manage_random_select(
                            question_value, question_elements)

                    elif question_type == "multi_select":

                        self.manage_cortex_multi_select(
                            question_value, question_elements)

                    elif question_type == "cortex_slider":
                        self.manage_cortex_slider(
                            question_value, question_elements)

            else:

                try:
                    self.press_cortex_next()
                except Exception as e:
                    # switching frame
                    self.switch_to_main_frame()
                    self.press_main_next()
                finally:
                    self.manage_provider()

    def manage_main(self):

        # Switch to main_frame
        self.switch_to_main_frame()

        # looping through questions
        while True:

            question_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#question .mrQuestionText"))).text

            question_value = self.find_question_excel(question_text)
            print(question_text)
            print(question_value)
            question = self.check_question_type_main()
            question_type = None
            question_elements = None

            if question != None:
                question_type = list(question.keys())[0]
                question_elements = question[list(question.keys())[0]]

            if question_type == "single_select":

                self.manage_main_single_select(
                    question_value, question_elements)

            elif question_type == "select_tag":

                try:
                    self.manage_random_select(
                        question_value, question_elements)
                except Exception as e:
                    pass

            elif question_type == "multi_select":
                self.manage_main_multi(question_value, question_elements)

            elif question_type == "multi_select_other":
                self.manage_main_multi_other(question_value, question_elements)

            elif question_type == "text_box":

                self.manage_main_text_box(question_value, question_elements)

            elif question_type == "grid_question":

                self.manage_main_grid_question(
                    question_text, question_elements)

            elif question_type == "slider":
                self.manage_main_slider(question_value, question_elements)

            elif question_type == None:
                self.press_main_next()
            else:
                self.press_main_next()


if __name__ == "__main__":
    pass
