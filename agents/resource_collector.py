import requests
import os
import re

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "81e90d32dc6660a5899bc748648404ac66bc32f2")
SERPER_URL = "https://google.serper.dev/search"

class ResourceCollectorAgent:
    def __init__(self):
        self.headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

    def search_github_links(self, user_query: str) -> list:
        query = f"site:github.com dataset {user_query}"
        payload = {"q": query, "num": 5}
        try:
            response = requests.post(SERPER_URL, headers=self.headers, json=payload)
            if response.status_code != 200:
                return []
            results = response.json()
            github_links = []
            for item in results.get("organic", []):
                title = item.get("title", "").replace(" · GitHub", "").replace("GitHub - ", "")
                link = item.get("link", "")
                snippet = item.get("snippet", "")
                if ("github.com" in link and "/blob/" not in link and any(term in (title + snippet).lower() for term in ["dataset", "data-set", "training-data", "corpus", "data science"])):
                    github_links.append({"title": title, "link": link, "description": snippet})
            return github_links
        except Exception:
            return []

    def search_huggingface_links(self, user_query: str) -> list:
        # Simulate Hugging Face dataset search result
        # In production, use Hugging Face API
        return [{
            "title": f"{user_query} dataset (Hugging Face)",
            "link": f"https://huggingface.co/datasets?search={'+'.join(user_query.split())}",
            "description": "Explore datasets for NLP, vision, and more on Hugging Face."
        }]

    def search_kaggle_links(self, user_query: str) -> list:
        # Simulate Kaggle dataset search result
        # In production, use Kaggle API
        return [{
            "title": f"{user_query} dataset (Kaggle)",
            "link": f"https://www.kaggle.com/search?q={'+'.join(user_query.split())}+dataset",
            "description": "Find ML datasets for your use case on Kaggle."
        }]

    def run(self, use_cases: str, user_input: str = None) -> str:
        use_case_blocks = re.split(r"(?=^\d+\.\s)", use_cases, flags=re.MULTILINE)
        md = "# Resource Links\n\n"
        for block in use_case_blocks:
            title_match = re.match(r"^\d+\.\s+(.+)", block)
            if not title_match:
                continue
            title = title_match.group(1).strip()
            desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)(\n|$)", block)
            description = desc_match.group(1).strip() if desc_match else "No description found."
            # Use user_input directly for dataset search if provided
            if user_input:
                search_query = user_input
            else:
                search_query = title
            github_results = self.search_github_links(search_query)
            huggingface_results = self.search_huggingface_links(search_query)
            kaggle_results = self.search_kaggle_links(search_query)
            md += f"## {title}\n\n"
            md += f"**Description:** {description}\n\n"
            # GitHub datasets
            if github_results:
                md += "### 📊 Available GitHub Datasets\n\n"
                for idx, result in enumerate(github_results, 1):
                    md += f"📦 [{result['title']}]({result['link']})\n"
                    if result['description']:
                        md += f"📝 {result['description']}\n"
                    md += "\n"
            # Hugging Face datasets
            if huggingface_results:
                md += "### 🤗 Available Hugging Face Datasets\n\n"
                for result in huggingface_results:
                    md += f"📦 [{result['title']}]({result['link']})\n"
                    if result['description']:
                        md += f"📝 {result['description']}\n"
                    md += "\n"
            # Kaggle datasets
            if kaggle_results:
                md += "### 🏅 Available Kaggle Datasets\n\n"
                for result in kaggle_results:
                    md += f"📦 [{result['title']}]({result['link']})\n"
                    if result['description']:
                        md += f"📝 {result['description']}\n"
                    md += "\n"
        with open("outputs/resources.md", "w", encoding="utf-8") as f:
            f.write(md)
        return md
