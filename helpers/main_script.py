from helpers.helper_functions import Helpers
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
from selenium.webdriver.common.action_chains import ActionChains
load_dotenv()


class MainScript(Helpers):
    def __init__(self):
        pass

    def press_main_next(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//input[@class="mrNext"][@value="Next"]'))).click()
            sleep(3)
        except Exception as e:
            pass

    def manage_select_main(self, question_value, question_elements):
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

        for select in question_elements:
            current_select = Select(select)
            try:
                if question_value != False:
                    pass
                else:
                    random_value = random.randint(
                        7 if 13 == len(current_select.options) else 23, 30 if 15 < len(current_select.options) else len(current_select.options)-1)
                    current_select.select_by_index(random_value)

            except Exception as e:
                pass

    def check_already_checked_elems(self, elements, type_of):
        try:
            if type_of == 'single':
                for element in elements:
                    if (element.find_element(By.CSS_SELECTOR, '.mrSingle').get_attribute('checked')):
                        return True
            if type_of == 'multi_checkbox':
                for element in elements:
                    if (element.find_element(By.CSS_SELECTOR, '.mrMultiple').get_attribute('checked')):
                        return True

            return None
        except Exception as e:
            logging.info(
                f" some thing went wrong in check_already_elems : {e}")

    def manage_main_single_select(self, question_value, question_elements):

        try:
            # showing all options in needed

            # check if contains_already checked elems
            if self.check_already_checked_elems(question_elements, type_of='single') == None:
                if question_value != False:
                    print(f"{question_value}")
                    for element in question_elements:
                        if (element.find_element(By.CSS_SELECTOR, '.mrSingle')).get_attribute('value') == f"__{question_value}":
                            element.click()
                else:
                    question_elements[random.randint(
                        0, len(question_elements)-1)].click()

        except Exception as e:
            logging.info(f"something went wrong and single select {e}")
        finally:
            self.press_main_next()

    def manage_main_multi(self, question_value, question_elements):
        try:
            # checking for the question value and punch punching , random
            if self.check_already_checked_elems(question_elements, type_of='multi_checkbox') == None:
                if question_value != False:
                    if type(question_value) is list:
                        for value in question_value:
                            for element in question_elements:
                                if element.find_element(By.CSS_SELECTOR, ".mrMultiple").get_attribute('value') == f"__{value}":
                                    element.click()
                    else:
                        for element in question_elements:
                            if element.find_element(By.CSS_SELECTOR, ".mrMultiple").get_attribute('value') == f"__{question_value}":
                                element.click()
                else:
                    for i in range(random.randint(1, len(question_elements)-1)):
                        question_elements[random.randint(
                            0, len(question_elements)-1)].click()

        except Exception as e:
            pass

        finally:
            self.press_main_next()

    def manage_main_multi_other(self, question_value, question_elements):
        try:

            # showing all options in need
            # filtered_input = question_elements.find_elements(
            #     By.CSS_SELECTOR, '.mrMultiple')
            # if self.check_already_checked_elems(filtered_input) == None:
            #     if question_value != False:
            #         pass

            #     else:
            for i in range(0, random.randint(1, len(question_elements))):
                question_elements[random.randint(
                    0, len(question_elements)-1)].click()
        except Exception as e:
            print(e)

        finally:
            self.press_main_next()

    def manage_main_text_box(self, question_value, question_elements):
        try:

            self.driver.execute_script('''
                elements  = document.querySelectorAll(".mrEdit")
                Array.from(elements).filter(element =>{
                    element.removeAttribute("pattern")
                })

            ''')
            for textbox in question_elements:
                if (question_value != False):
                    textbox.clear()
                    textbox.send_keys(str(question_value))
                else:
                    # random punch
                    if textbox.get_attribute('type') == 'text':
                        random_string = self.generate_random_string(10)
                        textbox.send_keys(random_string)
                    elif textbox.get_attribute('type') == 'number':
                        random_int = self.generate_random_number(
                            int(textbox.get_attribute("maxlength")))

                        textbox.send_keys(str(random_int))
                    else:
                        textbox.send_keys(str(0))
        except Exception as e:
            print("Exceptions Raised in manage_main_text_box :=>", e)
        finally:
            # clicking on submit
            sleep(3)
            self.press_main_next()
            self.press_main_next()

    def manage_main_grid_question(self, question_value, question_elements):
        try:
            # grid_options = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            #     (By.CSS_SELECTOR, '.mrGridCategoryText.mrGridQuestionText')))

            total_grid_questions = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prog-progress-bar-item")))

            filtered_grid_question = self.get_visible_enabled_elements(
                total_grid_questions)

            # filtered_grid_options = self.get_visible_enabled_elements(
            #     grid_options)

            for question in filtered_grid_question:
                question_elements[random.randint(
                    0, len(question_elements)-1)].click()

                sleep(1)

        except Exception as e:
            action = ActionChains(self.driver)
            action.key_down(Keys.CONTROL).send_keys(
                'Z').key_up(Keys.CONTROL).perform()
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

    def check_question_container(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            form_elements = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '#mrForm #content .question-container')))

            print(
                f" this is form elements with container {len(form_elements)}")

            return form_elements
        except Exception as e:
            form_elements = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mrForm #content')))

            print(f"{form_elements}")
            return form_elements

    def check_question_type_main(self, question_container):
        '''
        function return element present on the screen and detects it types
        '''

        element_types = {
            'select_tag': {'selector': '.mrDropdown', 'locator': By.CSS_SELECTOR},
            'single_select': {'selector': '.label-with-mrSingle ', 'locator': By.CSS_SELECTOR},
            'text_box': {'selector': '.mrEdit', 'locator': By.CSS_SELECTOR},
            'multi_select': {'selector': '.label-with-mrMultiple', 'locator': By.CSS_SELECTOR},
            'grid_question': {'selector': '.mrGridCategoryText.mrGridQuestionText', 'locator': By.CSS_SELECTOR},
            'slider_question': {'selector': '.slider', 'locator': By.CSS_SELECTOR},

        }

        all_elements = []

        for elements_name, element_type in element_types.items():
            try:
                filtered_elements = question_container.find_elements(
                    element_type['locator'], element_type['selector'])

                elements = self.get_visible_enabled_elements(
                    filtered_elements)

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
