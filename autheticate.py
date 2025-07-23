import streamlit as st
import time
import json
import http.client
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
import google.auth.exceptions
from googleapiclient.errors import HttpError



DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

domain = st.secrets['auth']['auth0']['domain']
client_id = st.secrets['auth']['auth0']['client_id']
client_secret = st.secrets['auth']['auth0']['client_secret']
audience = st.secrets['auth']['auth0']['audience']
grant_type = st.secrets['auth']['auth0']['grant_type']


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



def google_token():
    
        
    msg_toast = st.toast(f"Loading :material/sync:")

    def access_token_exp24():
        conn = http.client.HTTPSConnection(domain)
        payload = (
            f"{{"
            f"\"client_id\":\"{client_id}\","
            f"\"client_secret\":\"{client_secret}\","
            f"\"audience\":\"{audience}\","
            f"\"grant_type\":\"{grant_type}\""
            f"}}"
        )
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
                
        access_token = data["access_token"]
        bearer = data["token_type"]
        
        st.session_state["mg_token"] = {
            "access_token": access_token,
            "token_type": bearer,
            "expires_in": 86300,
            "timestamp": time.time()
        }
        return True
    
    if st.session_state.mg_token['access_token'] is None or st.session_state.mg_token['token_type'] is None or st.session_state.mg_token['expires_in'] is None or st.session_state.mg_token['timestamp'] is None:
        processed =  access_token_exp24()
        if processed:
            msg_toast.toast(f"Still Loading...")

    else:
        now = time.time()
        token_data = st.session_state.mg_token
        if now > token_data['timestamp']+token_data['expires_in']:
            processed = access_token_exp24()
            if processed:
                msg_toast.toast("**Access Token Expired, Fetched New Token**")

    
    def user_token_google():
        
        access_token = st.session_state.mg_token['access_token']
        bearer = st.session_state.mg_token['token_type']
        sub = st.user['sub']
        user_id = sub.split("|")[0], sub.split("|")[1]
        url = f"https://{domain}/api/v2/users/{user_id[0]}%7C{user_id[1]}"
        
        payload = {}
        headers = {
        'Accept': 'application/json',
        'Authorization': f'{bearer} {access_token}',
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        user_ = response.json()
        

        nonlocal user_token
        user_token = user_["identities"][0]["access_token"]
        expires_in = user_['identities'][0]['expires_in']
        
        st.session_state["user_token"] = {
            "user_token": user_token,
            "expires_in": expires_in,
            "timestamp": time.time()
        }
        return True
    
    if st.session_state.user_token['user_token'] is None or st.session_state.user_token['expires_in'] is None or st.session_state.user_token['timestamp'] is None:
        processed = user_token_google()
        if processed:
            msg_toast.toast(f"Fetched new credentials for {st.user['given_name']}")
    else:
        now = time.time()
        user_token = st.session_state.user_token
        if now > user_token['timestamp'] + 3300:
            processed = user_token_google()
            if processed:
                msg_toast.toast(f"Expired! Fetched New credentials for {st.user['given_name']}")
        else:
            msg_toast.toast(f"Connected with {st.user['given_name']}'s Credentials")
    
    time.sleep(0.5)
    msg_toast.toast("Checking Credentials",icon="↗️")
    return user_token


def get_form(creds):
    
    form_check = st.toast(f"Checking Form Access :material/folder_open:")
    form_service = build(
        "forms",
        "v1",
        credentials=creds,
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )
    form_check.toast(f"Contacting Google Forms :material/import_contacts:")
    form_id = "abc"
    try:
        request = form_service.forms().get(formId=form_id)
        form = request.execute()
        
    except google.auth.exceptions.RefreshError:
        st.toast(f"**Session Expired! Please Login again to Continue**", icon = "⚠️")
        return 1
        
    except HttpError as err:
        form_check.toast(f"**Connected with {st.user['given_name']}'s Google Form :material/contract:**", icon="✅")
        return 2
    
def creds_():
    
    if st.session_state.cred == "":
        try:
            user_token = google_token()
            creds = Credentials(
                token=user_token,
                scopes=["https://www.googleapis.com/auth/forms.body"]
            )
            st.session_state.cred = creds
            
            processed = get_form(creds)

            if processed == 1:
                time.sleep(2)
                st.logout()
                st.rerun()
            if processed==2:
                return creds
    
        except GoogleAuthError as e:
            st.toast(f"**Session Expired! Please Login again to Continue**", icon = "⚠️")
            time.sleep(2)
            st.logout()
            st.rerun()
        except Exception as e:
            st.toast(f"**Session Expired! Please Login again to Continue**", icon = "⚠️")
            time.sleep(2)
            st.logout()
            st.rerun()
        
    else :
        st.toast(f"**Welcome Back {st.user['given_name']}!**")
    return st.session_state.cred

def get_creds():
    cred = creds_()
    return cred