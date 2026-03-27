# ∑ Socratic Math Tutor

- An AI-powered math tutoring app that guides students through problems using Socratic questioning, one small step at a time, rather than just handing out answers.
- Built with Python, Streamlit, and Groq (free, fast, no credit card needed).

---

## Quick Start

### 1. Get a free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up — free, no credit card required
3. Click **API Keys → Create API Key**
4. Copy the key (starts with `gsk_...`)

### 2. Set up your `.env` file

Create a file called `.env` in the same folder as `app.py`:

```
GROQ_API_KEY=gsk_your_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

⚠️ No quotes around values, no spaces around `=`

### 3. Install dependencies

```bash
pip install streamlit langchain-openai langchain-core openai python-dotenv
```

Or with the requirements file:

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

### 5. Run tests

```bash
pytest -q
```

---

## GitHub Workflows (CI/CD)

This repository now includes three GitHub Actions workflows under `.github/workflows/`:

- `ci.yml`
        - Trigger: push and pull request on `main`, `master`, `develop`
        - Runs Ruff lint checks and unit tests on Python 3.11

- `tests.yml`
        - Trigger: pull request, and manual run (`workflow_dispatch`)
        - Runs a Python version matrix (`3.10`, `3.11`, `3.12`, `3.13`)
        - Generates and uploads `coverage.xml` artifact from the 3.11 job
        - Uploads coverage to Codecov (non-blocking)

- `cd.yml`
        - Trigger: push to `main`, version tags like `v1.0.0`, and manual run (`workflow_dispatch`)
        - Builds a release archive after tests
        - Development path: runs for `main` push or manual `target=development`
        - Production path: runs for tag push or manual `target=production`
        - Automatically creates a GitHub Release for tag builds

### Recommended Branch Protection

In GitHub repository settings for `main`, enable branch protection with:

- Require a pull request before merging
- Require status checks to pass before merging
        - Required checks:
                - `Lint and Unit Tests (Python 3.11)`
                - `Pytest (Python 3.10)`
                - `Pytest (Python 3.11)`
                - `Pytest (Python 3.12)`
                - `Pytest (Python 3.13)`
- Require branches to be up to date before merging
- Include administrators

---

## How It Works

The tutor follows a strict Socratic flow for every problem:

```
Student types/uploads a problem
        ↓
"Do you already know how to solve this?"
        ↓
   YES ─────────────────────── NO
    ↓                           ↓
"Show me your solution,"    Guided step by step
(type or upload photo)     (one question at a time)
        ↓                       ↓
   AI reviews it           AI checks each answer
   and gives feedback      and moves to the next step
        ↓                       ↓
        └──────── ✅ Done! ──────┘
```

---

## Features
- **Strict Socratic flow** — never gives the answer, always asks first
- **Yes / No confidence check** — student declares what they know before starting
- **Step-by-step guidance** — one small question at a time, AI checks each answer
- **Solution upload** — students can type their solution or upload a photo of their written work
- **Problem upload** — upload a photo of a textbook problem instead of typing it
- **Sidebar actions** — 💡 Hint, 📖 Full solution, 🆕 New problem
- **Phase indicator** — sidebar shows current state (waiting/guiding/reviewing/done)
- **Topic expansion** — topic-aware support for linear algebra, statistics, and number theory
- **Multi-language support** — English, Hindi, and Spanish UI/prompt modes
- **Progress tracker** — persistent session metrics (solved, attempts, streak, last 7 days)
- **Theme system** — switch between Classic, High Contrast, and Minimal Paper
- **Powered by Groq** — free tier, fast responses, reliable

---

## Changing the Model

Edit `MODEL_NAME` in your `.env` (no quotes):

```
MODEL_NAME=llama-3.3-70b-versatile     ← default, recommended
MODEL_NAME=llama-3.1-8b-instant        ← faster, lighter
MODEL_NAME=mixtral-8x7b-32768          ← alternative
```

See all available models at [console.groq.com/docs/models](https://console.groq.com/docs/models)

---

## Project Structure

```
.
├── app.py                      # lightweight Streamlit entrypoint
├── .env                        # your API key (never commit this)
├── .env.example                # template — copy to .env and fill in
├── requirements.txt            # Python dependencies
├── pytest.ini                  # pytest configuration
├── tests/                      # unit test baseline
│   ├── conftest.py
│   ├── test_helpers.py
│   ├── test_progress.py
│   └── test_topics.py
└── src/
    └── socratic_tutor/
        ├── __init__.py
        ├── config.py             # env/config constants
        ├── prompts.py            # language/topic-aware system prompts
        ├── llm.py                # Groq/OpenAI-compatible LLM wrapper
        ├── helpers.py            # shared helpers
        ├── i18n.py               # translations and language strings
        ├── themes.py             # theme presets and CSS builder
        ├── topics.py             # topic detection and topic guidance
        ├── progress.py           # SQLite progress tracking
        └── ui.py                 # Streamlit UI and app flow
```

---

## Supported Math Topics

Algebra, calculus, geometry, trigonometry, word problems, and more.
Just type or upload any high school or college level math problem.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `model_not_found` | Remove quotes around `MODEL_NAME` in `.env` |
| `No GROQ_API_KEY` | Make sure `.env` is in the same folder as `app.py` |
| Yes/No buttons missing | Scroll down — they appear below the problem statement |
| App remembers old problem | Click **🆕 New problem** in the sidebar |

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
   ```bash
   git clone https://github.com/your-username/socratic-math-tutor.git
   cd socratic-math-tutor
   ```
3. **Create a branch** for your feature or fix
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them locally
5. **Commit** with a clear message
   ```bash
   git commit -m "Add: brief description of your change."
   ```
6. **Push** and open a **Pull Request**

### Ideas for contributions
- 📐 Add more math topics (linear algebra, statistics, number theory)
- 🌍 Add multi-language support
- 📊 Add a progress tracker across sessions
- 🎨 UI improvements or themes
- 🧪 Add unit tests

For ready-to-use issue drafts (scope, acceptance criteria, labels, and estimates), see:

- `docs/CONTRIBUTION_ROADMAP.md`

- Please keep PRs focused on one feature or fix per PR. Be kind and constructive in reviews.

---

## License
```
MIT License

Copyright (c) 2026 Socratic Math Tutor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including, without limitation, the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

