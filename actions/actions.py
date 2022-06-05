from multiprocessing import context
from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .ocr_utils import DataExtractor
from .quest_gen_utils import generate_questions
from time import sleep

#Action for link quesgen
class ActionSayLinkBack(Action):

    def name(self) -> Text:
        return "action_say_link_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pdf_link = tracker.get_slot("link")
        qtype = tracker.get_slot("qtype")

        #-----------------------------------------

        #if qtype[0].lower()=="s" or "b":
        if qtype[0].lower() in ["s","b"]:
          qtype_="short"
        elif qtype[0].lower()=="m":
          qtype_="mcq"
        #elif qtype[0].lower()=="t" or "b":
        elif qtype[0].lower() in ["t","b"]:
          qtype_="bool"

        #------------------------------------------
        
        #Extracting link content here
        dataext=DataExtractor(qtype)
        content=dataext.extract_url_data(url=pdf_link)

        
        # Processing content and question generation
        if qtype_ == "mcq":

          #dispatcher.utter_message(text=qtype+" is the value in slot")

          dispatcher.utter_message(text="Generating mcq questions...")

          result=generate_questions(ques_type='mcq',context=content)
          print(result)

          n=len(result['questions'])

          for i in range(n):

            out="Question "+str(i+1)+" : \n"+result['questions'][i]['question_statement']
            dispatcher.utter_message(text=out)

            for j in (result['questions'][i]['options']):
              dispatcher.utter_message(text=j)

            out=result['questions'][i]['answer']+"*"
            dispatcher.utter_message(text=out)
          
          
        elif qtype_ == "bool":

          dispatcher.utter_message(text="Generating true or false questions...")

          result=generate_questions(ques_type='bool',context=content)
          print(result)

          n=len(result['Boolean Questions'])

          for i in range(n):

            out=result['Boolean Questions'][i]
            
            dispatcher.utter_message(text=out)


        elif qtype_ == "short":

          #dispatcher.utter_message(text=qtype+" is the value in slot")

          dispatcher.utter_message(text="Generating short answer questions..")

          result=generate_questions(ques_type='paraphrase',context=content)

          #Result has dictionairy of questions and answers..
          #Iterating the in loop to perform QA showcase..

          print(result)
          n=len(result['questions'])

          for i in range(n):

            out="Question "+str(i+1)+" : \n"+result['questions'][i]['Question']
            dispatcher.utter_message(text=out)
            
            out="Answer "+str(i+1)+" : \n"+result['questions'][i]['Answer']
            dispatcher.utter_message(text=out)

          #Data  will be processed after analysing output type
               
        return []


#Action for link quesgen
class ActionSayPdfBack(Action):

    def name(self) -> Text:
        return "action_say_pdf_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="PDF processing under development")
        return []                