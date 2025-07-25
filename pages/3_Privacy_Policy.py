import streamlit as st

# Configure page
st.set_page_config(
    page_title="QuizFlow - Privacy Policy",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if st.button("Back to Home", use_container_width=False, type="primary"):
    st.session_state["privacy_policy"] = False
    st.session_state["terms_of_service"] = False
    st.switch_page("Welcome.py")
    
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@100..900&display=swap');
    
    .main {
        font-family: "Geist", sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .stMarkdown {
        font-family: "Geist", sans-serif;
    }
    
    /* Effective date styling */
    .effective-date-privacy {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .effective-date-terms {
        background-color: #fdf2f2;
        border-left: 4px solid #e74c3c;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .contact-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .disclaimer {
        background-color: #fff3cd;
        padding: 15px;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .important {
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Create tabs


st.markdown("""
# Privacy Policy for QuizFlow
""")

# Effective date box
st.markdown("""
<div class="effective-date-privacy">
    <strong>Effective Date:</strong> July 23, 2025<br>
    <strong>Last Updated:</strong> July 23, 2025
</div>
""", unsafe_allow_html=True)

st.markdown("""
## 1. Introduction

Welcome to QuizFlow ("we," "our," or "us"). This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our web application located at [https://quizflow.streamlit.app/](https://quizflow.streamlit.app/) (the "Service").

Please read this Privacy Policy carefully. If you do not agree with the terms of this Privacy Policy, please do not access the Service.

## 2. Information We Collect

### 2.1 Personal Information

We may collect personally identifiable information that you provide directly to us, including but not limited to:

- Name and email address (through Google OAuth and Auth0 authentication)
- Google account profile information
- User preferences and settings
- Quiz responses and performance data

### 2.2 Automatically Collected Information

When you access our Service, we may automatically collect certain information, including:

- IP address and device information
- Browser type and version
- Operating system
- Access times and dates
- Pages viewed and features used
- Referring website addresses

### 2.3 Third-Party Authentication Data

Through our integration with Google OAuth and Auth0, we collect:

- Google account authentication tokens
- Basic profile information from your Google account
- Authentication status and session data

### 2.4 YouTube Content Data

When you use our YouTube integration features, we may collect:

- YouTube video URLs and metadata
- Video content for quiz generation purposes
- Usage patterns related to video content

## 3. How We Use Your Information

We use the collected information for the following purposes:

- To provide, operate, and maintain our Service
- To authenticate users through Google OAuth and Auth0
- To generate quizzes from YouTube content using yt-dlp
- To personalize your experience and improve our Service
- To analyze usage patterns and optimize performance
- To communicate with you about your account or our Service
- To comply with legal obligations and protect our rights

## 4. Information Sharing and Disclosure

### 4.1 Third-Party Service Providers

We share information with trusted third-party service providers:

- **Google APIs:** For authentication and Google services integration
- **Auth0:** For secure user authentication and identity management
- **Streamlit:** For application hosting and infrastructure
- **YouTube/yt-dlp:** For accessing and processing video content

### 4.2 Legal Requirements

We may disclose your information if required by law or in response to:

- Valid legal processes (subpoenas, court orders)
- Government investigations
- Protection of our rights, property, or safety
- Prevention of fraud or illegal activities

### 4.3 Business Transfers

In the event of a merger, acquisition, or sale of assets, your information may be transferred as part of that transaction.

## 5. Data Security

We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet is 100% secure.

Security measures include:

- Encryption of data in transit and at rest
- Secure authentication protocols (OAuth 2.0)
- Regular security assessments and updates
- Access controls and user permission management

## 6. Data Retention

We retain your personal information only as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required by law. Quiz data and user preferences may be stored indefinitely unless you request deletion.

## 7. Your Rights and Choices

Depending on your location, you may have certain rights regarding your personal information:

- **Access:** Request access to your personal information
- **Correction:** Request correction of inaccurate information
- **Deletion:** Request deletion of your personal information
- **Portability:** Request a copy of your data in a structured format
- **Opt-out:** Unsubscribe from marketing communications

To exercise these rights, please contact us at aritradhabal36@gmail.com.

## 8. Google API Services User Data Policy Compliance

Our use of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements. We:

- Only request access to data necessary for our Service functionality
- Do not use Google user data for advertising purposes
- Do not allow humans to read user data unless required for security purposes
- Do not transfer Google user data to third parties except as disclosed in this policy

## 9. International Data Transfers

Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place for such transfers in compliance with applicable data protection laws.

## 10. Children's Privacy

Our Service is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If we become aware that we have collected such information, we will take steps to delete it promptly.

## 11. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last Updated" date. Your continued use of the Service after changes constitutes acceptance of the updated policy.

## 12. Contact Information
""")

st.markdown("""
<div class="contact-info">
    <p>If you have any questions about this Privacy Policy, please contact us at:</p>
    <p><strong>Email:</strong> aritradhabal36@gmail.com<br>
    <strong>Address:</strong> Jalpaiguri, West Bengal, India<br>
    <strong>Website:</strong> <a href="https://quizflow.streamlit.app/">https://quizflow.streamlit.app/</a></p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
---
*This Privacy Policy was last updated on July 23, 2025 and is effective as of July 23, 2025.*
""")
