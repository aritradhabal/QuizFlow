import streamlit as st
import re
from all_functions import (
    auth_create,
    model_,
    model_text,
    qs_setGenerator_llm,
    requests_set,
)
from pydub import AudioSegment


    
st.set_page_config(
    page_title="QuizFlow.Ai",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("QuizFlow.Ai", help = "", anchor=None)
