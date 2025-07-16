import streamlit as st
import json
import copy
from google import genai
from googleapiclient.discovery import build

api_key = st.secrets['auth']['google']

def qs_setGenerator_llm(easy_qs, med_qs, hard_qs):

    default_qs = {'EASY_QUESTION': [{'title': 'EASY_QUESTION_1',
   'options': [{'value': 'OPTION_1'},
    {'value': 'OPTION_2'},
    {'value': 'OPTION_3'},
    {'value': 'OPTION_4'}],
   'correct_answer': 'OPTION_2'}],
 'MEDIUM_QUESTION': [{'title': 'MEDIUM_QUESTION_1',
   'options': [{'value': 'OPTION_1'},
    {'value': 'OPTION_2'},
    {'value': 'OPTION_3'},
    {'value': 'OPTION_4'}],
   'correct_answer': 'OPTION_3'}],
 'HARD_QUESTION': [{'title': 'HARD_QUESTION_1',
   'options': [{'value': 'OPTION_1'},
    {'value': 'OPTION_2'},
    {'value': 'OPTION_3'},
    {'value': 'OPTION_4'}],
   'correct_answer': 'OPTION_4'}]}
    
    all_qs = {}
    if easy_qs>0:
        all_qs["EASY_QUESTION"]=[]
        for i in range(easy_qs):
            item_qs = copy.deepcopy(default_qs['EASY_QUESTION'][0])
            item_qs['title']=f"EASY_QUESTION_{i+1}"
            all_qs['EASY_QUESTION'].append(item_qs)
    if med_qs>0:
        all_qs["MEDIUM_QUESTION"]=[]
        for i in range(med_qs):
            item_qs = copy.deepcopy(default_qs['MEDIUM_QUESTION'][0])
            item_qs['title']=f"MEDIUM_QUESTION_{i+1}"
            all_qs['MEDIUM_QUESTION'].append(item_qs)
    if hard_qs>0:
        all_qs["HARD_QUESTION"]=[]
        for i in range(hard_qs):
            item_qs = copy.deepcopy(default_qs['HARD_QUESTION'][0])
            item_qs['title']=f"HARD_QUESTION_{i+1}"
            all_qs['HARD_QUESTION'].append(item_qs)
    all_qs['title']="GENERATE A SUITABLE TITLE FOR THIS QUIZ"
    all_qs['document_title']="GENERATE A EVEN SHORTER TITLE TO QUICKLY IDENTIY IT IN GOOGLE DRIVE"
    all_qs['description']="GENERATE A SUITABLE DESCRIPTION FOR THIS QUIZ"
    return all_qs


def param_set(ai_generated_qs, qs_num, pts, qs_type, shuffle, index):
    
    createItem = [{'createItem': {'item': {'title': 'EASY_QUESTION',
    'questionItem': {'question': {'required': True,
      'choiceQuestion': {'type': 'RADIO',
       'options': [{'value': 'OPTION_1'},
        {'value': 'OPTION_2'},
        {'value': 'OPTION_3'},
        {'value': 'OPTION_4'}],
       'shuffle': False},
      'grading': {'pointValue': 'EASY_PTS',
       'correctAnswers': {'answers': [{'value': 'status'}]}}}}},
   'location': {'index': 'current_index'}}}]
    
    createItem[0]['createItem']['item']['questionItem']['question']['choiceQuestion']['shuffle']=shuffle
    createItem[0]['createItem']['item']['questionItem']['question']['grading']['pointValue']=pts
    createItem[0]['createItem']['location']['index']=index
    _questions=[]
    for i in range(qs_num):
        item = copy.deepcopy(createItem[0])
        item['createItem']['item']['title'] = ai_generated_qs[f'{qs_type}_QUESTION'][i]['title']
        for j in range(4):
            item['createItem']['item']['questionItem']['question']['choiceQuestion']['options'][j]['value']=ai_generated_qs[f'{qs_type}_QUESTION'][i]['options'][j]['value']
        
        item['createItem']['item']['questionItem']['question']['grading']['correctAnswers']['answers'][0]['value']=ai_generated_qs[f'{qs_type}_QUESTION'][i]['correct_answer']
        item['createItem']['location']['index']=i+createItem[0]['createItem']['location']['index']
        _questions.append(item)
    return _questions


