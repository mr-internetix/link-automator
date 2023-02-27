# Imports
from time import sleep
from helpers.browser_config import BrowserConfig
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import random
from dotenv import load_dotenv
import pandas as pd
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

    def find_question_excel(self, question_text):
        ''' Return options of the Question if Question Exists in Excel '''
        df = pd.read_excel("./excel_config.xlsx")

        for index, question in enumerate(df.Question):
            if question.lower().find(question_text.lower()) != -1:
                return df["Options"][index]

        return False

    def check_question_type_cortex(self):
        question_type = self.driver.execute_script(''' 
        
                const checkForInputs = () => {
                    const inputs = ["select", "radio", "text"];
                    select_tags = document.getElementsByTagName("select");
                    single_select = document.querySelectorAll("input.mrSingle"); // this is for web script question
                    text_box = document.querySelectorAll("input.mrEdit"); //this for web script question
                    cortex_radio = document.querySelectorAll(".radio");
                    cortex_text = document.querySelectorAll("input[type='text']");

                    if (select_tags.length > 0) {
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

    def punch_random_select(self):
        # display element on screen
        self.driver.execute_script('''
                                                function display_select() {
                            select_tags = document.getElementsByTagName("select");

                            Array.from(select_tags).forEach((element) => {
                                element.style.display = "block";
                            });
                            }

                          display_select()
                           
                             ''')

        sleep(5)

        all_select = (WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "select"))))

        for select in all_select:
            current_select = Select(select)
            random_value = random.randint(
                7 if 13 == len(current_select.options) else 23, 30 if 15 < len(current_select.options)else len(current_select.options)-1)
            current_select.select_by_index(random_value)

         # clicking on submit

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()

        # sleeping for 10 secs
        sleep(10)

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

                question_type = self.check_question_type_cortex()

                print(question_type, question_text)

                if question_value != False:

                    if question_type == "select":

                        print("select block")

                        self.punch_random_select()

                        # punch according to data
                    elif question_type == "single_select":

                        print("single_select block")

                        # sleep(10000)

                        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        #     (By.XPATH, f'//input[@type="radio"][@data-test-id="_{question_value}"]'))).click()

                        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                            (By.XPATH, f'//input[@type="radio"]')))[question_value-1].click()

                        # clicking on submit

                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()

                        #  sleeping for 10 seconds
                        sleep(10)

                    elif question_type == "text_box":
                        print("text Box question")

                        text_boxes = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
                        for textbox in text_boxes:
                            textbox.send_keys(str(question_value))

                        # clicking on submit

                        sleep(3)

                        try:

                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()

                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()
                        except Exception as e:
                            pass

                        #  sleeping for 10 seconds
                        sleep(10)

                else:

                    # we dont have question punching randomly
                    print("we dont have question punching randomly")

                    # finding_random_count
                    count = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                        (By.XPATH, f'//input[@type="radio"]')))

                    # selecting random option question
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, f'//input[@type="radio"][@data-test-id="_{random.randint(1,len(count))}"]'))).click()

                    # clicking on submit

                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, '//a[@data-test-id="submitButton"]'))).click()

                    #  sleeping for 10 seconds
                    sleep(10)
            else:
                self.manage_provider()

    def manage_main(self):
        #  main frame

        main_frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "mainFrame")))
        # switching to main frame

        self.driver.switch_to.frame(main_frame)

        # driver.switchTo().frame(iframe);
        # click on next button
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@class="mrNext"][@value="Next"]'))).click()


if __name__ == "__main__":
    pass
