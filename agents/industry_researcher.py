import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "81e90d32dc6660a5899bc748648404ac66bc32f2")
SERPER_URL = "https://google.serper.dev/search"

class IndustryResearcherAgent:
    def __init__(self):
        self.headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

    def research_industry(self, company_or_industry: str) -> dict:
        query = f"{company_or_industry} industry overview AI digital transformation"
        payload = {"q": query, "num": 5}
        try:
            response = requests.post(SERPER_URL, headers=self.headers, json=payload)
            if response.status_code != 200:
                return {"error": response.text}
            results = response.json()
            links = []
            for item in results.get("organic", []):
                links.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
            return {"results": links}
        except Exception as e:
            return {"error": str(e)}
