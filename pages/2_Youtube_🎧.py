import streamlit as st
import re
import tempfile
from all_functions import (
    auth_create,
    model_,
    qs_setGenerator_llm,
    requests_set,
    call_yt,
    model_yt
)
import os
import whisper
from pydub import AudioSegment
import time
from yt_dlp import YoutubeDL
import uuid
from yt_dlp.utils import DownloadError
from authenticate import get_creds
from database import inserting_, fetching_, buttons, fetching_curated


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
    
st.set_page_config(
    page_title="QuizFlow.Ai",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)



if st.user.is_logged_in != True:
  def login():
    st.login("auth0")
  
  st.title(":material/lock: Please login To Continue")
  st.markdown("")
  a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")
  with e:
      st.button(
              ":material/login: Log in", key = "login",
              on_click=login,
              use_container_width=True,
              type="primary",
          )
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
    ###########################################################################
  
  if "user_data_all" not in st.session_state:
      st.session_state.user_data_all = None
  if "user_data_topics" not in st.session_state:
      st.session_state.user_data_topics = None
  if "user_data_youtube" not in st.session_state:
      st.session_state.user_data_youtube = None
  if "placeholder_yt" not in st.session_state:
      st.session_state.placeholder_yt = "https://www.youtube.com/watch?v=8t7MUD87_Kc"
  if "selected_val_yt" not in st.session_state:
      st.session_state.selected_val_yt = 2
###########################################################################

  with st.sidebar:
    selected_val = st.selectbox(f"**Your Quizzes**", ["All", "Topics", "YouTube"], index=st.session_state.selected_val_yt, key="selecting_db", on_change=None, placeholder=None, width="stretch")
    
    if selected_val == "All":
        if st.session_state.user_data_all is None or selected_val != st.session_state.selected_val_yt:
            all_data_yt = fetching_(st.user.email)
            if all_data_yt == []:
              st.write("**Nothing to display here!**")
            else: 
              st.session_state.user_data_all = all_data_yt
              buttons(st.session_state.user_data_all)
    if selected_val == "Topics":
        if st.session_state.user_data_topics is None or selected_val != st.session_state.selected_val_yt:
            user_data_topics_yt = fetching_curated(st.user.email, "Topics")
            if user_data_topics_yt == []:
              st.write("**Nothing to display here!**")
            else :
              st.session_state.user_data_topics = user_data_topics_yt
              buttons(st.session_state.user_data_topics)
    if selected_val == "YouTube":
        if st.session_state.user_data_youtube is None or selected_val != st.session_state.selected_val_yt:
            user_data_youtube_yt = fetching_curated(st.user.email, "YouTube")
            if user_data_youtube_yt == []:
              st.write("**Try creating your first quiz!**")
            else:
              st.session_state.user_data_youtube = user_data_youtube_yt
              buttons(st.session_state.user_data_youtube)


###########################################################################
#SESSION STATES

  if "link_valid" not in st.session_state:
    st.session_state.link_valid = False
  if "btn1_clicked" not in st.session_state:
    st.session_state.btn1_clicked = False
  if "btn1_color" not in st.session_state:
    st.session_state.btn1_color = "primary"
  if "btn2_clicked" not in st.session_state:
    st.session_state.btn2_clicked = False
  # ---------- caching logic ------------- #
  if "transcription" not in st.session_state:
      st.session_state.transcription = None
  if "last_url" not in st.session_state:
      st.session_state.last_url = ""
  # ------------- Numbers ---------------------#
  if "easy_qs_last" not in st.session_state:
    st.session_state.easy_qs_last = None
  if "medium_qs_last" not in st.session_state:
    st.session_state.medium_qs_last = None
  if "hard_qs_last" not in st.session_state:
    st.session_state.hard_qs_last = None
  if "easy_qs_num_last" not in st.session_state:
    st.session_state.easy_qs_num_last = None
  if "medium_qs_num_last" not in st.session_state:
    st.session_state.medium_qs_num_last = None
  if "hard_qs_num_last" not in st.session_state:
    st.session_state.hard_qs_num_last = None

