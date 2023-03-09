import openpyxl
from fuzzywuzzy import fuzz
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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


if __name__ == "__main__":
    pass
