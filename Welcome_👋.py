import streamlit as st
from authenticate import get_creds

    
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
            st.switch_page("pages/1_Topics.py")
            
    with e:
        st.button(
            ":material/move_item: Log Out", key = "logout",
            on_click=logout,
            use_container_width=True,
        )

    get_creds()