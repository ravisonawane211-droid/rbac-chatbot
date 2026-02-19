import streamlit as st
import requests
from app.schemas.login_request import LoginRequest
from app.utils.logger import get_logger

st.set_page_config(page_title="Fin Assist AI", layout="wide")
logger = get_logger(__name__)

# ==========================================
# CUSTOM CSS (Top Navbar Style)
# ==========================================
st.markdown("""
<style>
            
.main-content {
    margin-top: 90px;
}

/* 🔥 Force form labels to white */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label,
div[data-testid="stNumberInput"] label {
    color: white !important;
}


/* Hide Streamlit UI */
section[data-testid="stSidebar"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Background */
.stApp {
    background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0b0f1a 50%);
    color: white;
}

/* Navbar */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(17,24,39,0.75);
    backdrop-filter: blur(12px);
    padding: 12px 40px;
    z-index: 999;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.spacer {
    height: 80px;
}
            
.blob {
    position: fixed;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle at center, rgba(124,58,237,0.4), transparent 70%);
    filter: blur(80px);
    z-index: -1;
    animation: float 12s ease-in-out infinite alternate;
}

.blob2 {
    position: fixed;
    right: 10%;
    top: 40%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle at center, rgba(59,130,246,0.4), transparent 70%);
    filter: blur(80px);
    z-index: -1;
    animation: float2 14s ease-in-out infinite alternate;
}

@keyframes float {
    from { transform: translate(-50px, -50px); }
    to { transform: translate(80px, 50px); }
}

@keyframes float2 {
    from { transform: translate(50px, 80px); }
    to { transform: translate(-60px, -40px); }
}

/* ---------- Glass Cards with Glow Hover ---------- */

.glass-card {
    background: rgba(255,255,255,0.04);
    padding: 30px;
    border-radius: 18px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.06);
    height: 100%;
    transition: all 0.35s ease;
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    transform: translateY(-8px);
    border: 1px solid rgba(124,58,237,0.7);
    box-shadow: 0 0 25px rgba(124,58,237,0.5);
}

/* ---------- Trusted Logos ---------- */

.logo-strip {
    display: flex;
    justify-content: space-between;
    align-items: center;
    opacity: 0.6;
    gap: 40px;
    margin-top: 40px;
    filter: grayscale(100%);
}

.logo-strip img {
    max-height: 40px;
}

/* 🔥 FORCE MENU BUTTON STYLE */
.nav-btn div[data-testid="stButton"] > button {
    background: transparent !important;
    border: none !important;
    color: #9CA3AF !important;   /* Soft gray */
    font-size: 15px;
    font-weight: 500;
    box-shadow: none !important;
}

/* Hover */
.nav-btn div[data-testid="stButton"] > button:hover {
    color: #E5E7EB !important;
    background: transparent !important;
}

/* Remove blue focus outline */
.nav-btn div[data-testid="stButton"] > button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Login button */
.login-btn div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#7C3AED,#3B82F6) !important;
    color: white !important;
    border-radius: 8px;
    padding: 6px 18px;
    font-weight: 600;
}
            
/* WHITE BUTTON → BLACK TEXT */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: white !important;
    color: black !important;
    border-radius: 8px;
    border: 1px solid #e5e7eb !important;
}

/* Hover effect */
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: #f3f4f6 !important;
    color: black !important;
}

/* Remove focus glow */
div[data-testid="stButton"] > button:focus {
    outline: none !important;
    box-shadow: none !important;
}          

.glass-section {
    background: rgba(255,255,255,0.05);
    padding: 50px;
    border-radius: 20px;
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 40px;
}

.glass-section:hover {
    transform: translateY(-8px);
    border: 1px solid rgba(124,58,237,0.7);
    box-shadow: 0 0 25px rgba(124,58,237,0.5);
}


.gradient-text {
    background: linear-gradient(90deg,#7C3AED,#3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}
            
.feature-subtext {
    color: #D1D5DB;
    font-size: 17px;
}
            
/* Architecture Container */
.architecture-container {
    margin-top: 80px;
    margin-bottom: 80px;
    padding: 60px;
    border-radius: 24px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Architecture Flow */
.arch-flow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
    flex-wrap: wrap;
}

.arch-box {
    background: rgba(255,255,255,0.04);
    padding: 20px 25px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    text-align: center;
    min-width: 150px;
    transition: 0.3s ease;
}

.arch-box:hover {
    transform: translateY(-6px);
    border: 1px solid rgba(124,58,237,0.6);
    box-shadow: 0 0 20px rgba(124,58,237,0.4);
}

.arch-arrow {
    font-size: 28px;
    margin: 10px;
    color: #9CA3AF;
}

.arch-subtext {
    margin-top: 40px;
    color: #D1D5DB;
    font-size: 16px;
    line-height: 1.6;
}
            
</style>
""", unsafe_allow_html=True)

