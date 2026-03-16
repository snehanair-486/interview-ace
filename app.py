import streamlit as st
import boto3
import json

# --- Page Config ---
st.set_page_config(page_title="InterviewAce", page_icon="🎤", layout="centered")
st.title("🎤 InterviewAce")
st.caption("AI-powered mock interviews for students & fresh grads — powered by Amazon Nova")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Your Details")
    job_role = st.text_input("Job Role", placeholder="e.g. Software Engineer Intern")
    resume_text = st.text_area("Paste your Resume (text)", height=200,
                               placeholder="Copy-paste your resume content here...")
    difficulty = st.selectbox("Interview Difficulty", ["Easy", "Medium", "Hard"])
    start_btn = st.button("🚀 Start Interview")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# --- System Prompt ---
def get_system_prompt(role, resume, diff):
    return f"""You are a professional interviewer conducting a mock job interview.
The candidate is a student or fresh graduate applying for: {role}
Their resume summary: {resume[:500]}
Difficulty level: {diff}

STRICT RULES — follow exactly:
- Ask ONLY ONE question per response. Stop after the question mark. Do NOT write anything else.
- NEVER write placeholder text like "[After candidate's answer]" or "[After your response]"
- NEVER simulate or predict the candidate's answers
- NEVER write the full interview script upfront
- Wait for the candidate to actually reply before continuing
- After the candidate answers, give 1-2 sentences of feedback, then ask the next question
- Ask exactly 5 questions total: intro, technical, behavioral, situational, closing
- Start by greeting briefly and asking question 1 only"""
# --- Bedrock Client ---
client = boto3.client("bedrock-runtime", region_name="us-east-1")

def ask_nova(messages, system_prompt):
    # Format messages so content is always an array
    formatted = []
    for m in messages:
        content = m["content"]
        if isinstance(content, str):
            content = [{"text": content}]
        formatted.append({"role": m["role"], "content": content})

    body = {
        "system": [{"text": system_prompt}],
        "messages": formatted,
        "inferenceConfig": {"maxTokens": 500, "temperature": 0.7}
    }
    response = client.invoke_model(
        modelId="amazon.nova-lite-v1:0",
        body=json.dumps(body),
        contentType="application/json"
    )
    result = json.loads(response["body"].read())
    return result["output"]["message"]["content"][0]["text"]
# --- Start Interview ---
if start_btn and job_role and resume_text:
    st.session_state.interview_started = True
    st.session_state.messages = []
    st.session_state.system_prompt = get_system_prompt(job_role, resume_text, difficulty)
    # Get opening message from Nova
    opening = ask_nova([{"role": "user", "content": "Please begin the interview."}], st.session_state.system_prompt)

# --- Display Chat ---
if st.session_state.interview_started:
    st.divider()
    st.subheader(f"🧑‍💼 Mock Interview: {job_role}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Candidate reply
    user_input = st.chat_input("Type your answer here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Nova responds
        with st.spinner("Interviewer is thinking..."):
            reply = ask_nova(st.session_state.messages, st.session_state.system_prompt)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

elif not st.session_state.interview_started:
    st.info("👈 Fill in your details in the sidebar and click **Start Interview** to begin!")
    st.markdown("""
    ### How it works:
    1. **Enter** your target job role and paste your resume
    2. **Choose** difficulty level
    3. **Click** Start Interview — Nova will conduct a personalized mock interview
    4. **Answer** each question naturally
    5. **Get** instant feedback after each answer
    """)