def requests_set(ai_generated_qs, easy_qs, easy_qs_pts, med_qs, med_qs_pts, hard_qs, hard_qs_pts):

    default_requests = {'requests': [{'updateFormInfo': {'info': {'description': 'Generate a suitable description for this Google Form'},
    'updateMask': 'description'}},
  {'updateSettings': {'settings': {'quizSettings': {'isQuiz': True},
     'emailCollectionType': 'VERIFIED'},
    'updateMask': '*'}},
  {'createItem': {'item': {'title': 'EASY_QUESTION_PAGE_TITLE',
     'description': 'EASY_QUESTION_PAGE_DESC.',
     'pageBreakItem': {}},
    'location': {'index': 'index'}}}]}

    
    
    all_requests = {}
    all_requests['requests']=[]
    item = copy.deepcopy(default_requests['requests'][0])
    item['updateFormInfo']['info']['description']=ai_generated_qs['description']
    all_requests['requests'].append(item)
    item = copy.deepcopy(default_requests['requests'][1])
    all_requests['requests'].append(item)
    index = 0
    if easy_qs > 0:
        item = copy.deepcopy(default_requests['requests'][2])
        item['createItem']['item']['title']="Easy Questions ✍️"
        item['createItem']['item']['description'] = f"Each Question worth {easy_qs_pts} point(s) each."
        item['createItem']['location']['index']=index
        index+=1
        all_requests['requests'].append(item)
        
        easy = param_set(ai_generated_qs, qs_num=easy_qs, pts=easy_qs_pts, qs_type="EASY", shuffle=True, index=index)
        for i in range (easy_qs):
            all_requests['requests'].append(easy[i])
        index+=easy_qs
        
    if med_qs > 0:    
        item = copy.deepcopy(default_requests['requests'][2])
        item['createItem']['item']['title']="Medium Questions 💭"
        item['createItem']['item']['description'] = f"Each Question worth {med_qs_pts} point(s) each."
        item['createItem']['location']['index']=index
        index+=1
        all_requests['requests'].append(item)
        
        medium = param_set(ai_generated_qs, qs_num=med_qs, pts=med_qs_pts, qs_type="MEDIUM", shuffle=True, index=index)
        for i in range (med_qs):
            all_requests['requests'].append(medium[i])
        index+=med_qs
    if hard_qs > 0:    
        item = copy.deepcopy(default_requests['requests'][2])
        item['createItem']['item']['title']="Hard Questions 🧠"
        item['createItem']['item']['description'] = f"Each Question worth {hard_qs_pts} point(s) each."
        item['createItem']['location']['index']=index
        index+=1
        all_requests['requests'].append(item)
        
        hard = param_set(ai_generated_qs, qs_num=hard_qs, pts=hard_qs_pts, qs_type="HARD", shuffle=True, index=index)
        for i in range (hard_qs):
            all_requests['requests'].append(hard[i])
        index+=hard_qs

    
    return all_requests


def model_(all_generated_qs, everything, easy_qs, med_qs, hard_qs):
    
    client = genai.Client(api_key=api_key)
    
    prompt = f'''You are an expert quiz generator. You will be given a lecture transcript as input. Your task is to generate a JSON file that contains single-answered multiple-choice questions based on that transcript. Based on the transcript, generate single-answered multiple-choice questions in the following strict JSON format. Do not include any explanation, headers, or extra text. Only return valid JSON. Do not change the structure or keys: 
    Guidelines:
    
    Question Type: Multiple-choice
    Answer Constraint: Only one correct answer

    -The EASY_QUESTIONS should be directly fact-based from the transcript (definitions, lists, simple concepts).
    
    -The MEDIUM_QUESTION should require some understanding or comparison between concepts.
    
    -The HARD_QUESTION should test deeper reasoning, critical thinking, or less directly stated ideas.
    
    Ensure that the questions are derived only from the content of the transcript.
    
    Provide exactly {easy_qs} easy questions, {med_qs} medium questions, and {hard_qs} hard questions from the transcript.
    
    Use realistic and topic-relevant question titles and answer options, but preserve the JSON key names and structure exactly as provided.
    
    The "options" must be relevant choices.
    
    One "correct_answer" must exactly match one of the values in "options".
    
    "title" – A suitable full title for the quiz based on the lecture.
    "document_title" – A shorter version of the title, suitable for identifying the quiz file in Google Drive.
    "description" – A one or two sentence description of what the quiz is about.
    
    Only return a valid JSON object in the **EXACT FORMAT** as provided, nothing else.
    DO NOT CHANGE THE JSON FORMAT EVEN IF THIRD WORLD WAR HAPPENS. NEVER EVER CHANGE THE JSON FORMAT.
    
    Here is the JSON -> {all_generated_qs}
    Here is the Transcript of the lecture -> {everything}
    '''
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[prompt],
    )
    response = response.text
    ai_generated_qs = json.loads(response.removeprefix('```json\n').removesuffix('\n```'))
    return ai_generated_qs


