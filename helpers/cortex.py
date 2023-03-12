# Imports
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
from helpers.helper_functions import Helpers
import logging
load_dotenv()


class Cortex(Helpers):
    def __init__(self) -> None:
        pass

    def press_cortex_next(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()
            sleep(3)
        except Exception as e:
            pass

    def manage_cortex_single_select(self, question_value, question_elements):

        try:
            # showing all options needed
            self.showAllOptions()

            # single_select_count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            #     (By.XPATH, f'//input[@type="radio"]')))

            question_elements[question_value-1].click(
            ) if question_value != False else question_elements[random.randint(0, len(question_elements)-1)].click()

            # selecting random option question
            #  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            #             (By.XPATH, f'//input[@type="radio"][@data-test-id="_{random.randint(1,len(count))}"]'))).click()

        except Exception as e:
            print(e)

        finally:
            # clicking on submit
            self.press_cortex_next()

    def manage_cortex_multi_select(self, question_value, question_elements):

        try:
            # showing all options in need
            self.showAllOptions()

            sleep(3)
            # managing multi_select
            # multi_select_count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            #     (By.CLASS_NAME, "multipleChoice-checkbox")))

            # sleep
            # sleep(3)

            question_elements[question_value-1].click(
            ) if question_value != False else question_elements[random.randint(0, len(question_elements)-1)].click()

        except Exception as e:
            pass

        finally:
            self.press_cortex_next()

    def manage_cortex_slider(self, question_value, question_elements):

        try:
            # show all options in need
            self.showAllOptions()

            # managing cortex

            self.driver.execute_script('''
                cortex_slider = document.querySelectorAll(
                    ".slider-handle.max-slider-handle.round.hide")
                cortex_slider.forEach(elem => elem.click())
            ''')

        except Exception as e:
            pass

        finally:
            self.press_cortex_next()

    def manage_cortex_text_box(self, question_value, question_elements):

        try:
            # text_boxes = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
            for textbox in question_elements:
                if question_value != False:
                    textbox.send_keys(question_value)
                else:
                    textbox.send_keys(random.generate_random_number(
                        int(textbox.get_attribute("maxlength"))))
        except Exception as e:
            print(e)
        finally:
            self.press_cortex_next()
            self.press_cortex_next()

    def check_question_type_cortex(self):
        wait = WebDriverWait(self.driver, 10)
        element_types = {
            'cortex_slider': {'selector': '.slider-handle.max-slider-handle.round.hide', 'locator': By.CSS_SELECTOR},
            'multi_select': {'selector': '.multipleChoice-checkbox', 'locator': By.CSS_SELECTOR},
            'select': {'selector': 'select', 'locator': By.TAG_NAME},
            'single_select': {'selector': '.radio', 'locator': By.CSS_SELECTOR},
            'text_box': {'selector': 'input[type="text"]', 'locator': By.CSS_SELECTOR}
        }

        form = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, 'form')))
        all_elements = []
        for elements_name, element_type in element_types.items():
            try:
                elements = form.find_elements(
                    element_type['locator'], element_type['selector'])
                all_elements.append({elements_name: elements})
            except Exception as e:
                logging.info(
                    f'exception raised at looping elements in all_elements{e}')

        for dict in all_elements:
            for elem_name, elem_list in dict.items():
                if len(elem_list) > 0:
                    return {elem_name: elem_list}


if __name__ == "__main__":
    pass
