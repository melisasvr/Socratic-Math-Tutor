import streamlit as st
import os
import re
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ─── Config — Groq ────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Free models on Groq (fast & reliable — no rate limit surprises)
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile").strip(chr(34)).strip(chr(39))

WELCOME_MESSAGE = """I'm ready to be your Socratic Math Tutor! I'll guide you with hints and questions rather than just giving answers — because that's how real understanding sticks. 😊

What problem are you working on today?
Just type it out (or paste it), and we'll work through it together step by step!"""

# ─── System prompts ───────────────────────────────────────────────────────────
SYSTEM_GUIDE = """You are a patient Socratic Math Tutor.

STRICT RULES:
- Ask ONLY ONE small guiding question at a time. Never ask two questions.
- NEVER give the full solution or final answer.
- After the student answers correctly: praise them briefly, then ask the NEXT small step.
- After the student answers wrongly: gently hint and ask again.
- Be warm and encouraging always.
- Keep responses short and focused.

End every response with exactly one bold question like:
**What is your next step?**"""

SYSTEM_REVIEW = """You are a math tutor reviewing a student's submitted solution.
Look at their work carefully. Praise what's correct. Gently point out any errors.
If fully correct, congratulate them enthusiastically and confirm the final answer.
If there are mistakes, ask them to fix one specific thing.
Keep your response clear and encouraging."""

# ─── LLM setup — Groq uses OpenAI-compatible API ─────────────────────────────
def get_llm():
    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=GROQ_API_KEY,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0.3,
        max_tokens=600,
    )

def call_llm(system: str, history: list) -> str:
    try:
        llm = get_llm()
        messages = [SystemMessage(content=system)]
        for m in history[-10:]:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))
        return llm.invoke(messages).content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ─── Image encoding ───────────────────────────────────────────────────────────