def submit_login(user_name: str, password: str):
    logger.info(f"Submitting login for user {user_name}")

    login_request = LoginRequest(user_name=user_name, password=password)

    try:
        login_response = requests.post(
            url="http://localhost:10000/users/login",
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

# ==========================================
# NAVIGATION STATE
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ==========================================
# NAVBAR
# ==========================================
st.markdown('<div class="navbar">', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns([3,1,1,1,1,1])

with col1:
    st.markdown("### 🤖 Fin Assist AI")

with col2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("Home"):
        st.session_state.page = "Home"
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="features-btn">', unsafe_allow_html=True)
    if st.button("Features", key="features_btn"):
        st.session_state.page = "Features"
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="about-btn">', unsafe_allow_html=True)
    if st.button("About Us", key="about_btn"):
        st.session_state.page = "About"
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="contact-btn">', unsafe_allow_html=True)
    if st.button("Contact", key="contact_btn"):
        st.session_state.page = "Contact"
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="login-btn">', unsafe_allow_html=True)
    if st.button("Login", key="login_btn"):
        #st.switch_page("pages/01_Login.py")
        st.session_state.page = "Login"
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ==========================================
# PAGE CONTENT
# ==========================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class='glass-section' style='text-align:center;'>

    <h1 class='gradient-text' style='font-size:52px;'>
    Fin Assistant AI
    </h1>

    <h3 style='color:#D1D5DB; font-weight:400;'>
    Enterprise-Grade RAG Intelligence Chatbot with Built-In Role Governance
    </h3>

    <p style='max-width:900px; margin:auto; font-size:18px; color:#E5E7EB;'>
    FinSolve Technologies is redefining enterprise knowledge access through a 
    secure Retrieval-Augmented Generation (RAG) chatbot platform.  
    Our system combines contextual AI intelligence with strict role-based access control, 
    ensuring every user receives precise, authorized, and business-critical insights — instantly.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-section'>

    <h2>🚨 The Enterprise Challenge</h2>

    <p style='color:#D1D5DB; font-size:17px;'>
    Organizations generate vast volumes of sensitive data across finance, HR, marketing, 
    engineering, and executive leadership. Traditional chatbots lack contextual intelligence 
    and governance controls — creating risks of misinformation and data exposure.
    </p>

    <h2 style='margin-top:30px;'>💡 Our Solution</h2>

    <p style='color:#D1D5DB; font-size:17px;'>
    FinSolve integrates a RAG-based AI pipeline with dynamic role validation, ensuring:
    </p>

    <ul style='color:#E5E7EB; font-size:16px;'>
    <li>Context-rich, source-grounded responses</li>
    <li>Zero unauthorized data exposure</li>
    <li>Department-specific intelligence delivery</li>
    <li>Executive-level cross-functional insights</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🔐 Role-Based Intelligence Architecture")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='glass-card'>
        <h4>💰 Finance</h4>
        <p>Access to financial reports, expense breakdowns, reimbursements, and cost analytics.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:20px;'>
        <h4>📢 Marketing</h4>
        <p>Campaign performance metrics, customer insights, and revenue attribution data.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
        <h4>👩‍💼 Human Resources</h4>
        <p>Employee records, payroll data, attendance, and performance management insights.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:20px;'>
        <h4>⚙ Engineering</h4>
        <p>Technical architecture, development processes, operational documentation.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='glass-card'>
        <h4>🏢 C-Level Executives</h4>
        <p>Full enterprise visibility with cross-department intelligence synthesis.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:20px;'>
        <h4>👤 Employee</h4>
        <p>General policies, company events, and FAQ-level information access.</p>
        </div>
        """, unsafe_allow_html=True)

    st.text("")
    st.text("")

    st.markdown("""
    <div class='glass-section' style='text-align:center;'>

    <h2>Secure. Contextual. Enterprise-Ready.</h2>
    <p style='color:#D1D5DB;'>Experience the future of governed AI intelligence.</p>

    </div>
    """, unsafe_allow_html=True)

    if st.button("🔐 Access the Platform", type="primary"):
        st.session_state.page = "Login"


elif st.session_state.page == "Features":

    st.title("Platform Features")

    st.markdown("""
    <div class='glass-section section' style='text-align:center;'>

    <h1 class='gradient-text' style='font-size:48px;'>
    Enterprise Intelligence Engine
    </h1>

    <p style='color:#D1D5DB; font-size:17px;'>
    FinSolve Technologies combines Retrieval-Augmented Generation (RAG) 
    with dynamic role-based governance to deliver secure, context-rich enterprise intelligence.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-section section'>

    <h2>🧠 Retrieval-Augmented Intelligence</h2>

    <p style='color:#D1D5DB; font-size:17px;'>
    Our architecture retrieves verified enterprise knowledge before generating responses — 
    ensuring contextual accuracy, compliance, and reduced hallucination risk.
    </p>

    <p style='color:#D1D5DB; font-size:17px;'>
    <li>Secure vector-based document retrieval</li>
    <li>Context-enriched response generation</li>
    <li>Multi-department knowledge indexing</li>
    <li>Source-grounded outputs</li>
    <li>Optimized query processing pipeline</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='glass-section section'>

    <h2>🗄️ Natural Language to SQL Intelligence</h2>

    <p class='feature-subtext'>
    FinSolve enables business users to query structured enterprise databases 
    using natural language. The system translates human queries into optimized 
    SQL statements, retrieves validated data, and delivers contextual insights — 
    all within role-based access boundaries.
    </p>

    <ul class='feature-subtext'>
    <li>Natural language → SQL query translation</li>
    <li>Schema-aware query generation</li>
    <li>Role-based database access control</li>
    <li>Secure execution layer</li>
    <li>Contextual result explanation</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class='glass-section section'>

    <h2>🔐 Precision Role-Based Access Control</h2>

    <p style='color:#D1D5DB; font-size:17px;'>
    Every query undergoes real-time role validation before retrieval and response synthesis. 
    Data exposure is dynamically filtered based on user permissions.
    </p>

    <p style='color:#D1D5DB; font-size:17px;'>
    <li>Department-level data segmentation</li>
    <li>Executive cross-functional access</li>
    <li>Automatic response filtering</li>
    <li>Zero unauthorized data exposure architecture</li>
    <li>Audit-ready governance framework</li>
    </ul>

    </div>
""", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='glass-section section' style='text-align:center;'>

    <h2>🧠 AI Architecture Overview</h2>
    <p style='color:#D1D5DB; max-width:800px; margin:auto;'>
    Every user query flows through role validation, secure vector retrieval,
    and a Retrieval-Augmented Generation engine before delivering
    a compliant, context-rich response.
    </p>

    </div>
    """, unsafe_allow_html=True)

    col11, col22, col33 = st.columns([1, 6, 1])

    with col22:
        st.image(
            "./ui/images/RBAC Chatbot Architecture V1.png",
            width='content'
        )


    st.markdown("## 🏢 Department-Specific Intelligence Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='glass-card'>
        <h4>💰 Finance Intelligence</h4>
        <p>Financial reports, expense analytics, reimbursements, and cost visibility.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:25px;'>
        <h4>📢 Marketing Insights</h4>
        <p>Campaign performance, sales metrics, and customer behavior analytics.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
        <h4>👩‍💼 Human Resources</h4>
        <p>Payroll data, employee records, attendance tracking, performance reviews.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:25px;'>
        <h4>⚙ Engineering Knowledge</h4>
        <p>Technical documentation, architecture guidelines, operational playbooks.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='glass-card'>
        <h4>🏢 Executive Analytics</h4>
        <p>Cross-department intelligence synthesis for strategic decision-making.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card' style='margin-top:25px;'>
        <h4>👤 Employee Knowledge Hub</h4>
        <p>Policies, announcements, internal FAQs, and general company resources.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.text("")
    st.text("")

    st.markdown("""
    <div class='glass-section section'>

    <h2>⚙ Enterprise-Grade Infrastructure</h2>

    <p class='feature-subtext'>
    Built for scale, security, and compliance.
    </p>

    <ul class='feature-subtext'>
    <li>Encrypted document ingestion pipeline</li>
    <li>Secure API-driven backend architecture</li>
    <li>Role-isolated knowledge indexing</li>
    <li>Scalable vector database integration</li>
    <li>Compliance-ready audit logging</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)






elif st.session_state.page == "About":

    
    st.markdown("""
    <div class='glass-section section'>

    <h1 class='gradient-text'>About FinSolve Technologies</h1>

    <p style='color:#D1D5DB; font-size:17px;'>
    FinSolve Technologies is redefining enterprise intelligence through secure,
    context-aware AI systems powered by Retrieval-Augmented Generation (RAG)
    and dynamic role-based access control.
    </p>

    <h3 style='margin-top:30px;'>🎯 Our Mission</h3>
    <p style='color:#D1D5DB;'>
    To make enterprise knowledge instantly accessible — without compromising
    security, compliance, or governance.
    </p>

    <h3 style='margin-top:30px;'>🧠 What Makes Us Different</h3>
    <ul style='color:#D1D5DB;'>
    <li>Governance-first AI architecture</li>
    <li>Role-validated intelligent responses</li>
    <li>Secure knowledge retrieval pipelines</li>
    <li>Enterprise-ready infrastructure</li>
    </ul>

    <h3 style='margin-top:30px;'>🌍 Our Vision</h3>
    <p style='color:#D1D5DB;'>
    We are building the infrastructure layer for governed AI adoption
    across modern enterprises.
    </p>

    </div>
    """, unsafe_allow_html=True)


elif st.session_state.page == "Contact":

    st.title("Contact Us")
    st.text_input("Name")
    st.text_input("Email")
    st.text_area("Message")
    st.button("Send Message")

elif st.session_state.page == "Login":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)

        st.markdown("## 🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In", type="primary"):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:  
                submit_login(username, password)

                if st.session_state.get("logged_in"):
                    st.success(st.session_state.get("login_success_msg", "Login successful"))
                    st.switch_page("pages/02_Home.py")
                else:
                    st.error(st.session_state.get("login_success_msg", "Login failed"))

        st.markdown('</div>', unsafe_allow_html=True)