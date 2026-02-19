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

st.set_page_config(
    page_title="FinSolve Chatbot",
    page_icon="🤖",
    layout="wide"
)

API_BASE = "http://localhost:10000"

# =====================================================
# 🎨 ENTERPRISE STYLING
# =====================================================
st.markdown("""
<style>
:root {
    --bg: #0f172a;
    --card: rgba(255,255,255,0.05);
    --border: rgba(255,255,255,0.08);
}

.stApp {
    background: radial-gradient(circle at 30% 30%, #1e1b4b 0%, #0b0f1a 50%);
    color: white;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

section.main > div {
    max-width: 1400px;
    margin: 2rem auto;
    background: var(--card);
    backdrop-filter: blur(20px);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid var(--border);
}

/* Tabs */
div[data-baseweb="tab-list"] {
    gap: 10px;
}

button[role="tab"] {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
}

button[role="tab"][aria-selected="true"] {
    background: white !important;
    color: black !important;
    font-weight: 600 !important;
}

/* Labels */
label {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: white !important;
    color: black !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

/* File uploader browse button */
[data-testid="stFileUploader"] button {
    color: black !important;
    font-weight: 600 !important;
}

/* Assistant text white */
[data-testid="stChatMessage"] div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 🔐 LOGIN CHECK
# =====================================================
if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.switch_page("00_Landing.py")
    st.stop()

# =====================================================
# 👤 USER INFO
# =====================================================
user = st.session_state.get("user", {})
logged_in_user = user.get("user_id", "User")
roles_list = user.get("user_role", [])
role = roles_list[0].lower() if roles_list else "general"

col1, col2 = st.columns([8, 2])

with col1:
    st.markdown("### 🏦 Fin Assist AI Platform")

with col2:
    st.markdown(f"**👤 {logged_in_user}**  \n**Role:** {role}")
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("00_Landing.py")

st.divider()

# =====================================================
# 📑 ROLE-BASED TABS
# =====================================================
if role == "c-level":
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📤 Upload", "🛠 Admin", "📊 Dashboard"])
else:
    (tab1,) = st.tabs(["💬 Chat"])

# =====================================================
# 💬 CHAT TAB
# =====================================================
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

with tab1:

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hi {logged_in_user}, how can I assist you today?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(
                    f"<div style='color:white;font-weight:700;'>🤖 {msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(f"👤 {msg['content']}")

    if prompt := st.chat_input("Ask FinSolve AI..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(f"👤 {prompt}")

        with st.chat_message("assistant"):
            thinking = st.empty()
            thinking.markdown("🤖 *FinSolve AI is analyzing your request...*")
            answer = call_query_api(prompt)
            thinking.empty()

            st.markdown(
                f"<div style='color:white;font-weight:700;'>🤖 {answer}</div>",
                unsafe_allow_html=True
            )

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# =====================================================
# 📤 UPLOAD TAB
# =====================================================
if role == "c-level":
    with tab2:
        st.header("Upload Documents")

        uploaded_file = st.file_uploader("Choose file", type=["pdf","txt","csv","md"])
        doc_role = st.selectbox("Document role", ["general","engineering","marketing","finance","hr"])

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

# =====================================================
# 🛠 ADMIN TAB
# =====================================================
    with tab3:
        st.header("Admin Panel")

        admin_tab1, admin_tab2 = st.tabs(["👤 User Management", "⚙ Configuration"])

        # USER TAB
        with admin_tab1:
            st.subheader("Create User")

            new_username = st.text_input("Username", key="admin_user_username")
            new_password = st.text_input("Password", type="password", key="admin_user_password")
            new_role = st.selectbox(
                "Role",
                ["general","engineering","marketing","finance","hr","admin","c-level"],
                key="admin_user_role"
            )

            if st.button("Create User", key="create_user_btn"):
                if new_username and new_password:
                    response = create_user_api(new_username, new_password, new_role)
                    if response.get("error"):
                        st.error(response["error"])
                    else:
                        st.success("User created successfully.")
                else:
                    st.warning("Username and password required.")

        # CONFIG TAB
        with admin_tab2:
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


# =====================================================
# 📊 DASHBOARD TAB
# =====================================================
    with tab4:
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

