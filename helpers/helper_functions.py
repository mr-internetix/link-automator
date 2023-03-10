import openpyxl
from fuzzywuzzy import fuzz
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import string


class Helpers():
    def __init__(self):
        pass

    def find_question_excel(self, question_text):
        ''' Return options of the Question if Question Exists in Excel '''
        # Load the Excel file
        workbook = openpyxl.load_workbook('./excel_config.xlsx')
        sheet = workbook.active

        try:
            # Search for the question in the Excel file
            for row in sheet.iter_rows(values_only=True):
                if fuzz.ratio(row[0], question_text) > 90:
                    if "[" in row[1]:
                        converted_list = row[1].strip(
                            '][').split(',')
                        return converted_list
                    else:
                        return row[1]
            # If the question isn't found, return None
            return False
        except Exception as e:
            return row[1]

    def generate_random_number(self, n):
        """
        Generates a random n-digit number.
        """
        start_range = 10**(n-1)  # Smallest n-digit number
        end_range = (10**n)-1   # Largest n-digit number
        return random.randint(start_range, end_range)

    def generate_random_string(self, length):
        # Define the character set from which to generate the string
        characters = string.ascii_letters

        # Use the random module to generate a string of the desired length
        random_string = ''.join(random.choice(characters)
                                for i in range(length))

        return random_string

    def showAllOptions(self):
        self.driver.execute_script('''
            function showAllOptions() {
        all_plus = document.querySelectorAll(".mrShowText");

        all_plus.forEach((elem) => elem.click());
        }

        showAllOptions()

        ''')

    def get_visible_enabled_elements(self, elements):

        visible_enabled_elements = []

        for element in elements:
            if element.is_enabled() and element.is_displayed():
                visible_enabled_elements.append(element)

        return visible_enabled_elements

    def get_question_text(self):

        try:
            question_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".mrQuestionText")))

            return question_text.text
            # visible_elements = []

            # for element in all_text:
            #     if element.is_displayed():
            #         visible_elements.append(element.text)

            # return ' '.join(visible_elements)

        except Exception as e:
            return 'No question Found'

    def get_respondent_id(self):

        try:
            respondent_serial_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'current-question'))).text

            respondent_serial = respondent_serial_text[0:respondent_serial_text.index(
                '.')]

            if respondent_serial:
                # saving serial in txt
                with open('serial.txt', 'a') as f:
                    f.write("\n" + str(respondent_serial)+"\n")

            return respondent_serial
        except Exception as e:
            pass

    def check_survey_ends(self):
        try:
            skip_submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".SEMBtn .vClick .SEMEmpty")))
            skip_submit_button.click()

            thanks_for_survey = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))).text

            if thanks_for_survey.lower() == 'thanks for taking this survey!':
                with open('serial.txt', 'r') as f:
                    for line in f:
                        line == self.respondent_serial
                        f.write(f"{self.respondent_serial} -- Complete")

                return True

        except Exception as e:
            pass


if __name__ == "__main__":
    pass
