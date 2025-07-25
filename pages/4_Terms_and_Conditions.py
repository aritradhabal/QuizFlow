import streamlit as st

# Configure page
st.set_page_config(
    page_title="QuizFlow - Terms and Conditions",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

#-----------
if st.button("Back to Home", use_container_width=False, type="primary"):
    st.session_state["privacy_policy"] = False
    st.session_state["terms_of_service"] = False
    st.switch_page("Welcome.py")

st.markdown("""
# Terms of Service for QuizFlow
""")

# Effective date box
st.markdown("""
<div class="effective-date-terms">
    <strong>Effective Date:</strong> July 23, 2025<br>
    <strong>Last Updated:</strong> July 23, 2025
</div>
""", unsafe_allow_html=True)

st.markdown("""
## 1. Agreement to Terms

By accessing or using QuizFlow ("Service") located at [https://quizflow.streamlit.app/](https://quizflow.streamlit.app/), you ("User" or "you") agree to be bound by these Terms of Service ("Terms"). If you disagree with any part of these Terms, you may not access the Service.

## 2. Description of Service

QuizFlow is a web application that allows users to generate quizzes from YouTube content. Our Service includes:

- User authentication through Google OAuth and Auth0
- YouTube video content processing using yt-dlp
- Quiz generation and management features
- Integration with Google APIs for enhanced functionality

## 3. User Accounts and Authentication

### 3.1 Account Creation

To use certain features of our Service, you must create an account by authenticating through:

- Google OAuth (Google account required)
- Auth0 authentication system

### 3.2 Account Responsibilities

You are responsible for:

- Maintaining the confidentiality of your account credentials
- All activities that occur under your account
- Ensuring your account information is accurate and up-to-date
- Notifying us immediately of any unauthorized use

### 3.3 Account Termination

We reserve the right to terminate or suspend your account at our discretion for violations of these Terms or for any other reason.

## 4. Acceptable Use Policy

### 4.1 Permitted Uses

You may use our Service to:

- Generate educational quizzes from publicly available YouTube content
- Access and manage your quiz data
- Use features provided within the intended functionality

### 4.2 Prohibited Uses

You may **NOT** use our Service to:

- Violate any applicable laws or regulations
- Infringe upon intellectual property rights
- Upload, share, or process copyrighted content without permission
- Attempt to gain unauthorized access to our systems
- Use the Service for commercial purposes without permission
- Harass, abuse, or harm other users
- Distribute malware, viruses, or harmful code
- Circumvent security measures or authentication systems

## 5. Intellectual Property Rights

### 5.1 Our Content

The Service and its original content, features, and functionality are owned by QuizFlow and are protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.

### 5.2 User Content

You retain ownership of content you create through our Service. By using our Service, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, and display your content solely for providing and improving our Service.

### 5.3 Third-Party Content

Our Service may access YouTube content through yt-dlp. You acknowledge that:

- You must comply with YouTube's Terms of Service
- Content accessed belongs to its respective owners
- We do not claim ownership of third-party content
- You are responsible for ensuring you have rights to use accessed content

## 6. Privacy and Data Protection

Your privacy is important to us. Our collection and use of your information is governed by our Privacy Policy, which is incorporated into these Terms by reference. By using our Service, you consent to the collection and use of your information as described in our Privacy Policy.

## 7. Google API Services

Our Service uses Google API Services, and your use is subject to:

- Google API Services Terms of Service
- Google Privacy Policy
- Any additional Google product-specific terms

We comply with Google's API Services User Data Policy, including Limited Use requirements.

## 8. Third-Party Services

Our Service integrates with third-party services including:

- **Google APIs:** Subject to Google's terms and policies
- **Auth0:** Subject to Auth0's terms of service
- **Streamlit:** Subject to Streamlit's terms and conditions
- **YouTube/yt-dlp:** Subject to YouTube's Terms of Service

You are responsible for complying with all applicable third-party terms.

## 9. Service Availability and Modifications

### 9.1 Service Availability

We strive to maintain Service availability but do not guarantee uninterrupted access. The Service may be temporarily unavailable due to:

- Scheduled maintenance
- Technical difficulties
- Circumstances beyond our control

### 9.2 Service Modifications

We reserve the right to:

- Modify or discontinue the Service at any time
- Update features and functionality
- Change these Terms with appropriate notice

## 10. Disclaimers and Limitations of Liability
""")

st.markdown("""
<div class="disclaimer">
    <h3>10.1 Disclaimers</h3>
    <p class="important">The service is provided "as is" and "as available" without warranties of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, and non-infringement.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    <h3>10.2 Limitation of Liability</h3>
    <p class="important">To the maximum extent permitted by law, we shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to loss of profits, data, or other intangible losses.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## 11. Indemnification

You agree to indemnify, defend, and hold harmless QuizFlow and its officers, directors, employees, and agents from any claims, damages, losses, or expenses arising from:

- Your use of the Service
- Your violation of these Terms
- Your violation of third-party rights
- Your violation of applicable laws

## 12. Termination

### 12.1 Termination by You

You may terminate your account at any time by discontinuing use of the Service and requesting account deletion.

### 12.2 Termination by Us

We may terminate or suspend your access immediately for:

- Violation of these Terms
- Fraudulent or illegal activity
- Extended periods of inactivity
- Any other reason at our sole discretion

### 12.3 Effect of Termination

Upon termination:

- Your right to use the Service ceases immediately
- We may delete your account and data
- Provisions that should survive termination will remain in effect

## 13. Governing Law and Dispute Resolution

### 13.1 Governing Law

These Terms are governed by and construed in accordance with the laws of India, without regard to conflict of law principles.

### 13.2 Dispute Resolution

Any disputes arising from these Terms or your use of the Service shall be resolved through:

1. Good faith negotiations
2. Binding arbitration if negotiations fail
3. Courts of West Bengal, India for matters not subject to arbitration

## 14. General Provisions

### 14.1 Entire Agreement

These Terms, together with our Privacy Policy, constitute the entire agreement between you and QuizFlow regarding the Service.

### 14.2 Severability

If any provision of these Terms is found to be unenforceable, the remaining provisions will remain in full force and effect.

### 14.3 Waiver

Our failure to enforce any provision of these Terms does not constitute a waiver of that provision.

### 14.4 Assignment

You may not assign your rights under these Terms. We may assign our rights to any affiliate or successor.

## 15. Contact Information
""")

st.markdown("""
<div class="contact-info">
    <p>If you have any questions about these Terms, please contact us at:</p>
    <p><strong>Email:</strong> aritradhabal36@gmail.com<br>
    <strong>Address:</strong> Jalpaiguri, West Bengal, India<br>
    <strong>Website:</strong> <a href="https://quizflow.streamlit.app/">https://quizflow.streamlit.app/</a></p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    ## 16. Updates to Terms
    
    We reserve the right to update these Terms at any time. We will notify users of significant changes by:
    
    - Posting the updated Terms on our website
    - Sending email notifications to registered users
    - Displaying prominent notices within the Service
    
    Your continued use of the Service after changes constitutes acceptance of the updated Terms.
    
    ---
    
    *These Terms of Service were last updated on July 23, 2025 and are effective as of July 23, 2025.*
    """)