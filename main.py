import streamlit as st
from agents.industry_researcher import IndustryResearcherAgent
from agents.use_case_generator import UseCaseGeneratorAgent
from agents.resource_collector import ResourceCollectorAgent
import os
from fpdf import FPDF
import re

st.set_page_config(page_title="Multi-Agent Market Research & Use Case Generator", layout="wide")
st.title("🧠 Multi-Agent Market Research & GenAI Use Case Generator")

st.markdown("""
This app conducts market research, generates AI/GenAI use cases, and collects relevant datasets for a given company or industry.
""")

company_or_industry = st.text_input("Enter Company or Industry Name:", "Retail")

if st.button("Run Multi-Agent Workflow"):
    # 1. Industry/Company Research
    st.subheader("1️⃣ Industry/Company Research")
    researcher = IndustryResearcherAgent()
    research_results = researcher.research_industry(company_or_industry)
    if "results" in research_results:
        for r in research_results["results"]:
            st.markdown(f"- [{r['title']}]({r['link']})\n> {r['snippet']}")
    else:
        st.error(f"Error: {research_results.get('error', 'Unknown error')}")

    # 2. Use Case Generation
    st.subheader("2️⃣ Use Case Generation")
    use_case_agent = UseCaseGeneratorAgent()
    use_cases = use_case_agent.generate_use_cases(company_or_industry)
    st.markdown(f"**Generated Use Cases:**\n\n{use_cases}")

    # 3. Resource Asset Collection
    st.subheader("3️⃣ Resource Asset Collection")
    resource_agent = ResourceCollectorAgent()
    resources_md = resource_agent.run(use_cases, user_input=company_or_industry)
    # Remove 'undefined' and fix topic links before displaying
    resources_md = resources_md.replace('undefined', '').replace('+Classification-dataset', '-dataset')
    st.markdown(resources_md, unsafe_allow_html=True)

    # 4. Final Proposal & References (show only once)
    st.subheader("4️⃣ Final Proposal & References")
    st.markdown("**Top Use Cases:**")
    for uc in use_cases.split("\n\n"):
        st.markdown(f"- {uc.split('**')[0].strip()}")
    st.markdown("**References:**")
    for r in research_results.get("results", []):
        st.markdown(f"- [{r['title']}]({r['link']})")

    st.success("Workflow completed! See outputs/resources.md for full resource links.")

    # PDF Download Button
    def remove_emojis(text):
        # Remove all emoji characters using regex
        emoji_pattern = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
        return emoji_pattern.sub(r"", text)

    def generate_pdf_from_md(md_text, pdf_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        clean_text = remove_emojis(md_text)
        for line in clean_text.splitlines():
            pdf.multi_cell(0, 10, line)
        pdf.output(pdf_path)

    pdf_path = "outputs/resources_report.pdf"
    generate_pdf_from_md(resources_md, pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download Report as PDF",
            data=f.read(),
            file_name="resources_report.pdf",
            mime="application/pdf"
        )