def auth_create(all_requests, title, document_title, creds):

  SCOPES = "https://www.googleapis.com/auth/forms.body"
  DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

  form_service = build(
    "forms",
    "v1",
    credentials=creds,
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
  )

  NEW_FORM = {
    "info": {
        "title": f"{title}",
        "documentTitle": f"{document_title}"
    }
  }
  result = form_service.forms().create(body=NEW_FORM).execute()
  question_setting = (
      form_service.forms()
      .batchUpdate(formId=result["formId"], body=all_requests)
      .execute()
  )
  get_result = form_service.forms().get(formId=result["formId"]).execute()

  return get_result






def all_functions(everything, easy_qs, easy_qs_num, med_qs, med_qs_num, hard_qs, hard_qs_num):
    all_qs_generated = qs_setGenerator_llm(easy_qs=easy_qs, med_qs=med_qs, hard_qs=hard_qs)
    print("step 1 done")
    ai_generated_qs = model_(all_qs_generated,everything,easy_qs, med_qs, hard_qs)
    print("step 2 done")
    all_requests = requests_set(ai_generated_qs, easy_qs, easy_qs_num, med_qs, med_qs_num, hard_qs, hard_qs_num)
    print("step 3 done")
    get_result = auth_create(all_requests=all_requests, title=ai_generated_qs['title'], document_title=ai_generated_qs['document_title'])
    print("step 4 done")

    return get_result




def model_text(all_generated_qs, everything, easy_qs, med_qs, hard_qs):
    
    client = genai.Client(api_key=api_key)
    
    prompt = f'''You are an expert quiz generator. You will be given a paragraph, or a few topics as input. Your task is to generate a JSON file that contains multiple-choice questions based on those topics. Based on those topics, generate multiple choice questions in the following strict JSON format. Do not include any explanation, headers, or extra text. Only return valid JSON. Do not change the structure or keys: 
    Guidelines:
    The EASY_QUESTIONS should be directly fact-based from the paragraph or topics (definitions, lists, simple concepts).
    
    The MEDIUM_QUESTION should require some understanding or comparison between concepts.
    
    The HARD_QUESTION should test deeper reasoning, critical thinking, or less directly stated ideas.
    
    Ensure that the questions are derived only from the topics of the paragraph.
    
    Provide exactly {easy_qs} easy questions, {med_qs} medium questions, and {hard_qs} hard questions from the paragraph.
    
    Use realistic and topic-relevant question titles and answer options, but preserve the JSON key names and structure exactly as provided.
    
    The "options" must be relevant choices.
    
    One "correct_answer" must exactly match one of the values in "options".
    
    "title" – A suitable full title for the quiz based on the topics.
    "document_title" – A shorter version of the title, suitable for identifying the quiz file in Google Drive.
    "description" – A one or two sentence description of what the quiz is about.
    
    Only return a valid JSON object in the **EXACT FORMAT** as provided, nothing else.
    DO NOT CHANGE THE JSON FORMAT EVEN IF THIRD WORLD WAR HAPPENS. NEVER EVER CHANGE THE JSON FORMAT.
    
    Here is the JSON -> {all_generated_qs}
    Here is the paragraph -> {everything}
    '''
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[prompt],
    )
    response = response.text
    ai_generated_qs = json.loads(response.removeprefix('```json\n').removesuffix('\n```'))
    return ai_generated_qs
