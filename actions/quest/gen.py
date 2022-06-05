'''
from pprint import pprint
#import nltk
#nltk.download('stopwords')
from Questgen import main

def gener(qtype,context):

    """ This is the main function of Question Generation segmentaion

    Args:
            qtype (str): mcq  brief  bool

    """

    qe = main.BoolQGen()
    qg = main.QGen()
    payload = {"input_text": context}

    if qtype=='bool':
        output = qe.predict_boolq(payload)

    elif qtype=='mcq':
        output = qg.predict_mcq(payload)
    
    elif qtype=='short':
        output = qg.predict_shortq(payload)
    
    return output


#book="Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."

#result=gener(qtype=1,context=book)

#pprint(result)

'''

import errno
try:
    from Questgen import main
except ImportError as e:
    print("Error in importing Questgen module: ", e)


def generate_questions(ques_type: str, context: str) -> dict:
    """This function takes the question type and context as input and returns the questions of that type.

    Args:
        ques_type (str): The type of question to be generated.
        context (str): The context of the question.

    Returns:
        dict: The questions and answers of the given type and context.
    """
    payload = {
        "input_text": context
    }
    try:
        if ques_type == "bool":
            bool_ques_gen = main.BoolQGen()
            output = bool_ques_gen.predict_boolq(payload)
        elif ques_type == "mcq":
            general_ques_gen = main.QGen()
            output = general_ques_gen.predict_mcq(payload)
        elif ques_type == "paraphrase":
            general_ques_gen = main.QGen()
            output = general_ques_gen.predict_shortq(payload)
        else:
            return "Invalid question type"
    except OSError as error:
        if error.errno == errno.ENOENT:
            return "Model not found"
        else:
            return "Error in generating questions"
    return output