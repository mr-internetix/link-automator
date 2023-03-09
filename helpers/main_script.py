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
import logging
import pandas as pd
load_dotenv()


class MainScript():
    def __init__(self):
        pass

    def press_main_next(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//input[@class="mrNext"][@value="Next"]'))).click()
            sleep(3)
        except Exception as e:
            pass

    def manage_main_single_select(self, question_value, question_elements):

        try:
            # showing all options in needed
            self.showAllOptions()

            # single select count
            # all_single_select = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            #     (By.XPATH, f'//input[@type="radio"]')))

            # single_select = self.get_visible_enabled_elements(
            #     all_single_select)

            # if single_select[question_value-1].is_enabled():
            #     if question_value != False:
            #         single_select[question_value-1].click()
            #     else:
            #         single_select[random.randint(
            #             0, len(single_select)-1)].click()

            question_elements[random.randint(
                0, len(question_elements)-1)].click()

        except Exception as e:
            pass
        finally:
            self.press_main_next()

    def manage_main_multi(self, question_value, question_elements):
        try:

            # showing all options in need
            self.showAllOptions()

            all_multi = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'mrMultipleText')))

            multiple_checkboxes = self.get_visible_enabled_elements(all_multi)

            sleep(2)

            multiple_checkboxes[random.randint(
                0, len(multiple_checkboxes)-1)].click()

        except Exception as e:
            pass

        finally:
            self.press_main_next()

    def manage_main_text_box(self, question_value, question_elements):
        try:
            all_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//input[@class="mrEdit"]')))

            text_boxes = self.get_visible_enabled_elements(all_elements)

            for textbox in text_boxes:
                if (question_value != False):
                    textbox.clear()
                    textbox.send_keys(str(question_value))
                else:
                    print(type(self.generate_random_number(
                        (textbox.get_attribute("maxlength")))))
                    textbox.send_keys("0")
                    # textbox.send_keys(self.generate_random_number(
                    #     (textbox.get_attribute("maxlength"))))
        except Exception as e:
            print("Exceptions Raised in manage_main_text_box :=>", e)
        finally:
            # clicking on submit
            sleep(3)
            try:
                self.press_main_next()
                self.press_main_next()
            except Exception as e:
                pass

    def manage_main_grid_question(self, question_value, question_elements):
        try:
            grid_options = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '.mrGridCategoryText.mrGridQuestionText')))

            total_grid_questions = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prog-progress-bar-item")))

            filtered_grid_question = self.get_visible_enabled_elements(
                total_grid_questions)

            filtered_grid_options = self.get_visible_enabled_elements(
                grid_options)

            for question in filtered_grid_question:
                filtered_grid_options[random.randint(
                    0, len(filtered_grid_options)-1)].click()

                sleep(3)
        except Exception as e:
            print(e)
        finally:
            self.press_main_next()

    def manage_main_slider(self, question_value, question_elements):
        try:

            total_questions = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prog-progress-bar-item")))

            filered_questions = self.get_visible_enabled_elements(
                total_questions)

            for question in filered_questions:

                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, "slider-add-arrow"))).click()

                self.driver.execute_script('''
                    document.querySelector(".prog-control-next").click()

                    ''')
                sleep(3)
        except Exception as e:
            pass
        finally:
            self.press_main_next()

    def check_question_type_main(self):
        '''
        function return element present on the screen and detects it types
        '''

        wait = WebDriverWait(self.driver, 10)

        element_types = {
            'select_tag': {'selector': 'select.mrDropdown', 'locator': By.CSS_SELECTOR},
            'single_select': {'selector': '.mrSingle', 'locator': By.CSS_SELECTOR},
            'text_box': {'selector': '.mrEdit', 'locator': By.CSS_SELECTOR},

            'multi_select': {'selector': '.mrMultiple', 'locator': By.CSS_SELECTOR},
            # 'radio_button':{'selector':'.mrRadio','locator':By.CSS_SELECTOR},
            # 'checkbox':{'selector':'.mrCheckbox','locator':By.CSS_SELECTOR},
            # 'all_labels': {'selector': 'label', 'locator': By.TAG_NAME},
            'grid_question': {'selector': '.mrGridCategoryText.mrGridQuestionText', 'locator': By.CSS_SELECTOR},
            'slider_question': {'selector': '.slider', 'locator': By.CSS_SELECTOR},

        }

        form = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mrForm #content .question-container')))

        all_elements = []

        for elements_name, element_type in element_types.items():
            try:
                filtered_elements = form.find_elements(
                    element_type['locator'], element_type['selector'])

                elements = self.get_visible_enabled_elements(filtered_elements)

                all_elements.append({elements_name: elements})

            except Exception as e:
                logging.info(
                    f" exception in main_script check question type {e}")

        for dict in all_elements:
            for elem_name, elem_list in dict.items():
                if len(elem_list) > 0:
                    return {elem_name: elem_list}


if __name__ == "__main__":
    pass
