# Mind Jungle 🌿

> A journal analyzer that helps you reflect on your thoughts and understand your emotional patterns. Instead of being a jumble of words and thoughts, the analyzer will help you organize them and help you visualize how you've been feeling recently.

## What it does

Mind Jungle takes your raw, unfiltered journal entries and transforms them into structured insights. Go ahead and paste anything: stream of consciousness, venting, reflections, and get back a breakdown of your themes, emotional tone, a summary, and a gentle reframe. An animated mood meter visualizes your emotional heaviness score at a glance.

## Features

- 🧠 Journal analysis with structured output
- 🎨 Animated emotional heaviness meter
- ✨ Prompts to help you get started
- 🔒 Your entries are never saved — full privacy by default!

## Tech Stack

- **Frontend/UI:** Streamlit
- **AI:** Groq API (LLaMA 3.3 70B)
- **Language:** Python
- **Deployment:** Streamlit Community Cloud

## Run it locally
```bash
# Clone the repo
git clone https://github.com/yoshisaurusrex-rawr/mind-jungle.git
cd mind-jungle

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
streamlit run mind_jungle.py
```

## Live Demo

👉 [Try Mind Jungle here](https://mind-jungle.streamlit.app/)

## Author

Built by [Yoshi](https://github.com/yoshisaurusrex-rawr) as a build/data analysis portfolio project.