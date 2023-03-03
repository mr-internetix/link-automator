import pandas as pd
import random
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process


# mrMultipleText => grid question text selector

# mrQuestionText

question_text = "How many children under the age of 18 are living in your household? Please reference only the children for which you are the parent or legal guardian. (If there are no children under 18 in your household, please type 0)"
# question_text = "lll"
# question_text = "Please insert your zipcode ?"


def find_question_excel(question_text):

    try:
        df = pd.read_excel("./excel_config.xlsx")
        for index, question in enumerate(df.Question):
            try:
                if (fuzz.ratio(question_text, question)) > 90:
                    # question  sting
                    if "[" in df["Options"][index]:
                        converted_list = df["Options"][index].strip(
                            '][').split(',')
                        return converted_list
                    else:
                        return df["Options"][index]
            except Exception as e:
                return df["Options"][index]

    except Exception as e:
        print(e)


def generate_random_number(n):
    """
    Generates a random n-digit number.
    """
    start_range = 10**(n-1)  # Smallest n-digit number
    end_range = (10**n)-1   # Largest n-digit number
    return random.randint(start_range, end_range)

#     index = df.index[df["Question"].str.contains(question_text)].to_list()[
#         0]
#     return df["Options"][index]
# except Exception as e:
#     print(e)
#     return False

#     for index, question in enumerate(df.Question):

#         if question_text.lower() in df.Question:

#         df["Question"] == question_text:

#         # if question.lower().find(question_text.lower()) != -1:
#         #     return df["Options"][index]

#         # return False
# except Exception as e:
#     pass


# def check_for_inputs():
#     ''' Returns input available on the page '''

#     inputs = driver.execute_script('''

#     ''')


if __name__ == "__main__":
    print(find_question_excel(question_text))
    # print(generate_random_number(5))
