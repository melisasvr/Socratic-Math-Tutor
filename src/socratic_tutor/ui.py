import streamlit as st

# RESOLVED CONFLICT: Keeping your Absolute Imports + Adding Himanshu's new modules
from socratic_tutor.config import (
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    PROGRESS_DB_PATH,
    WELCOME_MESSAGE,
)
from socratic_tutor.helpers import extract_bold_question, is_solution_likely_correct
from socratic_tutor.i18n import LANGUAGES, t
from socratic_tutor.llm import call_llm
from socratic_tutor.mistakes import (  # New Module
    detect_mistake_patterns,
    is_correction_feedback,
)
from socratic_tutor.progress import get_progress_stats, init_progress_db, record_attempt
from socratic_tutor.prompts import get_system_guide, get_system_review
from socratic_tutor.themes import THEMES, build_styles
from socratic_tutor.topics import detect_topic, topic_instruction


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
    # New: Tracking mistake tags for the current session
    if "current_mistake_tags" not in st.session_state:
        st.session_state.current_mistake_tags = set()


def _reset_for_new_problem() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    st.session_state.current_problem = None
    st.session_state.step_state = "initial"
    st.session_state.current_step_q = None
    st.session_state.current_topic = "general"
    st.session_state.interaction_count = 0
    st.session_state.attempt_logged = True
    st.session_state.current_mistake_tags = set()


def _finalize_attempt(solved: bool) -> None:
    if not st.session_state.current_problem or st.session_state.attempt_logged:
        return
    
    # Record attempt with the new mistake_tags field
    record_attempt(
        PROGRESS_DB_PATH,
        st.session_state.current_topic,
        solved,
        st.session_state.interaction_count,
        list(st.session_state.current_mistake_tags)
    )
    st.session_state.attempt_logged = True


def _format_mistake_label(tag: str) -> str:
    """Makes machine-readable tags (like 'sign_error') look pretty ('Sign Error')"""
    return tag.replace("_", " ").title()


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
        <div style="font-size:36px">∑</div>
        <div style="font-family:'Space Mono',monospace;font-size:14px;font-weight:700;
             background:linear-gradient(135deg,#A78BFA,#EC4899);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent">
             Socratic Math Tutor</div>
    </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Stats Section
        st.markdown(f"**{t(st.session_state.language, 'progress')}**")
        col1, col2 = st.columns(2)
        col1.metric(t(st.session_state.language, "total_solved"), stats["total_solved"])
        col2.metric(t(st.session_state.language, "total_attempts"), stats["total_attempts"])
        
        # New Feature: Common Mistakes List (Integrated with i18n)
        st.markdown(f"**{t(st.session_state.language, 'common_mistakes')}**")
        common_mistakes = stats.get("common_mistakes", [])[:3]
        if common_mistakes:
            for tag, count in common_mistakes:
                st.caption(f"- {_format_mistake_label(tag)} ({count})")
        else:
            st.caption(t(st.session_state.language, "no_mistake_patterns"))

        st.markdown("---")
        
        if st.button(t(st.session_state.language, "new_problem")):
            if st.session_state.step_state not in ("initial", "done"):
                _finalize_attempt(False)
            _reset_for_new_problem()
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="Socratic Math Tutor", page_icon="∑", layout="wide")
    _init_session_state()
    init_progress_db(PROGRESS_DB_PATH)
    
    theme_styles = build_styles(st.session_state.theme)
    st.markdown(theme_styles, unsafe_allow_html=True)
    
    _render_sidebar()

    st.title(f"∑ {t(st.session_state.language, 'title')}")

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle User Input
    if prompt := st.chat_input(t(st.session_state.language, "placeholder")):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.interaction_count += 1
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Logic: Solving or Guiding
        if st.session_state.step_state == "initial":
            # FIXED: treat topic_info as a direct string rather than a dictionary
            topic_info = detect_topic(prompt)
            st.session_state.current_topic = topic_info 
            st.session_state.current_problem = prompt
            st.session_state.step_state = "waiting_yes_no"
            st.session_state.attempt_logged = False
            
            reply = (
                f"{t(st.session_state.language, 'got_it_problem_intro')}\n\n"
                f"**{st.session_state.current_problem}**\n\n"
                f"{t(st.session_state.language, 'ask_confidence')}"
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        elif st.session_state.step_state == "waiting_yes_no":
            # Very simple yes/no detection
            if any(word in prompt.lower() for word in ["yes", "yeah", "yep", "ha", "haan", "sí", "evet"]):
                st.session_state.step_state = "reviewing"
                reply = t(st.session_state.language, "show_work")
            else:
                st.session_state.step_state = "guiding"
                reply = t(st.session_state.language, "let_us_start")
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        elif st.session_state.step_state in ["guiding", "reviewing"]:
            with st.spinner(t(st.session_state.language, "checking")):
                # Determine context
                if st.session_state.step_state == "guiding":
                    system_prompt = get_system_guide(
                        st.session_state.language, 
                        topic_instruction(st.session_state.current_topic)
                    )
                else:
                    system_prompt = get_system_review(
                     st.session_state.language, 
                     topic_instruction(st.session_state.current_topic)
                   )
                
                reply = call_llm(system_prompt, st.session_state.messages)
                
                # New Feature: Mistake Pattern Detection logic
                # Only analyze if the tutor seems to be correcting the student
                if is_correction_feedback(reply):
                    detected_tags = detect_mistake_patterns(prompt, reply)
                    st.session_state.current_mistake_tags.update(detected_tags)

                st.session_state.messages.append({"role": "assistant", "content": reply})
                
                # Check if session is finished
                if st.session_state.step_state == "reviewing":
                    if is_solution_likely_correct(reply):
                        st.session_state.step_state = "done"
                        _finalize_attempt(True)
                else:
                    st.session_state.current_step_q = extract_bold_question(reply)
                    if not st.session_state.current_step_q:
                        st.session_state.step_state = "done"
                        _finalize_attempt(True)
                
            st.rerun()

    st.caption("Socratic Math Tutor - Powered by Groq | Patient guidance, not instant answers")

if __name__ == "__main__":
    main()