import streamlit as st
from authenticate import get_creds
from database import fetching_, buttons, fetching_curated
import time

from menu import menu
menu()

st.set_page_config(
    page_title="QuizFlow.Ai",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("QuizFlow.Ai", help = "", anchor=None)

def login():
    st.login("auth0")
def logout():
    st.logout()

def legal():
    if "privacy_policy" not in st.session_state:
        st.session_state["privacy_policy"] = False
    if "terms_of_service" not in st.session_state:
        st.session_state["terms_of_service"] = False
        
    def privacy():
        st.session_state["privacy_policy"] = True
        
    def terms():
        st.session_state["terms_of_service"] = True
        
    st.button("Privacy Policy", key="privacy_", on_click=lambda: privacy(),use_container_width=True, type="tertiary")
    st.button("Terms of Service", key="terms_", on_click=terms,use_container_width=True, type="tertiary")

    st.markdown(
        """<style>
            .element-container:nth-of-type(4) button {
                position: fixed;
                bottom: 3rem;
                right: 0;
                # background-color: white;
                # color: black;
                text-align: right;
                padding: 10px;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                border-top-left-radius: 12px;   
                display: block;
                text-align: right;
                text-decoration: none;
                color: black;
                font-size: 8px;
                width: fit-content;
            }
            .element-container:nth-of-type(5) button {
                position: fixed;
                bottom: 0;
                right: 0;
                background-color: white;
                color: black;
                text-align: right;
                padding: 10px;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                border-top-left-radius: 12px;   
                display: block;
                text-align: right;
                text-decoration: none;
                color: black;
                font-size: 8px;
                width: fit-content;
            }
        
            </style>""",
        unsafe_allow_html=True,
    )

    if st.session_state["privacy_policy"]:
        st.switch_page("pages/3_Privacy_Policy.py")
        st.session_state["privacy_policy"] = False
    if st.session_state["terms_of_service"]:
        st.switch_page("pages/4_Terms_and_Conditions.py")
        st.session_state["terms_of_service"] = False



if not st.user.is_logged_in:
    
    a , b = st.columns([1, 1], vertical_alignment="center")
    with a:
        st.image("images/left.png",use_container_width=True)
    with b:
        st.image("images/right_login.png", use_container_width=True)


    a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")
    with e:
        st.button(
                ":material/login: Log in", key = "login",
                on_click=login,
                use_container_width=True,
                type="primary",
            )
    
    legal()
    
else:
    
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
    

    a , b = st.columns([1, 1], vertical_alignment="center")
    with a:
        st.image("images/left.png",use_container_width=True)
    with b:
        st.image("images/right_logout.png", use_container_width=True)

    a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center") # LOGOUT BUTTON
    
    with e:
        if st.button(":material/wand_stars: Generate Yours", key = "switch", use_container_width=True,type="primary"):
            st.switch_page("pages/2_Youtube.py")
            
    with e:
        st.button(
            ":material/move_item: Log Out", key = "logout",
            on_click=logout,
            use_container_width=True,
        )

    get_creds()
    
    if "user_data_all" not in st.session_state:
        st.session_state.user_data_all = None
    if "user_data_topics" not in st.session_state:
        st.session_state.user_data_topics = None
    if "user_data_youtube" not in st.session_state:
        st.session_state.user_data_youtube = None

    with st.sidebar:
        if not fetching_(st.user.email):
            time.sleep(1)
            st.toast(f"**Welcome {st.user.given_name}! Try creating your first quiz**", icon="🙌")
        else:
            selected_val = st.selectbox(f"**Your Quizzes**", ["All", "Topics", "YouTube"], index=0, key="selecting_db", on_change=None, placeholder=None, width="stretch")
            
            if selected_val == "All":
                if st.session_state.user_data_all is None:
                    st.session_state.user_data_all = fetching_(st.user.email)
                buttons(st.session_state.user_data_all)
            if selected_val == "Topics":
                if st.session_state.user_data_topics is None:
                    st.session_state.user_data_topics = fetching_curated(st.user.email, "Topics")
                buttons(st.session_state.user_data_topics)
            if selected_val == "YouTube":
                if st.session_state.user_data_youtube is None:
                    st.session_state.user_data_youtube = fetching_curated(st.user.email, "YouTube")
                buttons(st.session_state.user_data_youtube)
                



