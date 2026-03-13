import streamlit as st
import requests

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from io import BytesIO

from app.services.s3_service import upload_pdf
from app.services.methodology_service import generate_methodology
from app.services.novelty_plagiarism_service import analyze_novelty_plagiarism

methodology = st.session_state.get("methodology", "")
def generate_pdf(result, topic, methodology):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("AI-Powered Academic Research Assistant Report", styles['Title']))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Research Topic:</b> {topic}", styles['BodyText']))
    story.append(Spacer(1, 20))


    # -------------------------
    # Literature Review
    # -------------------------
    story.append(Paragraph("Literature Review", styles['Heading2']))
    story.append(Spacer(1, 10))

    for line in result.get("literature_review", "").split("\n"):
        story.append(Paragraph(line, styles['BodyText']))

    story.append(Spacer(1, 20))


    # -------------------------
    # Research Trends
    # -------------------------
    story.append(Paragraph("Major Research Trends", styles['Heading2']))
    story.append(Spacer(1, 10))

    trends = result.get("trends", "")

    if trends:
        story.append(Paragraph(trends, styles['BodyText']))

    story.append(Spacer(1, 20))


    # -------------------------
    # Research Gaps
    # -------------------------
    story.append(Paragraph("Research Gaps", styles['Heading2']))
    story.append(Spacer(1, 10))

    for line in result.get("research_gaps", "").split("\n"):
        story.append(Paragraph(line, styles['BodyText']))

    story.append(Spacer(1, 20))

    methodology = st.session_state.get("methodology", "")
    # -------------------------
    # Methodology
    # -------------------------
    story.append(Paragraph("Proposed Research Methodology", styles['Heading2']))
    story.append(Spacer(1, 10))

    if methodology:
        for line in methodology.split("\n"):
            story.append(Paragraph(line, styles['BodyText']))

    story.append(Spacer(1, 20))


    # -------------------------
    # Grant Proposal
    # -------------------------
    story.append(Paragraph("Grant Proposal", styles['Heading2']))
    story.append(Spacer(1, 10))

    for line in result.get("proposal", "").split("\n"):
        story.append(Paragraph(line, styles['BodyText']))

    story.append(Spacer(1, 20))


    # -------------------------
    # Novelty Analysis
    # -------------------------
    #story.append(Paragraph("Novelty & Plagiarism Analysis", styles['Heading2']))
    #story.append(Spacer(1, 10))

   # for line in result.get("novelty_analysis", "").split("\n"):
    #    story.append(Paragraph(line, styles['BodyText']))

    #story.append(Spacer(1, 20))


    # -------------------------
    # Top Research Papers
    # -------------------------
    story.append(Paragraph("Top Research Papers", styles['Heading2']))
    story.append(Spacer(1, 10))

    papers = result.get("papers", [])

    for paper in papers:

        story.append(Paragraph(f"<b>{paper['title']}</b>", styles['BodyText']))
        story.append(Paragraph(f"Link: {paper['link']}", styles['BodyText']))
        story.append(Spacer(1, 10))


    doc.build(story)

    buffer.seek(0)

    return buffer

st.set_page_config(page_title="AI Research Assistant")

st.title("📚 AI-Powered Academic Research Assistant & Grant Proposal Generator using RAG Architecture")

st.info("⚡ The system retrieves research papers, detects research gaps, and generates a grant proposal automatically.")

# -----------------------------
# INPUT SECTION
# -----------------------------

topic = st.text_input("Research Topic")

num_papers = st.slider(
    "Number of papers to retrieve",
    5,
    50,
    10
)

top_k = st.slider(
    "Top papers used for review",
    3,
    30,
    10
)

agency = st.selectbox(
    "Funding Agency",
    ["National Science Foundation (NSF)", "National Institutes of Health (NIH)", "Institute of Engineering & Management (IEM)", "General"]
)

domain = st.text_input("Research Domain")

duration = st.selectbox(
    "Project Duration",
    ["1-3 months", "4-6 months", "7-9 months", "1 year", "2 years", "3 years"]
)

# -----------------------------
# GENERATE REPORT
# -----------------------------

if st.button("🚀 Generate Research Report"):

    payload = {
        "topic": topic,
        "agency": agency,
        "duration": duration,
        "domain": domain,
        "top_k": top_k
    }

    with st.status("Running AI Research Pipeline...", expanded=True) as status:

        st.write("📚 Agent 1: Retrieving research papers")

        with st.spinner("Fetching papers and generating literature review..."):

            response = requests.post(
                "http://127.0.0.1:8000/generate-full-report",
                json=payload
            )

        st.write("🔍 Agent 2: Detecting research gaps")

        st.write("📑 Agent 3: Generating grant proposal")

        if response.status_code == 200:

            data = response.json()

            st.session_state["result"] = data

            status.update(label="✅ Research report generated successfully!", state="complete")

        else:

            st.error("Backend error occurred")
            st.write(response.text)

