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
├── app.py            # complete single-file Streamlit app
├── .env              # your API key (never commit this)
├── .env.example      # template — copy to .env and fill in
└── requirements.txt  # Python dependencies
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
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
```

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
