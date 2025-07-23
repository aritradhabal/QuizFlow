import streamlit as st
from all_functions import (
    auth_create,
    model_text,
    qs_setGenerator_llm,
    requests_set,
)
import time
from authenticate import get_creds
from database import inserting_, fetching_, buttons, fetching_curated

    
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
    
if "value_topic" not in st.session_state:
    st.session_state.value_topic = None
    
if "placeholder" not in st.session_state:
    st.session_state.placeholder = "Min. 20 words for accurate quiz generation"
    
###########################################################################






def btn1_topics():
    if len(text)<10:
        st.toast(f"**Please enter at least 20 words about your topic.**", icon="🚫")
    elif text == st.session_state.last_text:
        st.toast(f"**Please change the topic to generate a new quiz.**", icon="🚫")
    else:
        st.session_state.last_text = text
        st.session_state.btn1_topics_clicked = True
        st.session_state.btn2_topics_clicked = False
        st.session_state.value_topic = None


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
        time.sleep(1)
        
        FormID = get_result["formId"]
        ResponderURL = get_result["responderUri"]
        doc_title = get_result["info"]["documentTitle"]

        bool = inserting_(email=st.user.email, form_title=doc_title, form_url=ResponderURL, form_edit_url=f"https://docs.google.com/forms/d/{FormID}/edit", origin="Topics")
        if bool:
            st.session_state.user_data_topics = None
        quiz_status.empty()
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


    text = st.text_input(f"**Type a few Topics** ↘️",max_chars=100, placeholder=st.session_state.placeholder, key="my_text")

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
    ##############################################################
    
      
    if "user_data_all" not in st.session_state:
        st.session_state.user_data_all = None
    if "user_data_topics" not in st.session_state:
        st.session_state.user_data_topics = None
    if "user_data_youtube" not in st.session_state:
        st.session_state.user_data_youtube = None
    if "selected_val_topics" not in st.session_state:
        st.session_state.selected_val_topics = 1
    
    ###########################################################################

    with st.sidebar:
        selected_val = st.selectbox(f"**Your Quizzes**", ["All", "Topics", "YouTube"], index=st.session_state.selected_val_topics, key="selecting_db", on_change=None, placeholder=None, width="stretch")


        if selected_val == "All":
            if st.session_state.user_data_all is None or selected_val != st.session_state.selected_val_topics:
                all_data_yt = fetching_(st.user.email)
                if all_data_yt == []:
                    st.write("**Nothing to display here!**")
                else: 
                    st.session_state.user_data_all = all_data_yt
                    buttons(st.session_state.user_data_all)
        if selected_val == "Topics":
            if st.session_state.user_data_topics is None or selected_val != st.session_state.selected_val_topics:
                user_data_topics_yt = fetching_curated(st.user.email, "Topics")
                if user_data_topics_yt == []:
                    st.write("**Try creating your first quiz!**")
                else:
                    st.session_state.user_data_topics = user_data_topics_yt
                    buttons(st.session_state.user_data_topics)
        if selected_val == "YouTube":
            if st.session_state.user_data_youtube is None or selected_val != st.session_state.selected_val_topics:
                user_data_youtube_yt = fetching_curated(st.user.email, "YouTube")
                if user_data_youtube_yt == []:
                    st.write("**Nothing to display here!**")
                else:
                    st.session_state.user_data_youtube = user_data_youtube_yt
                    buttons(st.session_state.user_data_youtube)


    
    
    
    
    
    
    ##################################################################
    
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
            if st.session_state.value_topic == None:
                st.session_state.value_topic = quiz()
                st.session_state.placeholder = text
                
                st.rerun()
            FormID, ResponderURL = st.session_state.value_topic
            st.markdown(f"### 📤 Share this Quiz: [{ResponderURL}]({ResponderURL})")
            st.markdown(f"### 📝 Edit Your Form: [https://docs.google.com/forms/d/{FormID}/edit](https://docs.google.com/forms/d/{FormID}/edit)")
