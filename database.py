import email
import streamlit as st
from supabase import create_client, Client
import time

SUPABASE_URL=st.secrets["db"]["supabase_url"]
SUPABASE_API=st.secrets["db"]["supabase_api"]


supabase: Client = create_client(SUPABASE_URL, SUPABASE_API)

# data = supabase.table("Forms").select("*").execute()


def buttons(data):
    def delete(id):
      data = supabase.table("Forms").delete().eq("id", id).execute()
      st.toast(f"**Form deleted successfully!**", icon="🗑️")
      st.session_state.user_data_all = None
      st.session_state.user_data_topics = None
      st.session_state.user_data_youtube = None
      
    for _ in data:
      id = _["id"]
      form_title = _["form_title"]
      form_url = _["form_url"]
      form_edit_url = _["form_edit_url"]
      col1, col2, col3 = st.columns([7, 2, 2], vertical_alignment="center", gap="small")
      with col1:
          st.link_button(f":material/arrow_outward: {form_title}", url=form_url, type="secondary", use_container_width=True)
      with col2:
          st.link_button(":material/contract_edit:", url=form_edit_url, type="secondary", use_container_width=True)
      with col3:
          st.button(":material/delete:", key=f"delete_{id}", on_click=lambda id=id: delete(id), type="secondary", use_container_width=True)


# data_insert = supabase.table("Forms").insert({"email":"aritradhabal@gmail.com", "form_title":"Example Form 3", "form_url": "http://example.com/form3", "form_edit_url": "http://example.com/edit"}).execute()


def inserting_(email, form_title, form_url, form_edit_url, origin):
  try:
    data_insert = supabase.table("Forms").insert({
        "email": email,
        "form_title": form_title,
        "form_url": form_url,
        "form_edit_url": form_edit_url,
        "origin": origin
    }).execute()
  except Exception as e:
    st.toast(f"**Error! Please try again Later**", icon="⚠️")
    return False
  return True



def fetching_(email):
  
  try:
    email = supabase.table("Forms").select("*").eq("email", email).order("created_at", desc=True).execute()
  except Exception as e:
    st.toast(f"**Error! Please try again Later**", icon="⚠️")
    return False

  return email.data
  
def fetching_curated(email, origin):
  
  try:
    email = supabase.table("Forms").select("*").eq("email", email).eq("origin", origin).order("created_at", desc=True).execute()
  except Exception as e:
    st.toast(f"**Error! Please try again Later**", icon="⚠️")
    return False

  return email.data

def update_last_login(email):
  now = round(time.time())
  prev = supabase.table("Forms").select("last_login").eq("email", email).limit(1).execute()
  if prev.data[0]['last_login'] == None:
      data = supabase.table("Forms").update({"last_login": now}).eq("email", email).execute()
  else:
    if now > prev.data[0]["last_login"]+3600:
      data = supabase.table("Forms").update({"last_login": now}).eq("email", email).execute()
    elif now > prev.data[0]["last_login"]+3300:
      st.toast(f"**Your session will expire in less than 5 minutes! Make sure to save your work.**", icon="⚠️")