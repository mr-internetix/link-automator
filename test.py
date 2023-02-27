import pandas as pd


# mrMultipleText => grid question text selector

# mrQuestionText

question_text = "What is your"


def find_question_excel(question_text):
    df = pd.read_excel("./excel_config.xlsx")

    for index, question in enumerate(df.Question):
        if question.lower().find(question_text.lower()) != -1:
            return df["Options"][index]

    return False


def check_for_inputs():
    ''' Returns input available on the page '''

    inputs = driver.execute_script(''' 
    
    ''')


if __name__ == "__main__":
    print(find_question_excel(question_text))
