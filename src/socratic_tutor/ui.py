import streamlit as st

from .config import (
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    GROQ_API_KEY,
    PROGRESS_DB_PATH,
    WELCOME_MESSAGE,
)
from .helpers import extract_bold_question, is_solution_likely_correct
from .i18n import LANGUAGES, t
from .llm import call_llm
from .progress import get_progress_stats, init_progress_db, record_attempt
from .prompts import get_system_guide, get_system_review
from .themes import THEMES, build_styles
from .topics import TOPIC_LABELS, detect_topic, topic_instruction


def _init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
    if "step_state" not in st.session_state:
        st.session_state.step_state = "initial"
    if "current_step_q" not in st.session_state:
        st.session_state.current_step_q = None
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    if "theme" not in st.session_state:
        st.session_state.theme = DEFAULT_THEME
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = "general"
    if "interaction_count" not in st.session_state:
        st.session_state.interaction_count = 0
    if "attempt_logged" not in st.session_state:
        st.session_state.attempt_logged = True


def _reset_for_new_problem() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    st.session_state.current_problem = None
    st.session_state.step_state = "initial"
    st.session_state.current_step_q = None
    st.session_state.current_topic = "general"
    st.session_state.interaction_count = 0
    st.session_state.attempt_logged = True


def _finalize_attempt(solved: bool) -> None:
    if not st.session_state.current_problem or st.session_state.attempt_logged:
        return
    record_attempt(
        PROGRESS_DB_PATH,
        st.session_state.current_topic,
        solved,
        st.session_state.interaction_count,
    )
    st.session_state.attempt_logged = True


