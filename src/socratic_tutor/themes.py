THEMES = {
    "Classic": {
        "bg": "#0D0D1A",
        "card": "#1A1A35",
        "accent": "#6C63FF",
        "accent2": "#FF6584",
        "text": "#E8E6FF",
        "muted": "#9B99CC",
        "sidebar": "#13132B",
    },
    "High Contrast": {
        "bg": "#0A0A0A",
        "card": "#151515",
        "accent": "#00D1B2",
        "accent2": "#FFD166",
        "text": "#F7F7F7",
        "muted": "#B8B8B8",
        "sidebar": "#121212",
    },
    "Minimal Paper": {
        "bg": "#F7F4ED",
        "card": "#FFFDF8",
        "accent": "#1F7A8C",
        "accent2": "#BF4342",
        "text": "#1D1D1D",
        "muted": "#636363",
        "sidebar": "#EFE8DA",
    },
}


def build_styles(theme_name: str) -> str:
    theme = THEMES.get(theme_name, THEMES["Classic"])
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
:root {{ --bg: {theme['bg']}; --card: {theme['card']}; --accent: {theme['accent']}; --accent2: {theme['accent2']}; --text: {theme['text']}; --muted: {theme['muted']}; --sidebar: {theme['sidebar']}; }}
.stApp {{ background: radial-gradient(circle at 15% 15%, color-mix(in srgb, var(--accent) 22%, transparent), transparent 30%), radial-gradient(circle at 85% 5%, color-mix(in srgb, var(--accent2) 18%, transparent), transparent 32%), var(--bg) !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stChatMessage"] {{ background: var(--card) !important; border-radius: 14px !important; border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent) !important; margin-bottom: 8px !important; }}
.yes-btn button {{ background: color-mix(in srgb, #10B981 15%, transparent) !important; border: 2px solid color-mix(in srgb, #10B981 60%, transparent) !important; color: #6EE7B7 !important; font-size: 15px !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px !important; }}
.no-btn button  {{ background: color-mix(in srgb, #EF4444 12%, transparent) !important; border: 2px solid color-mix(in srgb, #EF4444 60%, transparent) !important; color: #FCA5A5 !important; font-size: 15px !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px !important; }}
.step-box {{ padding: 14px 18px; background: color-mix(in srgb, var(--accent) 10%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent); border-radius: 12px; margin: 10px 0 14px; }}
.step-label {{ font-size: 11px; font-family: 'Space Mono', monospace; color: var(--accent); font-weight: 700; letter-spacing: 1px; margin-bottom: 6px; }}
.step-q {{ font-size: 15px; color: var(--text); }}
.submit-box {{ padding: 16px 18px; background: color-mix(in srgb, var(--accent2) 9%, transparent); border: 1px solid color-mix(in srgb, var(--accent2) 35%, transparent); border-radius: 12px; margin: 10px 0; }}
[data-testid="stSidebar"] {{ background: var(--sidebar) !important; border-right: 1px solid color-mix(in srgb, var(--accent) 25%, transparent) !important; }}
.stButton > button {{ width: 100% !important; background: var(--card) !important; border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent) !important; color: var(--text) !important; border-radius: 10px !important; padding: 10px 14px !important; margin-bottom: 6px !important; text-align: left !important; transition: all .2s !important; }}
.stButton > button:hover {{ border-color: color-mix(in srgb, var(--accent) 70%, transparent) !important; transform: translateX(2px) !important; }}
[data-testid="stChatInput"] > div {{ background: var(--card) !important; border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent) !important; border-radius: 14px !important; }}
[data-testid="stChatInput"] textarea {{ color: var(--text) !important; background: transparent !important; }}
.stFileUploader > div {{ background: var(--card) !important; border: 1px dashed color-mix(in srgb, var(--accent) 35%, transparent) !important; border-radius: 12px !important; }}
.stSpinner > div {{ border-top-color: var(--accent) !important; }}
</style>
"""
