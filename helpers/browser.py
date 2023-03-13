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


class Browser(Cortex, MainScript):
    '''  Contains All The methods regarding to borwser action '''

    def __init__(self) -> None:
        ''' initializing Browser and  setting up configs for it '''

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-logging")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")

        # This is for getting headless browser
        # options.add_argument(BrowserConfig.browser_type.value)

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.respondent_serial = ''
        # self.driver.execute_script("document.body.style.zoom='80%'")
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

                        self.manage_select_cortex(
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

                        self.manage_random_select_cortex(
                            question_value, question_elements)

                        self.press_cortex_next()

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

        # getting respondent_id
        self.respondent_serial = self.get_respondent_id()

        # looping through questions
        while True:

            question_text = self.get_question_text()

            # show
            self.showAllOptions()

            question_value = self.find_question_excel(question_text)

            form_elements = self.check_question_container()

            print(form_elements)
            for question_container in form_elements:
                question = self.check_question_type_main(question_container)

                print(f"Question recieved : {question}")

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
                        self.manage_select_main(
                            question_value, question_elements)
                    except Exception as e:
                        pass

                    finally:
                        self.press_main_next()

                elif question_type == "multi_select":
                    self.manage_main_multi(question_value, question_elements)

                elif question_type == "multi_select_other":
                    self.manage_main_multi_other(
                        question_value, question_elements)

                elif question_type == "text_box":

                    self.manage_main_text_box(
                        question_value, question_elements)

                elif question_type == "grid_question":

                    self.manage_main_grid_question(
                        question_text, question_elements)

                elif question_type == "slider":
                    self.manage_main_slider(question_value, question_elements)

                elif question_type == None:
                    if self.check_survey_ends() == True:
                        print("survey Ends")
                        break
                    else:
                        self.press_main_next()
                else:
                    self.press_main_next()


if __name__ == "__main__":
    pass