def _render_sidebar() -> None:
    lang = st.session_state.language
    stats = get_progress_stats(PROGRESS_DB_PATH)

    with st.sidebar:
        selected_language_name = st.selectbox(
            t(lang, "language"),
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.values()).index(lang) if lang in LANGUAGES.values() else 0,
        )
        selected_language = LANGUAGES[selected_language_name]
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

        selected_theme = st.selectbox(
            t(st.session_state.language, "theme"),
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.theme) if st.session_state.theme in THEMES else 0,
        )
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()

        st.markdown(
            """<div style="text-align:center;padding:16px 0 10px">
        <div style="font-size:36px">S</div>
        <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;
             background:linear-gradient(135deg,#A78BFA,#EC4899);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent">
             Socratic Math Tutor</div>
    </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        if GROQ_API_KEY:
            st.success(t(st.session_state.language, "api_ok"))
        else:
            st.error(t(st.session_state.language, "api_missing"))

        phase_labels = {
            "initial": t(st.session_state.language, "waiting_problem"),
            "waiting_yes_no": t(st.session_state.language, "awaiting_answer"),
            "guiding": t(st.session_state.language, "guiding"),
            "waiting_solution": t(st.session_state.language, "awaiting_solution"),
            "done": t(st.session_state.language, "done"),
        }
        st.markdown(f"**{t(st.session_state.language, 'status')}:** {phase_labels.get(st.session_state.step_state, '')}")
        st.markdown(
            f"**{t(st.session_state.language, 'topic')}:** {TOPIC_LABELS.get(st.session_state.current_topic, 'General Math')}"
        )
        st.markdown("---")

        st.markdown(f"**{t(st.session_state.language, 'progress')}**")
        col1, col2 = st.columns(2)
        col1.metric(t(st.session_state.language, "total_solved"), stats["total_solved"])
        col2.metric(t(st.session_state.language, "total_attempts"), stats["total_attempts"])
        st.caption(
            f"{t(st.session_state.language, 'current_streak')}: {stats['current_streak']} | "
            f"{t(st.session_state.language, 'last_7_days')}: {stats['last_7_days']}"
        )

        if st.button(t(st.session_state.language, "hint")):
            if st.session_state.step_state == "guiding":
                with st.spinner(t(st.session_state.language, "thinking")):
                    hint_msgs = st.session_state.messages + [
                        {
                            "role": "user",
                            "content": "Can you give me a small hint without giving the answer?",
                        }
                    ]
                    guide_system = get_system_guide(
                        st.session_state.language,
                        topic_instruction(st.session_state.current_topic),
                    )
                    reply = call_llm(guide_system, hint_msgs)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

        if st.button(t(st.session_state.language, "show_solution")):
            if st.session_state.step_state not in ("initial", "done"):
                with st.spinner(t(st.session_state.language, "working")):
                    full_msgs = st.session_state.messages + [
                        {
                            "role": "user",
                            "content": (
                                "I'm stuck. Please show me the complete step-by-step solution to: "
                                f"{st.session_state.current_problem}"
                            ),
                        }
                    ]
                    guide_system = get_system_guide(
                        st.session_state.language,
                        topic_instruction(st.session_state.current_topic),
                    )
                    reply = call_llm(guide_system, full_msgs)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.step_state = "done"
                    st.session_state.current_step_q = None
                    _finalize_attempt(False)
                st.rerun()

        if st.button(t(st.session_state.language, "new_problem")):
            if st.session_state.step_state not in ("initial", "done"):
                _finalize_attempt(False)
            _reset_for_new_problem()
            st.rerun()

        st.markdown("---")
        st.markdown(
            """<div style="font-size:12px;color:#5A5880;line-height:1.8">
            <strong style="color:#9B99CC">How it works</strong><br>
    1. Type or upload a problem<br>
    2. Say yes or no to confidence<br>
    3. Answer one step at a time<br>
    4. AI checks every answer<br>
    5. Upload photos of your work
    </div>""",
            unsafe_allow_html=True,
        )


def _render_header() -> None:
    st.markdown(
        f"""<div style="display:flex;align-items:center;gap:14px;padding:20px 0 16px;
    border-bottom:1px solid rgba(108,99,255,0.2);margin-bottom:18px">
    <div style="width:48px;height:48px;background:linear-gradient(135deg,#6C63FF,#FF6584);
        border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:24px">S</div>
    <div>
        <div style="font-family:'Space Mono',monospace;font-size:19px;font-weight:700;
            background:linear-gradient(135deg,#A78BFA,#EC4899);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent">{t(st.session_state.language, 'title')}</div>
        <div style="font-size:13px;color:#5A5880;font-style:italic">{t(st.session_state.language, 'subtitle')}</div>
    </div>
</div>""",
        unsafe_allow_html=True,
    )


def run_app() -> None:
    init_progress_db(PROGRESS_DB_PATH)

    st.set_page_config(page_title="Socratic Math Tutor", page_icon="S", layout="wide")
    _init_session_state()
    st.markdown(build_styles(st.session_state.theme), unsafe_allow_html=True)

    _render_sidebar()
    _render_header()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.step_state == "guiding" and st.session_state.current_step_q:
        st.markdown(
            f"""<div class="step-box">
        <div class="step-label">{t(st.session_state.language, 'your_turn')}</div>
        <div class="step-q">{st.session_state.current_step_q}</div>
    </div>""",
            unsafe_allow_html=True,
        )

    if st.session_state.step_state == "waiting_yes_no":
        col1, col2, _ = st.columns([2, 2, 3])
        with col1:
            st.markdown('<div class="yes-btn">', unsafe_allow_html=True)
            if st.button("Yes, I know how", use_container_width=True):
                st.session_state.step_state = "waiting_solution"
                reply = (
                    "Awesome. Show me your solution - type it below or upload a photo "
                    "of your written work, then hit Submit."
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="no-btn">', unsafe_allow_html=True)
            if st.button("No, help me", use_container_width=True):
                st.session_state.step_state = "guiding"
                with st.spinner(t(st.session_state.language, "starting")):
                    start_msgs = [
                        {
                            "role": "user",
                            "content": (
                                "The student's problem is: "
                                f"{st.session_state.current_problem}\n\n"
                                "They said they don't know how to solve it. "
                                "Ask them the very first small question to get started. Do NOT solve it."
                            ),
                        }
                    ]
                    guide_system = get_system_guide(
                        st.session_state.language,
                        topic_instruction(st.session_state.current_topic),
                    )
                    reply = call_llm(guide_system, start_msgs)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.current_step_q = extract_bold_question(reply)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.step_state == "waiting_solution":
        st.markdown('<div class="submit-box">', unsafe_allow_html=True)
        st.markdown(f"**{t(st.session_state.language, 'submit_solution')}:**")
        col1, col2 = st.columns([3, 1])
        with col1:
            solution_text = st.text_area(
                t(st.session_state.language, "type_solution"),
                key="sol_text",
                height=120,
                placeholder="e.g. I factored it as (x-2)(x-3)=0, so x=2 or x=3",
            )
        with col2:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.file_uploader(
                t(st.session_state.language, "upload_photo"),
                type=["png", "jpg", "jpeg", "webp"],
                key="sol_img",
            )

        if st.button(t(st.session_state.language, "submit_solution_btn"), use_container_width=True):
            if solution_text or st.session_state.get("sol_img"):
                with st.spinner(t(st.session_state.language, "reviewing")):
                    st.session_state.interaction_count += 1
                    display = solution_text or "Solution photo submitted"
                    if st.session_state.get("sol_img"):
                        display = ("Photo + " + solution_text) if solution_text else "Solution photo submitted"
                    st.session_state.messages.append({"role": "user", "content": display})

                    review_msgs = st.session_state.messages + [
                        {
                            "role": "user",
                            "content": (
                                "Please review my solution above. The original problem was: "
                                f"{st.session_state.current_problem}"
                            ),
                        }
                    ]
                    review_system = get_system_review(
                        st.session_state.language,
                        topic_instruction(st.session_state.current_topic),
                    )
                    reply = call_llm(review_system, review_msgs)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    solved = is_solution_likely_correct(reply)
                    if solved:
                        st.session_state.step_state = "done"
                        _finalize_attempt(True)
                    else:
                        st.session_state.step_state = "guiding"
                        guide_system = get_system_guide(
                            st.session_state.language,
                            topic_instruction(st.session_state.current_topic),
                        )
                        followup = call_llm(
                            guide_system,
                            st.session_state.messages
                            + [{"role": "user", "content": "Ask one small corrective next step."}],
                        )
                        st.session_state.messages.append({"role": "assistant", "content": followup})
                        st.session_state.current_step_q = extract_bold_question(followup)
                st.rerun()
            else:
                st.warning(t(st.session_state.language, "warning_solution"))
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.step_state == "done":
        st.success(t(st.session_state.language, "done_message"))

    if st.session_state.step_state in ("initial", "guiding"):
        upload_label = (
            t(st.session_state.language, "upload_problem")
            if st.session_state.step_state == "initial"
            else t(st.session_state.language, "upload_work")
        )
        upload_key = "prob_img" if st.session_state.step_state == "initial" else "work_img"

        uploaded_file = st.file_uploader(upload_label, type=["png", "jpg", "jpeg", "webp"], key=upload_key)
        user_input = st.chat_input(
            t(st.session_state.language, "problem_input")
            if st.session_state.step_state == "initial"
            else t(st.session_state.language, "answer_input")
        )

        if user_input or uploaded_file:
            st.session_state.interaction_count += 1
            display = user_input or ""
            if uploaded_file:
                display = ("Photo + " + user_input) if user_input else "Image submitted"
            st.session_state.messages.append({"role": "user", "content": display})

            if st.session_state.step_state == "initial":
                st.session_state.current_problem = user_input or "the problem in the uploaded image"
                st.session_state.current_topic = detect_topic(st.session_state.current_problem)
                st.session_state.step_state = "waiting_yes_no"
                st.session_state.attempt_logged = False
                reply = (
                    "Got it! The problem is:\n\n"
                    f"**{st.session_state.current_problem}**\n\n"
                    "Do you already know how to solve this?"
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            elif st.session_state.step_state == "guiding":
                with st.spinner(t(st.session_state.language, "checking")):
                    guide_system = get_system_guide(
                        st.session_state.language,
                        topic_instruction(st.session_state.current_topic),
                    )
                    reply = call_llm(guide_system, st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.current_step_q = extract_bold_question(reply)
                    if not st.session_state.current_step_q:
                        st.session_state.step_state = "done"
                        _finalize_attempt(True)
                st.rerun()

    st.caption("Socratic Math Tutor - Powered by Groq | Patient guidance, not instant answers")
