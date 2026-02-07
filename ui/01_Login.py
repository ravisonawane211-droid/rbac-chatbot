import streamlit as st
import requests
from app.schemas.login_request import LoginRequest
from app.utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="FinSolve Login", page_icon="🔒", layout="centered", initial_sidebar_state="collapsed")

# --- Custom responsive CSS for a nicer login card ---
st.markdown(
    """
    <style>
    /* Background gradient */
    :root {
        --bg: #f6f7fb;
        --card: #ffffff;
        --muted: #6b7280;
        --accent: #06b6d4;
        --user-gradient: linear-gradient(90deg,#34d399 0%,#10b981 100%);
        --radius: 12px;
        --shadow: 0 8px 24px rgba(16,24,40,0.08);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    .stApp { background: var(--bg); min-height: 100vh; }

    /* Centered card */
    .login-card {
      max-width: 420px;
      margin: 3.5rem auto;
      background: rgba(255,255,255,0.95);
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15);
      font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .login-title {
      text-align: center;
      font-size: 1.6rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }
    .login-subtitle {
      text-align: center;
      color: #555;
      margin-bottom: 1.25rem;
    }
    /* Inputs */
    input[type='text'], input[type='password'] {
      border-radius: 8px !important;
      padding: 0.75rem !important;
      border: 1px solid #e6e6e6 !important;
      box-shadow: none !important;
    }
    /* Button */
    div.stButton > button {
      background: linear-gradient(90deg,#667eea,#764ba2) !important;
      color: white !important;
      border: none !important;
      padding: 0.7rem 1.1rem !important;
      border-radius: 8px !important;
      width: 100% !important;
      font-weight: 600 !important;
    }
    /* Responsive */
    @media (max-width: 600px) {
      .login-card { margin: 1rem; padding: 1.25rem; }
    }
    /* Hide Streamlit menu and footer for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Center the form using columns and a custom card
st.write("")  # spacer
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="login-title">Welcome To FinSolve Technologies</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Please sign in to continue to the FinSolve chatbot</div>', unsafe_allow_html=True)

def submit_login(user_name:str,password:str):
    logger.info(f"submitting user {user_name} login request to login API")

    login_request = LoginRequest(user_name=user_name,password=password)
    try:
        login_response = requests.post(url="https://rbac-chatbot.onrender.com/users/login",
                                    json=login_request.model_dump())
        login_response = login_response.json()
        if(login_response['status']=="success"):

            st.session_state["logged_in"] = True
            st.session_state["access_token"] = login_response["access_token"]
            st.session_state["conversation_id"] = login_response["conversation_id"]
            st.session_state["user"] = login_response["user"]
            st.session_state["login_success_msg"] = login_response["message"]
        else:
            st.session_state["logged_in"] = False
            st.session_state["access_token"] = None
            st.session_state["conversation_id"] = None
            st.session_state["user"] = None
            st.session_state["login_success_msg"] = "Error while login."
    except Exception as e:
        logger.error(f"error occurred while calling login API , error :{e}")
        st.session_state["logged_in"] = False
        st.session_state["access_token"] = None
        st.session_state["conversation_id"] = None
        st.session_state["user"] = None
        st.session_state["login_success_msg"] = "Exception occurred while login."


username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", type="password", placeholder="Enter your password")
st.write("")  # small spacer
if st.button("Login",type="primary"):
    submit_login(user_name=username,password=password)
    if st.session_state.get("logged_in"):
                st.success(st.session_state.get("login_success_msg", "Login successful!"))
                st.switch_page("pages/02_Home.py")
    else:
                st.error(st.session_state.get("login_success_msg", "Invalid username or password."))

st.markdown('</div>', unsafe_allow_html=True)