############## NUMBERS FOR API ------
  if "easy_qs_last_yt" not in st.session_state:
    st.session_state.easy_qs_last_yt = None
  if "medium_qs_last_yt" not in st.session_state:
    st.session_state.medium_qs_last_yt = None
  if "hard_qs_last_yt" not in st.session_state:
    st.session_state.hard_qs_last_yt = None
  if "easy_qs_num_last_yt" not in st.session_state:
    st.session_state.easy_qs_num_last_yt = None
  if "medium_qs_num_last_yt" not in st.session_state:
    st.session_state.medium_qs_num_last_yt = None
  if "hard_qs_num_last_yt" not in st.session_state:
    st.session_state.hard_qs_num_last_yt = None

  if "title" not in st.session_state:
    st.session_state.title = None
  if "tags" not in st.session_state:
    st.session_state.tags=None
  if "desc" not in st.session_state:
    st.session_state.desc=None
# ------------------------------------------------#

  if "btn2_ytclicked" not in st.session_state:
    st.session_state.btn2_ytclicked = False
  
  if "value_yt" not in st.session_state:
    st.session_state.value_yt = None
  if "value" not in st.session_state:
    st.session_state.value = None

  if "selection_pills" not in st.session_state:
    st.session_state.selection_pills = "YouTube API :material/bolt:"
  if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = None
    
  if "query_value" not in st.session_state:
    st.session_state.query_value = "" 
  
  if "changed" not in st.session_state:
    st.session_state.changed = False
  
  
  if len(st.query_params) > 0:
      st.session_state.query_value = st.query_params['url']
      
  ###########################################################################
  a,b = st.columns([5,2], vertical_alignment="center")
  with a:
    url = st.text_input("**Paste YouTube URL** ↘️", value=st.session_state.query_value, max_chars=100, key="yt_url", type="default", autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=st.session_state.placeholder_yt, disabled=False, label_visibility="visible", icon=None, width="stretch", help="YouTube API is much faster than Downloading, but it maybe less accurate. If Downloading fails try with YouTube API")
  with b:
    selection = st.pills(label=" ", options=["Download :material/cloud_download:","YouTube API :material/bolt:"],selection_mode="single",default=st.session_state.selection_pills,key="_pills", width="stretch")
    if selection != st.session_state.selection_pills:
      st.session_state.selection_pills = selection

  

  def load_model():
      model = whisper.load_model("base.pt")
      st.session_state.model_loaded = model
      return st.session_state.model_loaded
  if selection == "Download :material/cloud_download:" and st.session_state.model_loaded == None:
    model = load_model()
  else:
    model = st.session_state.model_loaded 
  # -------------------------------------------------
  def is_youtube_url(): # this function is used in the first button to determine is the text is actually a link or not
      if not url or not isinstance(url, str):
          return False

      pattern = re.compile(
          r'^(https?://)?'               
          r'([\w.-]+)'                   
          r'(\.[a-zA-Z]{2,})'            
          r'(/[^\s]*)?$',                
          re.IGNORECASE
      )
      return re.match(pattern, url.strip()) is not None


  def download(URL, temp_dir): #to download the video from the link
      random_filename = f"{st.session_state.session_id}.wav"
      temp_filepath = os.path.join(temp_dir, random_filename)

      def extract_percent(value):
          ansi_removed = re.sub(r'\x1b\[[0-9;]*m', '', value)
          match = re.search(r'([\d.]+)%', ansi_removed)
          if match:
              return float(match.group(1))
          return 0.0 

      download_bar = st.progress(0, text='Downloading 🤖')

      def progress_hook(d):
          if d['status'] == 'downloading':
              percent = extract_percent(d['_percent_str'])
              download_bar.progress(min(int(percent), 100), text = f"{int(percent)}% Loaded")

          if d['status'] == 'finished':
              download_bar.progress(100)
              download_bar.empty()
              download_success = st.success("Download Completed!", icon="🎉")
              time.sleep(0.5)
              download_success.empty()
              

      ydl_opts = {
          'quiet': True, 
          'format': 'bestaudio/best',
          'outtmpl': os.path.join(temp_dir, random_filename.replace('.wav', '.%(ext)s')),
          'progress_hooks': [progress_hook],
          'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'wav',
              'preferredquality': '192',
          }],
          'keepvideo': False,
      }
      try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])
      except DownloadError as e:
        st.toast(f"**Failed to download video. Needs account cache. Try Fetching through YouTube Data API.**", icon="🔁")
        st.warning(f"**Downloading Method works on [Streamlit hosted website](https://quizflow.streamlit.app/) only.**", icon="⚠️")
        st.session_state.last_url = url
        st.session_state.query_value = url
        del st.session_state['selection_pills']
        time.sleep(1.5)
        st.session_state.btn1_clicked = False
        st.session_state.changed = True
        st.rerun()

      except Exception as e:
        st.toast(f"**Failed to download video. Needs account cache. Try Fetching through YouTube Data API.**", icon="🔁")
        st.warning(f"**Downloading Method works on [Streamlit hosted website](https://quizflow.streamlit.app/) only.**", icon="⚠️")
        st.session_state.last_url = url
        st.session_state.query_value = url
        del st.session_state['selection_pills']
        st.session_state.btn1_clicked = False
        st.session_state.changed = True
        time.sleep(1.5)
        st.rerun()
      
      return temp_filepath

  def process(url):
    
    def truncate_context(text, max_len=500):
        return text[-max_len:]  
    
    with tempfile.TemporaryDirectory() as temp_dir:
    
      filename = download(url, temp_dir)
    ################
    #TRANSCRIPTION
    ################


    
      transcribe_bar = st.progress(0.0, text="Starting transcription...")
      
      audio = AudioSegment.from_file(filename)
      chunk_length_ms = 10 * 60 * 1000
      chunk_output_dir = os.path.join(temp_dir, f"chunks_{st.session_state.session_id}")

      os.makedirs(chunk_output_dir, exist_ok=True)
      total_length = len(audio)
      num_chunks = (total_length + chunk_length_ms - 1) // chunk_length_ms
      
      all_text = ""
      prev_text = ""
      t0 = time.time()
      
      for i in range(num_chunks):
        transcribe_bar.progress((i + 0.1) / num_chunks, text=f"Transcribing chunk {i+1}/{num_chunks}")
        start = i * chunk_length_ms
        end = min((i + 1) * chunk_length_ms, total_length)
        chunk = audio[start:end]

        chunk_filename = os.path.join(chunk_output_dir, f"chunk_{st.session_state.session_id}_{i}.wav")
        chunk = chunk.normalize()
        chunk.export(chunk_filename, format="wav")
        
        result = model.transcribe(
            chunk_filename,
            condition_on_previous_text=False,
            initial_prompt=truncate_context(prev_text)
        )
        transcribe_bar.progress((i + 1) / num_chunks, text=f"Transcribed chunk {i+1}/{num_chunks}")

        curr_text = result["text"]
        prev_text = curr_text
        all_text += curr_text
            
        
        if i == 0 and num_chunks>1:
          end = time.time()
          interval = end-t0
          if (interval*(num_chunks-1))<60:
            st.toast(f"**Estimated Time: {((interval))*(num_chunks-1):.1f} seconds**")
          else :
              st.toast(f"**Estimated time : {((interval)/60)*(num_chunks-1):.1f} minutes**")

      transcribe_bar.empty()
      t0_completed = st.success("Transcription Completed!", icon="🎉")
      time.sleep(0.5)
      t0_completed.empty()
      return all_text


  def btn1():
    
    if (url != st.session_state.last_url and len(url)>0) or st.session_state.changed == True:
      st.session_state.transcription = None
      st.session_state.last_url = url

      st.session_state.value = None
      st.session_state.value_yt = None
    
      st.session_state.btn1_clicked = True
      st.session_state.transcription = None
      st.session_state.link_valid = is_youtube_url()    
      st.session_state.btn2_clicked = False
      st.session_state.btn2_ytclicked = False
      
      st.session_state.title = None
      st.session_state.tags = None
      st.session_state.desc = None
      
  def btn2():
    if easy_qs != st.session_state.easy_qs_last or med_qs != st.session_state.medium_qs_last or hard_qs != st.session_state.hard_qs_last or easy_qs_num != st.session_state.easy_qs_num_last or med_qs_num != st.session_state.medium_qs_num_last or hard_qs_num != st.session_state.hard_qs_num_last:
      
      st.session_state.easy_qs_last = easy_qs
      st.session_state.medium_qs_last = med_qs
      st.session_state.hard_qs_last = hard_qs
      st.session_state.easy_qs_num_last = easy_qs_num
      st.session_state.medium_qs_num_last = med_qs_num
      st.session_state.hard_qs_num_last = hard_qs_num
      st.session_state.btn2_clicked = True
          
    st.session_state.btn1_color = "secondary" 


  def btn2_yt():
    if easy_qs_yt != st.session_state.easy_qs_last_yt or med_qs_yt != st.session_state.medium_qs_last_yt or hard_qs_yt != st.session_state.hard_qs_last_yt or easy_qs_num_yt != st.session_state.easy_qs_num_last_yt or med_qs_num_yt != st.session_state.medium_qs_num_last_yt or hard_qs_num_yt != st.session_state.hard_qs_num_last_yt:
      
        st.session_state.easy_qs_last_yt = easy_qs_yt
        st.session_state.medium_qs_last_yt = med_qs_yt
        st.session_state.hard_qs_last_yt = hard_qs_yt
        st.session_state.easy_qs_num_last_yt = easy_qs_num_yt
        st.session_state.medium_qs_num_last_yt = med_qs_num_yt
        st.session_state.hard_qs_num_last_yt = hard_qs_num_yt
        st.session_state.btn2_ytclicked = True
      
    st.session_state.btn1_color = "secondary" 
      

  def quiz():
    
    transcript = all_text
    quiz_status = st.status("🧠 Generating Quiz", expanded=True)
    
    with quiz_status:
    
      st.write("Creating prompts :material/bolt:")
      all_qs_generated = qs_setGenerator_llm(easy_qs=easy_qs, med_qs=med_qs, hard_qs=hard_qs)
      time.sleep(1.5)
      st.write("Selecting questions :material/checklist_rtl:")
      ai_generated_qs = model_(all_qs_generated, transcript, easy_qs, med_qs, hard_qs)
      time.sleep(0.5)
      st.write("Formatting requests :material/file_export:")
      all_requests = requests_set(
          ai_generated_qs,
          easy_qs,
          easy_qs_num,
          med_qs,
          med_qs_num,
          hard_qs,
          hard_qs_num,
      )
      
      time.sleep(1.5)
      st.write("Creating Google Form :material/add_to_drive:")
      
      try :
        get_result = auth_create(
          all_requests=all_requests,
          title=ai_generated_qs["title"],
          document_title=ai_generated_qs["document_title"],
          creds=creds
        )
      except Exception as e:
          st.error(f"Error creating Google Form! Refreshing...", icon="⚠️")
          time.sleep(1.5)
          st.rerun()
      quiz_status.update(
          label="Completed", state="complete", expanded=False
      )
      time.sleep(1)
    
      FormID = get_result["formId"]
      ResponderURL = get_result["responderUri"]
      doc_title = get_result["info"]["documentTitle"]

      bool = inserting_(email=st.user.email, form_title=doc_title, form_url=ResponderURL, form_edit_url=f"https://docs.google.com/forms/d/{FormID}/edit", origin="YouTube")
      if bool:
        st.session_state.user_data_youtube = None
      
      
      quiz_status.empty()
      return FormID, ResponderURL


  def quiz_yt():
  
    quiz_status = st.status("🧠 Generating Quiz", expanded=True)
    
    with quiz_status:
    
      st.write("Creating prompts :material/bolt:")
      all_qs_generated = qs_setGenerator_llm(easy_qs=easy_qs_yt, med_qs=med_qs_yt, hard_qs=hard_qs_yt)
      time.sleep(1.5)
      st.write("Selecting questions :material/checklist_rtl:")
      ai_generated_qs = model_yt(all_qs_generated, easy_qs_yt, med_qs_yt, hard_qs_yt, st.session_state.title, st.session_state.desc, st.session_state.tags)
      time.sleep(0.5)
      st.write("Formatting requests :material/file_export:")
      all_requests = requests_set(
          ai_generated_qs,
          easy_qs_yt,
          easy_qs_num_yt,
          med_qs_yt,
          med_qs_num_yt,
          hard_qs_yt,
          hard_qs_num_yt,
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

      bool = inserting_(email=st.user.email, form_title=doc_title, form_url=ResponderURL, form_edit_url=f"https://docs.google.com/forms/d/{FormID}/edit", origin="YouTube")
      if bool:
        st.session_state.user_data_youtube = None
      
      
      quiz_status.empty()
      return FormID, ResponderURL






  a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")

  with e: # -- Button 1
    st.button(
          "Generate Quiz", key = "btn1", icon="✍️",
          on_click=btn1,
          use_container_width=True,
          type=st.session_state.btn1_color,
      )

  if st.session_state.btn1_clicked == True:
    if selection == "Download :material/cloud_download:":
      if st.session_state.link_valid:
        if st.session_state.transcription is None:
          with st.spinner("Processing ⚙️"):
            st.session_state.transcription = process(url)
        
        all_text = st.session_state.transcription
        
        if len(all_text) != 0:
          with st.expander(label = "View Transcription ", icon = "⤵️", expanded=False):
            st.write(all_text)
            
    ##########################################
        a, b, c = st.columns([2, 2, 2], vertical_alignment="center", border=True)

        with a:
            easy_qs = st.slider(
                "Number of Easy Questions",
                key="e",
                min_value=0,
                max_value=20,
                value=5,
                step=1,
            )
        with b:
            med_qs = st.slider(
                "Number of Medium Questions",
                key="m",
                min_value=0,
                max_value=20,
                value=6,
                step=1,
            )
        with c:
            hard_qs = st.slider(
                "Number of Hard Questions",
                key="h",
                min_value=0,
                max_value=20,
                value=3,
                step=1,
            )

        d, e, f = st.columns([2, 2, 2], vertical_alignment="center", border=False)

        with d:
            easy_qs_num = st.number_input(
                "Points Per Question in Easy Section",
                key="en",
                min_value=1,
                max_value=20,
                value=1,
                step=1,
            )
        with e:
            med_qs_num = st.number_input(
                "Points Per Question in Medium Section",
                key="mn",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
            )
        with f:
            hard_qs_num = st.number_input(
                "Points Per Question in Hard Section",
                key="hn",
                min_value=1,
                max_value=20,
                value=10,
                step=1,
            )
    #############################################
      
      
        a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")

        with e: # -- Button 2 -- #
          st.button(
                "Generate", key = "btn2", icon="🚀",
                on_click=btn2,
                use_container_width=True,
                type="primary",
            )
        if st.session_state.btn2_clicked == True:
          if st.session_state.value is None:
            st.session_state.value = quiz()
            st.session_state.placeholder_yt = url
            st.rerun()
          FormID, ResponderURL = st.session_state.value
          st.markdown(f"### 📤 Share this Quiz: [{ResponderURL}]({ResponderURL})")
          st.markdown(f"### 📝 Edit Your Form: [https://docs.google.com/forms/d/{FormID}/edit](https://docs.google.com/forms/d/{FormID}/edit)")

        
        
      else:
        
        st.warning("🔗 Please Enter a Valid URL")

    else:
      
      if st.session_state.title == None and st.session_state.tags==None and st.session_state.desc == None:
        title, desc, tags = call_yt(url=url)
        st.session_state.title = title
        st.session_state.tags = tags
        st.session_state.desc = desc

##########################################
      a, b, c = st.columns([2, 2, 2], vertical_alignment="center", border=True)

      with a:
          easy_qs_yt = st.slider(
              "Number of Easy Questions",
              key="e",
              min_value=0,
              max_value=20,
              value=5,
              step=1,
          )
      with b:
          med_qs_yt = st.slider(
              "Number of Medium Questions",
              key="m",
              min_value=0,
              max_value=20,
              value=6,
              step=1,
          )
      with c:
          hard_qs_yt = st.slider(
              "Number of Hard Questions",
              key="h",
              min_value=0,
              max_value=20,
              value=3,
              step=1,
          )

      d, e, f = st.columns([2, 2, 2], vertical_alignment="center", border=False)

      with d:
          easy_qs_num_yt = st.number_input(
              "Points Per Question in Easy Section",
              key="en",
              min_value=1,
              max_value=20,
              value=1,
              step=1,
          )
      with e:
          med_qs_num_yt = st.number_input(
              "Points Per Question in Medium Section",
              key="mn",
              min_value=1,
              max_value=20,
              value=5,
              step=1,
          )
      with f:
          hard_qs_num_yt = st.number_input(
              "Points Per Question in Hard Section",
              key="hn",
              min_value=1,
              max_value=20,
              value=10,
              step=1,
          )
      #############################################


      a, b, c, d, e, f, g, h, i = st.columns([1, 2, 3, 4, 5, 4, 3, 2, 1], vertical_alignment="center")

      with e: # -- Button 2 -- #
        st.button(
              "Generate", key = "btn2_yt", icon="🚀",
              on_click=btn2_yt,
              use_container_width=True,
              type="primary",
          )
      if st.session_state.btn2_ytclicked == True:
        if st.session_state.value_yt is None:
          st.session_state.value_yt = quiz_yt()
          st.session_state.placeholder_yt = url
          st.rerun()
        FormID, ResponderURL = st.session_state.value_yt
        st.markdown(f"### 📤 Share this Quiz: [{ResponderURL}]({ResponderURL})")
        st.markdown(f"### 📝 Edit Your Form: [https://docs.google.com/forms/d/{FormID}/edit](https://docs.google.com/forms/d/{FormID}/edit)")
        