def encode_image(uploaded_file):
    bytes_data = uploaded_file.read()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    ext = uploaded_file.name.split(".")[-1].lower()
    media_type = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                  "png": "image/png", "webp": "image/webp"}.get(ext, "image/png")
    return b64, media_type

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Socratic Math Tutor", page_icon="∑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
:root { --bg: #0D0D1A; --card: #1A1A35; --purple: #6C63FF; --pink: #FF6584; --text: #E8E6FF; --muted: #9B99CC; }
.stApp { background-color: var(--bg) !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stChatMessage"] { background: var(--card) !important; border-radius: 14px !important; border: 1px solid rgba(108,99,255,0.15) !important; margin-bottom: 8px !important; }
.yes-btn button { background: rgba(16,185,129,0.12) !important; border: 2px solid rgba(16,185,129,0.6) !important; color: #6EE7B7 !important; font-size: 15px !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px !important; }
.no-btn button  { background: rgba(255,101,132,0.12) !important; border: 2px solid rgba(255,101,132,0.6) !important; color: #FF6584  !important; font-size: 15px !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px !important; }
.step-box { padding: 14px 18px; background: rgba(67,232,216,0.06); border: 1px solid rgba(67,232,216,0.3); border-radius: 12px; margin: 10px 0 14px; }
.step-label { font-size: 11px; font-family: 'Space Mono', monospace; color: #43E8D8; font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }
.step-q { font-size: 15px; color: var(--text); }
.submit-box { padding: 16px 18px; background: rgba(108,99,255,0.07); border: 1px solid rgba(108,99,255,0.25); border-radius: 12px; margin: 10px 0; }
[data-testid="stSidebar"] { background: #13132B !important; border-right: 1px solid rgba(108,99,255,0.2) !important; }
.stButton > button { width: 100% !important; background: var(--card) !important; border: 1px solid rgba(108,99,255,0.25) !important; color: var(--text) !important; border-radius: 10px !important; padding: 10px 14px !important; margin-bottom: 6px !important; text-align: left !important; transition: all .2s !important; }
.stButton > button:hover { border-color: rgba(108,99,255,0.6) !important; transform: translateX(2px) !important; }
[data-testid="stChatInput"] > div { background: var(--card) !important; border: 1px solid rgba(108,99,255,0.3) !important; border-radius: 14px !important; }
[data-testid="stChatInput"] textarea { color: var(--text) !important; background: transparent !important; }
.stFileUploader > div { background: var(--card) !important; border: 1px dashed rgba(108,99,255,0.35) !important; border-radius: 12px !important; }
.stSpinner > div { border-top-color: var(--purple) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
if "step_state" not in st.session_state:
    # States: initial | waiting_yes_no | guiding | waiting_solution | done
    st.session_state.step_state = "initial"
if "current_step_q" not in st.session_state:
    st.session_state.current_step_q = None

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:16px 0 10px">
        <div style="font-size:36px">∑</div>
        <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;
             background:linear-gradient(135deg,#A78BFA,#EC4899);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent">
             Socratic Math Tutor</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    if GROQ_API_KEY:
        st.success("✓ Groq API connected")
    else:
        st.error("⚠️ No GROQ_API_KEY in .env")

    phase_labels = {
        "initial": "⏳ Waiting for problem",
        "waiting_yes_no": "🤔 Awaiting your answer",
        "guiding": "🧭 Step-by-step mode",
        "waiting_solution": "📝 Awaiting your solution",
        "done": "✅ Problem solved!",
    }
    st.markdown(f"**Status:** {phase_labels.get(st.session_state.step_state, '')}")
    st.markdown("---")

    if st.button("💡 Give me a hint"):
        if st.session_state.step_state == "guiding":
            with st.spinner("Thinking..."):
                hint_msgs = st.session_state.messages + [{"role": "user", "content": "Can you give me a small hint without giving the answer?"}]
                reply = call_llm(SYSTEM_GUIDE, hint_msgs)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    if st.button("📖 Show full solution"):
        if st.session_state.step_state not in ("initial", "done"):
            with st.spinner("Working it out..."):
                full_msgs = st.session_state.messages + [{"role": "user", "content": f"I'm stuck. Please show me the complete step-by-step solution to: {st.session_state.current_problem}"}]
                reply = call_llm(SYSTEM_GUIDE, full_msgs)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.step_state = "done"
                st.session_state.current_step_q = None
            st.rerun()

    if st.button("🆕 New problem"):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
        st.session_state.current_problem = None
        st.session_state.step_state = "initial"
        st.session_state.current_step_q = None
        st.rerun()

    st.markdown("---")
    st.markdown("""<div style="font-size:12px;color:#5A5880;line-height:1.8">
    <strong style="color:#9B99CC">How it works</strong><br>
    1️⃣ Type or 📷 upload a problem<br>
    2️⃣ Say yes or no to confidence<br>
    3️⃣ Answer one step at a time<br>
    4️⃣ AI checks every answer<br>
    5️⃣ Upload photos of your work!
    </div>""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""<div style="display:flex;align-items:center;gap:14px;padding:20px 0 16px;
    border-bottom:1px solid rgba(108,99,255,0.2);margin-bottom:18px">
    <div style="width:48px;height:48px;background:linear-gradient(135deg,#6C63FF,#FF6584);
        border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:24px">∑</div>
    <div>
        <div style="font-family:'Space Mono',monospace;font-size:19px;font-weight:700;
            background:linear-gradient(135deg,#A78BFA,#EC4899);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent">Socratic Math Tutor</div>
        <div style="font-size:13px;color:#5A5880;font-style:italic">Think it through — I'll guide you there</div>
    </div>
</div>""", unsafe_allow_html=True)

# ─── Render chat history ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Current step reminder ────────────────────────────────────────────────────
if st.session_state.step_state == "guiding" and st.session_state.current_step_q:
    st.markdown(f"""<div class="step-box">
        <div class="step-label">✏️ YOUR TURN</div>
        <div class="step-q">{st.session_state.current_step_q}</div>
    </div>""", unsafe_allow_html=True)

# ─── Yes/No buttons ───────────────────────────────────────────────────────────
if st.session_state.step_state == "waiting_yes_no":
    col1, col2, _ = st.columns([2, 2, 3])
    with col1:
        st.markdown('<div class="yes-btn">', unsafe_allow_html=True)
        if st.button("✅  Yes, I know how!", use_container_width=True):
            st.session_state.step_state = "waiting_solution"
            reply = "Awesome! 💪 Show me your solution — type it below or upload a photo of your written work, then hit **Submit**."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="no-btn">', unsafe_allow_html=True)
        if st.button("❓  No, help me!", use_container_width=True):
            st.session_state.step_state = "guiding"
            with st.spinner("Let's start from the beginning..."):
                start_msgs = [{"role": "user", "content": f"The student's problem is: {st.session_state.current_problem}\n\nThey said they don't know how to solve it. Ask them the very first small question to get started. Do NOT solve it."}]
                reply = call_llm(SYSTEM_GUIDE, start_msgs)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                # Extract the bold question as current step
                q_match = re.search(r'\*\*(.+?)\*\*', reply)
                st.session_state.current_step_q = q_match.group(1) if q_match else None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Solution submission ──────────────────────────────────────────────────────
elif st.session_state.step_state == "waiting_solution":
    st.markdown('<div class="submit-box">', unsafe_allow_html=True)
    st.markdown("**📝 Submit your solution:**")
    col1, col2 = st.columns([3, 1])
    with col1:
        solution_text = st.text_area("Type your solution here", key="sol_text", height=120,
                                      placeholder="e.g. I factored it as (x-2)(x-3)=0, so x=2 or x=3")
    with col2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        sol_image = st.file_uploader("📷 Or upload photo", type=["png","jpg","jpeg","webp"], key="sol_img")

    if st.button("✅ Submit My Solution", use_container_width=True):
        if solution_text or sol_image:
            with st.spinner("Reviewing your solution..."):
                display = solution_text or "📷 Solution photo submitted"
                if sol_image:
                    display = ("📷 " + solution_text) if solution_text else "📷 Solution photo submitted"
                st.session_state.messages.append({"role": "user", "content": display})

                review_msgs = st.session_state.messages + [
                    {"role": "user", "content": f"Please review my solution above. The original problem was: {st.session_state.current_problem}"}
                ]
                reply = call_llm(SYSTEM_REVIEW, review_msgs)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.step_state = "done"
            st.rerun()
        else:
            st.warning("Please type your solution or upload a photo first.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Done ─────────────────────────────────────────────────────────────────────
elif st.session_state.step_state == "done":
    st.success("🎉 Great work! Use **🆕 New problem** in the sidebar for another one.")

# ─── Main input (initial problem entry + guided answers) ─────────────────────
if st.session_state.step_state in ("initial", "guiding"):
    upload_label = "📷 Upload a photo of your problem" if st.session_state.step_state == "initial" else "📷 Upload your work (optional)"
    upload_key = "prob_img" if st.session_state.step_state == "initial" else "work_img"

    uploaded_file = st.file_uploader(upload_label, type=["png","jpg","jpeg","webp"], key=upload_key)
    user_input = st.chat_input(
        "Type your problem here…" if st.session_state.step_state == "initial" else "Type your answer here…"
    )

    if user_input or uploaded_file:
        display = user_input or ""
        if uploaded_file:
            display = ("📷 " + user_input) if user_input else "📷 Image submitted"
        st.session_state.messages.append({"role": "user", "content": display})

        # ── New problem ──
        if st.session_state.step_state == "initial":
            st.session_state.current_problem = user_input or "the problem in the uploaded image"
            st.session_state.step_state = "waiting_yes_no"
            reply = f"Got it! The problem is:\n\n**{st.session_state.current_problem}**\n\nDo you already know how to solve this?"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        # ── Guided step answer ──
        elif st.session_state.step_state == "guiding":
            with st.spinner("Checking your answer..."):
                reply = call_llm(SYSTEM_GUIDE, st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                q_match = re.search(r'\*\*(.+?\?)\*\*', reply)
                st.session_state.current_step_q = q_match.group(1) if q_match else None
                if not st.session_state.current_step_q:
                    # No more questions = problem solved
                    st.session_state.step_state = "done"
            st.rerun()

st.caption("Socratic Math Tutor — Powered by Groq · Patient guidance, not instant answers")