# Multi-Agent Market Research & GenAI Use Case Generator

This Streamlit app conducts market research, generates AI/GenAI use cases, and collects relevant datasets for a given company or industry.

## How to Run Locally
1. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/multi-agent-market-research.git
   cd multi-agent-market-research
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your Serper API key in a `.env` file or as an environment variable:
   ```
   SERPER_API_KEY=your_serper_api_key
   ```
4. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

## Hosting on Streamlit Cloud
- Push your code to GitHub.
- Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your repo.
- Set your environment variables in the Streamlit Cloud settings.

## Features
- Industry/company research
- Dynamic use case generation
- Dataset collection from GitHub, Kaggle, Hugging Face
- PDF report download

---