# -----------------------------
# OUTPUT TABS
# -----------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📚 Literature Review",
    "🔍 Research Gaps",
    "📑 Grant Proposal",
    "📊 Research Trends",
    "⚙️ Methodology",
    "🔍 Novelty & Plagiarism Assessment"
])


# -----------------------------
# LITERATURE TAB
# -----------------------------

with tab1:

    if "result" in st.session_state:

        result = st.session_state["result"]

        st.subheader("Literature Review")

        st.write(result["literature_review"])

        st.divider()

        st.subheader("📑 Top Research Papers")

        st.caption(f"Showing Top {len(result['papers'])} most relevant papers")

        for paper in result["papers"]:

            with st.expander(paper["title"]):

                st.write(paper["summary"])

                st.markdown(f"[🔗 Read Paper]({paper['link']})")


# -----------------------------
# RESEARCH GAPS TAB
# -----------------------------

with tab2:

    import networkx as nx

    from app.services.graph_visualization_service import plot_paper_graph

    if "result" in st.session_state:

        result = st.session_state["result"]

        graph = nx.Graph()

        graph.add_nodes_from(result["graph_nodes"])
        graph.add_edges_from(result["graph_edges"])

        st.subheader("Citation / Similarity Network")

        fig = plot_paper_graph(graph)

        st.pyplot(fig)

        st.subheader("Research Gaps")

        st.write(result["research_gaps"])


# -----------------------------
# GRANT PROPOSAL TAB
# -----------------------------

with tab3:

    if "result" in st.session_state:

        result = st.session_state["result"]

        st.subheader("Grant Proposal")

        st.write(result["proposal"])

with tab4:

    if "result" in st.session_state:

        st.subheader("Research Trends")

        trends = result.get("trends", "")

        st.write(trends)

with tab5:

    if "result" in st.session_state:

        result = st.session_state["result"]

        gaps = result.get("research_gaps", [])
        trends = result.get("trends", [])

        st.subheader("Select Research Gap to Design Methodology")

        if gaps:

            import re

            gaps_text = result.get("research_gaps", "")

            # Extract research gaps
            gaps = re.findall(r"Research Gap \d+:.*?(?=Research Gap \d+:|$)", gaps_text, re.S)

            gap_titles = []
            gap_map = {}

            for gap in gaps:

                title_match = re.search(r"Gap Title:\s*(.*)", gap)

                if title_match:
                    title = title_match.group(1).split("\n")[0].strip()
                else:
                    title = gap[:80]

                gap_titles.append(title)
                gap_map[title] = gap


            # Only show radio if titles exist
            if gap_titles:

                selected_gap_title = st.radio(
                    "Choose a research gap:",
                    gap_titles
                )

                selected_gap = gap_map.get(selected_gap_title)

                st.session_state["selected_gap"] = selected_gap

            else:
                st.warning("No research gaps detected.")

            st.divider()

            if st.button("Generate Methodology for Selected Gap"):

                methodology = generate_methodology(
                    topic,
                    selected_gap,
                    trends
                )

                st.session_state["methodology"] = methodology
                summaries = [paper["summary"] for paper in result["papers"]]

                novelty = analyze_novelty_plagiarism(
                    methodology,
                    summaries
                )

                st.session_state["novelty_result"] = novelty

        if "methodology" in st.session_state:

            st.subheader("Proposed Research Methodology")

            st.write(st.session_state["methodology"])

with tab6:

    if "novelty_result" in st.session_state:

        novelty = st.session_state["novelty_result"]

        st.metric("Novelty Score", novelty["novelty_score"])
        st.metric("Similarity Score", novelty["similarity_score"])

        risk = novelty["plagiarism_risk"]

        if risk == "High":
            st.error(f"Plagiarism Risk: {risk}")
        elif risk == "Moderate":
            st.warning(f"Plagiarism Risk: {risk}")
        else:
            st.success(f"Plagiarism Risk: {risk}")

        st.divider()

        st.subheader("Ethical AI Assessment")
        st.write(novelty["ethical_analysis"])

if "result" in st.session_state:
    result = st.session_state["result"]
    pdf = generate_pdf(result, topic, methodology)

    s3_url = upload_pdf(pdf)

   # st.download_button(
   # label="📄 Download Research Report",
   # data=pdf,
   # file_name="research_report.pdf",
   # mime="application/pdf",
   # type="primary"
    #)    
    st.success("Report stored in AWS S3")

    st.markdown(f"[Download Report from Cloud]({s3_url})")