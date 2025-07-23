import streamlit as st
from all_functions import (
    auth_create,
    model_text,
    qs_setGenerator_llm,
    requests_set,
)
import time
from autheticate import get_creds

    
st.set_page_config(
    page_title="QuizFlow.Ai",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)



###########################################################################
#SESSION STATES
if "btn1_topics_color" not in st.session_state:
    st.session_state.btn1_topics_color = "primary"
if "last_text" not in st.session_state:
    st.session_state.last_text = ""
if "btn1_topics_clicked" not in st.session_state:
    st.session_state.btn1_topics_clicked = False
if "btn2_topics_clicked" not in st.session_state:
    st.session_state.btn2_topics_clicked = False
    
############NUMBERS
if "easy_qs_last_topics" not in st.session_state:
    st.session_state.easy_qs_last_topics = None
if "medium_qs_last_topics" not in st.session_state:
    st.session_state.medium_qs_last_topics = None
if "hard_qs_last_topics" not in st.session_state:
    st.session_state.hard_qs_last_topics = None
if "easy_qs_num_last_topics" not in st.session_state:
    st.session_state.easy_qs_num_last_topics = None
if "medium_qs_num_last_topics" not in st.session_state:
    st.session_state.medium_qs_num_last_topics = None
if "hard_qs_num_last_topics" not in st.session_state:
    st.session_state.hard_qs_num_last_topics = None
###########################################################################






def btn1_topics():
    if len(text)<10:
        st.toast(f"**Please enter at least 20 words about your topic.**", icon="🚫")
    elif text == st.session_state.last_text:
        st.toast(f"**Please change the topic to generate a new quiz.**", icon="🚫")
    else:
        st.session_state.last_text = text
        st.session_state.btn1_topics_clicked = True


def btn2_topics():
    if easy_qs_topics != st.session_state.easy_qs_last_topics or med_qs_topics != st.session_state.medium_qs_last_topics or hard_qs_topics != st.session_state.hard_qs_last_topics or easy_qs_num_topics != st.session_state.easy_qs_num_last_topics or med_qs_num_topics != st.session_state.medium_qs_num_last_topics or hard_qs_num_topics != st.session_state.hard_qs_num_last_topics:
        
        st.session_state.easy_qs_last_topics = easy_qs_topics
        st.session_state.medium_qs_last_topics = med_qs_topics
        st.session_state.hard_qs_last_topics = hard_qs_topics
        st.session_state.easy_qs_num_last_topics = easy_qs_num_topics
        st.session_state.medium_qs_num_last_topics = med_qs_num_topics
        st.session_state.hard_qs_num_last_topics = hard_qs_num_topics
        
        st.session_state.btn2_topics_clicked = True
    
    st.session_state.btn1_topics_color = "secondary"


def quiz():

    transcript = text
    quiz_status = st.status("🧠 Generating Quiz", expanded=True)

    with quiz_status:

        st.write("Creating prompts :material/bolt:")
        all_qs_generated = qs_setGenerator_llm(easy_qs=easy_qs_topics, med_qs=med_qs_topics, hard_qs=hard_qs_topics)
        time.sleep(1.5)
        st.write("Selecting questions :material/checklist_rtl:")
        ai_generated_qs = model_text(all_qs_generated, transcript, easy_qs_topics, med_qs_topics, hard_qs_topics)
        time.sleep(0.5)
        st.write("Formatting requests :material/file_export:")
        all_requests = requests_set(
            ai_generated_qs,
            easy_qs_topics,
            easy_qs_num_topics,
            med_qs_topics,
            med_qs_num_topics,
            hard_qs_topics,
            hard_qs_num_topics,
        )
        time.sleep(1.5)
        st.write("Creating Google Form :material/add_to_drive:")
        get_result = auth_create(
            all_requests=all_requests,
            title=ai_generated_qs["title"],
            document_title=ai_generated_qs["document_title"],
            creds=creds
        )
        quiz_status.update(
            label="Completed", state="complete", expanded=False
        )
        time.sleep(1.5)
        quiz_status.empty()
        

        FormID = get_result["formId"]
        ResponderURL = get_result["responderUri"]
        
        return FormID, ResponderURL





if st.user.is_logged_in != True:
  st.title(":material/lock: Please login To Continue")
else :
    
    if "mg_token" not in st.session_state:
        st.session_state["mg_token"] = {
            "access_token": None,
            "token_type": None,
            "expires_in": None,
            "timestamp": None
    }

    if "user_token" not in st.session_state:
        st.session_state["user_token"] = {
            "user_token": None,
            "expires_in": None,
            "timestamp": None
    }

    if "cred" not in st.session_state:
        st.session_state.cred = ""

    st.title("QuizFlow.Ai", help = "", anchor=None)

    creds = st.session_state.get("cred")
    
    if creds == "" :
        creds = get_creds()

    
    text = st.text_input(f"**Type a few Topics** ↘️",max_chars=100, placeholder="Min. 20 words for accurate quiz generation", key="my_text")
    
    a, b, c, d, e, f, g, h, i = st.columns(
            [1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center"
    )
    with e:
        st.button(
            "Generate Quiz", key = "btn1_topics", icon="✍️",
            on_click=btn1_topics,
            use_container_width=True,
            type=st.session_state.btn1_topics_color,
        )
    if st.session_state.btn1_topics_clicked == True:
        
        ############################################################
        
        a, b, c = st.columns([2, 2, 2], vertical_alignment="center", border=True)

        with a:
            easy_qs_topics = st.slider(
                "Number of Easy Questions",
                key="e",
                min_value=0,
                max_value=20,
                value=5,
                step=1,
            )
        with b:
            med_qs_topics = st.slider(
                "Number of Medium Questions",
                key="m",
                min_value=0,
                max_value=20,
                value=6,
                step=1,
            )
        with c:
            hard_qs_topics = st.slider(
                "Number of Hard Questions",
                key="h",
                min_value=0,
                max_value=20,
                value=3,
                step=1,
            )

        d, e, f = st.columns([2, 2, 2], vertical_alignment="center", border=False)

        with d:
            easy_qs_num_topics = st.number_input(
                "Points Per Question in Easy Section",
                key="en",
                min_value=1,
                max_value=20,
                value=1,
                step=1,
            )
        with e:
            med_qs_num_topics = st.number_input(
                "Points Per Question in Medium Section",
                key="mn",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
            )
        with f:
            hard_qs_num_topics = st.number_input(
                "Points Per Question in Hard Section",
                key="hn",
                min_value=1,
                max_value=20,
                value=10,
                step=1,
            )
            
    ############################################################
        a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")

        with e: # -- Button 2 -- #
            st.button(
                "Generate", key = "btn2_topics", icon="🚀",
                on_click=btn2_topics,
                use_container_width=True,
                type="primary",
            )
        if st.session_state.btn2_topics_clicked == True:
            
            FormID, ResponderURL = quiz()
            st.markdown(f"### 📤 Share this Quiz: [{ResponderURL}]({ResponderURL})")
            st.markdown(f"### 📝 Edit Your Form: [https://docs.google.com/forms/d/{FormID}/edit](https://docs.google.com/forms/d/{FormID}/edit)")
