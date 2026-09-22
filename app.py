import streamlit as st
from research_agent import generate_long_research_report

st.set_page_config(page_title="AI Research Agent", page_icon="🔬", layout="wide")

st.markdown("""
<style>
.stApp { background: #0b1020; }
.block-container { max-width: 1200px; padding-top: 2rem; }
h1, h2, h3, h4, p, label, .stMarkdown, .stCaption { color: #f3f4f6 !important; }
.report-box { padding: 1rem; border-radius: 12px; background: #111827; border: 1px solid #374151; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 AI Research Agent")
st.caption("Generate a long-form, source-grounded research report from any topic.")

with st.sidebar:
    st.header("Report Settings")
    target_pages = st.slider("Target report length (pages)", 100, 500, 100, 25)
    research_rounds = st.slider("Research rounds", 3, 12, 6)
    st.info("Page count is estimated at about 500 words/page. Actual pages depend on document formatting.")

topic = st.text_area(
    "Research topic",
    placeholder="Example: The future of renewable energy and battery energy storage systems from 2025 to 2040",
    height=150,
)

if st.button("🚀 Generate Long Research Report", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.status("Preparing long-form research...", expanded=True) as status:
        try:
            report = generate_long_research_report(
                topic.strip(), target_pages, research_rounds
            )
            status.update(label="✅ Research report generated", state="complete", expanded=False)
        except Exception as exc:
            status.update(label="❌ Research failed", state="error", expanded=True)
            st.exception(exc)
            st.stop()

    word_count = len(report.split())
    estimated_pages = max(1, round(word_count / 500))

    st.markdown("## 📄 Research Report")
    c1, c2, c3 = st.columns(3)
    c1.metric("Words", f"{word_count:,}")
    c2.metric("Estimated pages", f"{estimated_pages:,}")
    c3.metric("Requested pages", f"{target_pages:,}")

    st.warning("The page count is an estimate. Actual printed pages vary with font, margins, spacing, tables, and export format.")

    st.download_button(
        "⬇️ Download Markdown Report",
        report,
        "research_report.md",
        "text/markdown",
        use_container_width=True,
    )

    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(report)
    st.markdown("</div>", unsafe_allow_html=True)
