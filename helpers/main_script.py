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

    def manage_main_single_select(self, question_value):

        try:
            # showing all options in needed
            self.showAllOptions()

            # single select count
            single_select_count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, f'//input[@type="radio"]')))

            if single_select_count[question_value-1].is_enabled():
                if question_value != False:
                    single_select_count[question_value-1].click()
                else:
                    single_select_count[random.randint(
                        0, len(single_select_count)-1)].click()

        except Exception as e:
            pass
        finally:
            self.press_main_next()

    def manage_main_multi(self, question_value):
        try:

            # showing all options in need
            self.showAllOptions()

            multi_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'mrMultipleText')))

            sleep(2)

            multi_text[random.randint(
                0, len(multi_text)-1)].click()

        except Exception as e:
            pass

        finally:
            self.press_main_next()

    def manage_main_text_box(self, question_value):
        try:
            text_boxes = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//input[@class="mrEdit"]')))

            for textbox in text_boxes:
                if textbox.is_displayed():
                    textbox.send_keys(question_value) if question_value != False else textbox.send_keys(
                        self.generate_random_number(textbox.get_attribute("maxlength")))
        except Exception as e:
            print(e)
        finally:
            # clicking on submit
            sleep(3)
            try:
                self.press_main_next()
                self.press_main_next()
            except Exception as e:
                pass

    def manage_main_grid_question(self, question_value):
        try:
            grid_options = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '.mrGridCategoryText.mrGridQuestionText')))

            print(f'grid_options: {len(grid_options)}')

            total_grid_question = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prog-progress-bar-item")))

            print(f'total_grid_options: {len(total_grid_question)}')

            for question in total_grid_question:
                grid_options[random.randint(
                    0, len(grid_options)-1)].click()

                sleep(4)
            # click on next button
        except Exception as e:
            print(e)
        finally:
            self.press_main_next()

    def manage_main_slider(self, question_value):
        try:

            total_questions = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "prog-progress-bar-item")))

            for question in total_questions:

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
        main_question_type = self.driver.execute_script('''

            const checkForInputsInScript = () => {
                select_tags = document.querySelectorAll("select.mrDropdown");
                single_select = document.querySelectorAll(".mrSingle");
                text_box = document.querySelectorAll(".mrEdit");
                next_button = document.querySelector("input[class='mrNext']");
                multi_select = document.querySelectorAll(".mrMultiple");
                all_labels = document.querySelectorAll("label")
                grid_question = document.querySelectorAll(
                    ".mrGridCategoryText.mrGridQuestionText")

                slider_question = document.getElementsByClassName("slider")

                if(slider_question.length > 0 ){

                    slider_mover = document.querySelector(".slider-add-arrow")

                    if(slider_mover.classList.contains("hidden-arrow")){
                        slider_mover.classList.remove("hidden-arrow")
                    }


                    return "slider"


                }

                else if(grid_question.length > 0){

                    grid_question.forEach((elem)=>{

                    if(elem.hasAttribute("disabled")){
                        return "null"
                    }

                    })

                    return "grid_question"

                }
                else if (single_select.length > 0) {

                    single_select.forEach((elem) =>{
                        if(elem.hasAttribute("checked")){
                            console.log("single_already_selected")
                            return "null"
                        }
                    })

                    all_labels.forEach((elem) => {
                        if(elem.classList.contains("cellCheckedBackground")){
                            console.log("already selected")
                            return "null"
                        }
                    })

                    return "single_select";

                } else if (text_box.length > 0) {

                    text_box.forEach((elem)=>{

                        if(elem.hasAttribute("disabled")){

                            console.log("disabled")
                            return "null"

                        }
                    })

                    return "text_box";
                } else if (select_tags.length > 0) {
                    return "select_tag";
                }else if (multi_select.length > 0){

                    multi_select.forEach((elem)=>{

                        if(elem.hasAttribute("disabled")){
                            console.log("disabled")
                            return "null"

                        }
                    })

                    return "multi_select"
                }
                else {
                    return "null";
                }

            };

        return checkForInputsInScript()

        ''')

        return main_question_type


if __name__ == "__main__":
    pass
