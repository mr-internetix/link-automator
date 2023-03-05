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
load_dotenv()


class Cortex():
    def __init__(self) -> None:
        pass

    def cortex_method(self):
        print('i am a cortex method')

    def press_cortex_next(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()
            sleep(3)
        except Exception as e:
            pass

    def manage_cortex_single_select(self, question_value):

        try:
            # showing all options needed
            self.showAllOptions()

            single_select_count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, f'//input[@type="radio"]')))

            single_select_count[question_value-1].click(
            ) if question_value != False else single_select_count[random.randint(0, len(single_select_count)-1)].click()

            # selecting random option question
            #  WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            #             (By.XPATH, f'//input[@type="radio"][@data-test-id="_{random.randint(1,len(count))}"]'))).click()

        except Exception as e:
            print(e)

        finally:
            # clicking on submit
            self.press_cortex_next()

    def manage_cortex_multi_select(self, question_value):

        try:
            # showing all options in need
            self.showAllOptions()

            sleep(3)
            # managing multi_select
            multi_select_count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "multipleChoice-checkbox")))

            # sleep
            sleep(3)

            multi_select_count[question_value-1].click(
            ) if question_value != False else multi_select_count[random.randint(0, len(multi_select_count)-1)].click()

        except Exception as e:
            pass

        finally:
            self.press_cortex_next()

    def manage_cortex_slider(self, question_value):

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

    def manage_cortex_text_box(self, question_value):

        try:
            text_boxes = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
            for textbox in text_boxes:
                textbox.send_keys(question_value)
        except Exception as e:
            print(e)
        finally:
            self.press_cortex_next()
            self.press_cortex_next()

    def check_question_type_cortex(self):
        question_type = self.driver.execute_script('''

                const checkForInputs = () => {
                    const inputs = ["select", "radio", "text"];
                    select_tags = document.getElementsByTagName("select");
                    single_select = document.querySelectorAll("input.mrSingle"); // this is for web script question
                    text_box = document.querySelectorAll("input.mrEdit"); //this for web script question
                    cortex_radio = document.querySelectorAll(".radio");
                    cortex_text = document.querySelectorAll(
                        "input[type='text']");

                    cortex_slider = document.querySelectorAll(
                        ".slider-handle.max-slider-handle.round.hide")
                    cortex_multi = document.querySelectorAll(
                        ".multipleChoice-checkbox")

                    if (cortex_slider.length > 0){
                        return "cortex_slider"

                    }
                    else if (cortex_multi.length > 0 ){

                        return "multi_select"
                    }
                    else if (select_tags.length > 0) {
                        return "select"
                    } else if (single_select.length > 0 || cortex_radio.length > 0) {
                        return "single_select"
                    } else if (text_box.length == 1 || cortex_text.length > 0) {
                        return "text_box"
                    }
                    };

                    return checkForInputs()


        ''')
        return question_type


if __name__ == "__main__":
    pass
