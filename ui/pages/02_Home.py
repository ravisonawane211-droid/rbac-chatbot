import streamlit as st
import requests
import pandas as pd
from app.schemas.query_request import QueryRequest
from app.schemas.create_user_request import CreateUserRequest
from app.schemas.save_config_request import SaveConfigRequest
from app.schemas.user import User
from app.schemas.app_config import AppConfig
from app.utils.logger import get_logger
from app.config.config import get_settings


logger = get_logger(__name__)
settings = get_settings()

# Page configuration
st.set_page_config(page_title="FinSolve Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.write("")  # spacer
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="chatbot-title">Welcome To FinSolve Technologies</div>', unsafe_allow_html=True)

# --- Styles for a professional, ChatGPT-like chat UI ---
st.markdown(
    """
    <style>
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

    .chatbot-title {
      text-align: center;
      font-size: 1.6rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }

    .chat-card {
        max-width: 980px;
        margin: 2.25rem auto;
        background: var(--card);
        border-radius: 14px;
        padding: 0;
        box-shadow: var(--shadow);
        overflow: hidden;
        border: 1px solid rgba(15,23,42,0.04);
    }

    .chat-header {
        padding: 1rem 1.25rem;
        background: transparent;
        border-bottom: 1px solid rgba(15,23,42,0.04);
    }
    .chat-header h2 { margin: 0; font-size: 1.125rem; font-weight:700; color: #0f172a; }
    .chat-header p { margin: 0; color: var(--muted); font-size: 0.875rem; }

    .chat-body { display:flex; gap:1.25rem; padding: 1rem; }
    /* Use a transparent messages background so it blends with the card and does not create a large white box */
    .messages { flex: 1; min-height: 30vh; max-height: 56vh; border-radius: 10px; padding: 0.75rem; background: transparent; overflow:auto }
    .controls { width: 320px; max-width: 40%; }

    .msg { margin-bottom: 0.9rem; display:flex; gap:0.75rem; align-items: flex-end; max-width: 82%; }
    .msg .msg-content { padding: 0.7rem 0.95rem; border-radius: 10px; font-size: 0.95rem; line-height:1.35; box-shadow: 0 4px 10px rgba(2,6,23,0.03); }

    .msg.assistant { align-self:flex-start; }
    .msg.assistant .avatar { background: #eef2ff; color: #4f46e5; }
    .msg.assistant .msg-content { background: #ffffff; color: #0f172a; border: 1px solid rgba(15,23,42,0.03); border-bottom-left-radius:6px; }

    .msg.user { margin-left: auto; align-self:flex-end; flex-direction: row-reverse; }
    .msg.user .avatar { background: var(--user-gradient); color: white; }
    .msg.user .msg-content { background: var(--user-gradient); color: white; border-bottom-right-radius:6px; }

    .avatar { width:34px; height:34px; min-width:34px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:600; font-size:0.9rem; }

    .msg-meta { display:block; font-size:0.75rem; color:var(--muted); margin-top:4px; }

    /* Input area styling */
    .chat-input { padding: 0.65rem; border-radius: 10px; border: 1px solid rgba(15,23,42,0.06); background: #fff; }
    .send-row { display:flex; gap:0.6rem; align-items:center; }
    .send-row .send-btn { background: var(--accent) !important; color: white !important; border-radius: 8px !important; padding: 0.55rem 0.9rem !important; font-weight:600 !important; }

    /* Accessibility tweaks */
    .msg .msg-content code, .msg .msg-content pre { background: rgba(15,23,42,0.04); padding: 0.2rem 0.4rem; border-radius:6px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', monospace; }

    /* Responsive */
    @media (max-width: 900px) {
        .chat-body { flex-direction: column; }
        .controls { width: 100%; }
        .chat-card { margin: 1rem; }
    }

    /* Clean UI */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

API_BASE = "http://localhost:8000"

# Authentication guard
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You need to log in first.")
    st.switch_page("01_Login.py")

# Helper functions
def call_query_api(question: str):
    """Call the backend query endpoint and return the answer."""

    logger.info("Calling query API with question: %s", question)

    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        #headers["Authorization"] = token

    queryRequest = QueryRequest(question=question,include_sources=False,enable_evaluation=True,
    user_name=logged_in_user,conversation_id=st.session_state.get("conversation_id"))

    try:
        query_response = requests.post(f"{API_BASE}/query", json=queryRequest.model_dump(), headers=headers)
        query_response.raise_for_status()
        response = query_response.json()
        answer = response.get("answer", "").replace("\n", "  \n")  # Preserve line breaks for markdown
        return answer
    except Exception as e:
        logger.error("Error calling query API: %s", e)
        return f"Error calling query API: {e}"


def upload_document_api(file, role: str):
    logger.info("Uploading document: %s with role: %s", file.name, role)
    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    files = {"file": (file.name, file, file.type)}
    data = {"role": role}
    try:
        resp = requests.post(f"{API_BASE}/documents/upload", files=files, params=data, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error("Error uploading document: %s", e)
        return {"error": str(e)}


def create_user_api(username: str, password: str, role: str):
    logger.info("saving user")
    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    create_user_request = CreateUserRequest(user=User(user_id=username,password=password, user_role=[role]),created_by=logged_in_user)
    
    try:
        # Backend endpoint for user creation may not exist; try /users/create then /users
        try:
            resp = requests.post(f"{API_BASE}/users", json=create_user_request.model_dump(), headers=headers, timeout=15)
        except requests.exceptions.RequestException:
            logger.error(f"error while saving user {username}")
            resp = requests.post(f"{API_BASE}/users", json=create_user_request.model_dump(), headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"error while saving user {username}")
        return {"error": str(e)}

# Get Dashboard metrics
def get_evaluation_metrics_dashboard(app_name:str):
    logger.info("retriving metrics")
    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(f"{API_BASE}/dashboard/metrics/{app_name}", headers=headers, timeout=30)
        resp.raise_for_status()
        if resp.status_code != 200:
            logger.error("Error fetching evaluation metrics")
            raise Exception(f"Failed to fetch metrics: {resp.status_code} {resp.text}")
        return resp.json()
    except Exception as e:
        logger.error("Error fetching evaluation metrics: %s", e)
        return {"error": str(e)}
    

def create_app_config_api(enable_eval:str, eval_type: str):
    logger.info("Saving app config")
    headers = {}
    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    save_app_config_request = SaveConfigRequest(app_config=AppConfig(enable_eval=enable_eval,eval_type=eval_type))

    try:
        try:
            resp = requests.post(f"{API_BASE}/dashboard/config", json=save_app_config_request.model_dump(), 
                                 headers=headers, timeout=60)
        except requests.exceptions.RequestException:
            logger.error("error while saving app coniguration")
            resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error while saving app configuration": str(e)}
    
STATUS_COLOR_MAP = {
    "green": "#c8f0d1",
    "red": "#f8d7da",
}

def style_scores_by_status(row):
    styles = []
    for col, val in row.items():
        if col.endswith("_Score"):
            status_col = col.replace("_Score", "_Status")
            status_value = row.get(status_col)
            color = STATUS_COLOR_MAP.get(status_value, "")
            styles.append(f"background-color: {color}" if color else "")
        else:
            styles.append("")
    return styles


# Top-level tabs

user = st.session_state.get("user", {"user_id": "Guest","user_role": "general"})
logged_in_user:str = user["user_id"] if user["user_id"] else "Guest"
role:str = user["user_role"][0].lower() if user["user_role"] else "general"

with col3:
    st.markdown(f"**👤 User:** `{logged_in_user}`  \n**🛡️ Role:** `{role}`")
            # --- Logout ---
    if st.button("🚪 Logout"):
                st.session_state["user"] = None
                st.switch_page("01_Login.py")
                st.rerun()
    
        # Role-specific section
        # Dynamic rendering
st.markdown("")
if role == "c-level":
            st.write("You have global access")
            tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", " 📤 Upload", " 🛠️ Admin", "📊 Dashboard"])
        
elif role == "general":
            st.write(f"You have access to documents and features related to the `{role}` role.")
            (tab1,) =  st.tabs(["💬 Chat"])

else:
            st.write(f"You have access to documents and features related to the `{role}` role.")
            st.markdown("You also have access to **General documents** (e.g., company policies, holidays, announcements)")
            (tab1,) = st.tabs(["💬 Chat"])

# --- Chatbot tab ---
with tab1:
    # Ensure messages exist
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"Hi, {user['user_id']}. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        answer = call_query_api(question=prompt)

        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


# --- Upload tab ---
if role == "c-level":
    with tab2:
        st.header("Upload Documents")
        st.info("Upload PDF, TXT, Markdown or CSV files to be processed and added to the vector store.")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "csv", "md"])    
        role = st.selectbox("Document role", options=["general", "engineering", "marketing", "finance", "hr"], index=0)
        if st.button("Upload", key="upload_btn"):
            if not uploaded_file:
                st.error("Please select a file to upload.")
            else:
                with st.spinner("Uploading and processing..."):
                    result = upload_document_api(uploaded_file, role)
                    if result.get("error"):
                        st.error(f"Upload failed: {result['error']}")
                    else:
                        st.success(result.get("message", "Upload succeeded"))
                        st.write(result)

    # --- Admin tab ---
    with tab3:
        st.header("Admin — Create User")

        add_user, app_config = st.tabs(["Add User", " App Config"])

        with add_user:
            st.info("Create a new user for the application.")
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", options=["general", "engineering", "marketing", "finance", "hr","admin","c-level"], index=0)
            if st.button("Create user",type="primary",key="create_user"):
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                else:
                    resp = create_user_api(new_username, new_password, new_role)
                    if resp.get("error"):
                        st.error(f"User creation failed: {resp['error']}")
                    else:
                        st.success("User created successfully")
                        st.write(resp)
            # --- App Config tab ---
        with app_config:
            st.header("Add Application Configuration")
            st.info("Configure application settings here.")
            enable_evaluation = st.radio(label="Enable Evaluation",options=["Yes","No"])
            evaluation_type = st.selectbox(label="Evaluation Type",options=["Ragas","LLM-As-Judge"])
            if st.button("Add Config",type="primary",key="add_config"):
                if not enable_evaluation or not evaluation_type:
                    st.error("Enable Evaluation and Evaluation Type are required.")
                else:
                    logger.info(f"enable_evaluation: {enable_evaluation} , evaluation_type: {evaluation_type}")
                    resp = create_app_config_api(enable_eval=enable_evaluation,eval_type=evaluation_type)
                    if resp.get("messagge") != "success":
                        st.error(f"App config save failed: {resp['error']}")
                    else:
                        st.success("App Config saved successfully")


    # --- Dashboard tab ---
    with tab4:
        st.header("Dashboard")
        
        with st.spinner("Fetching Metrics..."):
            response = get_evaluation_metrics_dashboard(settings.app_name)
            metrics = response.get("metrics", [])
            threshold = response.get("threshold", {})
            if response.get("status") == "success" and len(metrics) > 0:
                rows = []
                for metric in metrics:
                    score = float(metric["metric_value"])
                    #symbol = "🟢" if metric["eval_status"] == "Green" else "🔴"
                    rows.append({
                                "Question": metric.get("question", ""),
                                "Answer": metric.get("answer", ""),
                                "Metric Name": metric.get("metric_name", ""),
                                "Score": score,
                                "Status": metric.get("eval_status","red"),
                            })
                display_df = pd.DataFrame(rows)

                score_df = display_df.pivot(
                    index=["Question", "Answer"],
                    columns="Metric Name",
                    values="Score"
                )

                status_df = display_df.pivot(
                    index=["Question", "Answer"],
                    columns="Metric Name",
                    values="Status"
                )

                score_df.columns = [f"{c}_Score" for c in score_df.columns]
                status_df.columns = [f"{c}_Status" for c in status_df.columns]

                final_df = pd.concat([score_df, status_df], axis=1).reset_index()


                st.markdown("#### Evaluation Metric Details")
                st.caption("Thresholds: " + ", ".join([f"{k}: {v}" for k, v in threshold.items()]))
                st.caption("🟢 Green: Within threshold | 🔴 Red: Outside threshold")

                styled_df = final_df.style.apply(style_scores_by_status, axis=1)

                column_config = {}

                # Hide _Status columns
                for col in final_df.columns:
                    if col.endswith("_Status"):
                        column_config[col] = None

                # Rename _Score columns and add threshold tooltip
                for col in final_df.columns:
                    if col.endswith("_Score"):
                        column_config[col] = st.column_config.NumberColumn(
                            label=col.replace("_Score", "")
                        )

                st.dataframe(
                    styled_df,
                    width='stretch',
                    hide_index=True,
                    column_config=column_config
                )
            else:
                 st.error("Unable to get metrics from evaluation services.Please contact administrator.")
