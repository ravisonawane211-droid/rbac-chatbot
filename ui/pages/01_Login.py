import streamlit as st
import requests
from app.schemas.login_request import LoginRequest
from app.utils.logger import get_logger
import base64

logger = get_logger(__name__)

st.set_page_config(
    page_title="FinSolve Technologies | Secure Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 🔥 ENTERPRISE FINTECH CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

:root {
    --primary: #6366f1;
    --accent: #22d3ee;
    --bg-dark: #0f172a;
    --glass: rgba(255,255,255,0.08);
    --text: #e2e8f0;
    --muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0b0f1a 50%);
    color: var(--text);
    overflow: hidden;
}

/* Hide Streamlit UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* -------------------- */
/* Animated Background  */
/* -------------------- */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    width: 700px;
    height: 700px;
    border-radius: 50%;
    filter: blur(180px);
    opacity: 0.5;
    z-index: -1;
    animation: float 20s ease-in-out infinite;
}

.stApp::before {
    background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0b0f1a 50%);
    top: -250px;
    left: -250px;
}

.stApp::after {
    background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0b0f1a 50%);
    bottom: -250px;
    right: -250px;
    animation-delay: 5s;
}

@keyframes float {
    0% { transform: translate(0px,0px); }
    50% { transform: translate(60px,40px); }
    100% { transform: translate(0px,0px); }
}

/* -------------------- */
/* Glass Login Card     */
/* -------------------- */
.login-card {
    max-width: 420px;
    margin: 6rem auto;
    padding: 2.5rem;
    background: var(--glass);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}

.login-title {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.login-subtitle {
    text-align: center;
    color: var(--muted);
    margin-bottom: 2rem;
    font-size: 0.95rem;
}


/* Label color */
label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Username & Password input fields */
.stTextInput > div > div > input {
    background: #ffffff !important;   /* White background */
    color: #000000 !important;        /* Black typed text */
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 0.75rem !important;
}

/* Placeholder color */
.stTextInput > div > div > input::placeholder {
    color: #6b7280 !important;
}

/* Login Button */
div.stButton > button {
    background: linear-gradient(135deg,#6366f1,#22d3ee);
    border-radius: 12px;
    border: none;
    color: white;
    font-weight: 600;
    padding: 0.8rem;
    width: 100%;
    transition: 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99,102,241,0.4);
}

/* Responsive */
@media (max-width: 600px) {
    .login-card {
        margin: 2rem 1rem;
        padding: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔐 LOGIN CARD UI
# -----------------------------

def submit_login(user_name: str, password: str):
    logger.info(f"Submitting login for user {user_name}")

    login_request = LoginRequest(user_name=user_name, password=password)

    try:
        login_response = requests.post(
            url="https://rbac-chatbot.onrender.com/users/login",
            json=login_request.model_dump()
        )
        login_response = login_response.json()

        if login_response['status'] == "success":
            st.session_state["logged_in"] = True
            st.session_state["access_token"] = login_response["access_token"]
            st.session_state["conversation_id"] = login_response["conversation_id"]
            st.session_state["user"] = login_response["user"]
            st.session_state["login_success_msg"] = login_response["message"]
        else:
            st.session_state["logged_in"] = False
            st.session_state["login_success_msg"] = "Invalid credentials."
    except Exception as e:
        logger.error(f"Login API error: {e}")
        st.session_state["logged_in"] = False
        st.session_state["login_success_msg"] = "Server connection error."



login_container = st.container()

with login_container:
    st.markdown(
        """
        <div class="login-card">
        <div class="login-title">🏦 FinSolve Technologies</div>
        <div class="login-subtitle">Secure AI Banking Assistant Access</div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    st.write("")

    if st.button("Secure Login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:  
            submit_login(username, password)

            if st.session_state.get("logged_in"):
                st.success(st.session_state.get("login_success_msg", "Login successful"))
                st.switch_page("pages/02_Home.py")
            else:
                st.error(st.session_state.get("login_success_msg", "Login failed"))

    st.markdown("</div>", unsafe_allow_html=True)
