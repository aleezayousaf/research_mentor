import streamlit as st
from crewai import Task, Crew, Process

# Import configuration and agent factories
from config import setup_environment
from agents.socratic_supervisor import get_socratic_supervisor
from agents.legal_researcher import get_legal_researcher
from agents.writing_coach import get_writing_coach
from agents.citation_integrator import get_citation_integrator
from agents.journal_publisher import get_journal_publisher

st.set_page_config(
    page_title="ResearchMentor AI - Multi-Agent Legal Supervisor",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ ResearchMentor AI: Legal Research Supervisor Matrix")
st.caption("Powered by CrewAI, Multi-Agent Memory, RAG Tools, and Socratic Guardrails")

# Sidebar for API Key
with st.sidebar:
    st.header("🔑 Credentials")
    gemini_key = st.text_input("Gemini API Key", type="password")
    if gemini_key:
        setup_environment(gemini_key)
        st.success("API Key Active!")

# Select Syllabus Phase
selected_phase = st.selectbox(
    "Select Active Workflow Phase (16-Week Roadmap):",
    [
        "Phase 1: Topic Refinement & Socratic Challenge (Agent 1)",
        "Phase 2: RAG Source Discovery & Legal Verification (Agent 2)",
        "Phase 3: IRAC Writing & Structural Analysis (Agent 3)",
        "Phase 4: Citation Integrity & OSCOLA Conversion (Agent 4)",
        "Phase 5: Journal Targeting & Manuscript Anonymization (Agent 5)"
    ]
)

student_input = st.text_area(
    "Enter your Research Proposal, Draft Paragraph, or Topic:",
    height=160,
    placeholder="Type or paste your research materials here..."
)

if st.button("Run AI Supervisor Crew Workflow"):
    if not gemini_key:
        st.error("Please provide a valid Gemini API Key in the sidebar.")
    elif not student_input.strip():
        st.warning("Input area cannot be empty.")
    else:
        with st.spinner("Orchestrating Multi-Agent Workflow with Memory & Verification..."):
            try:
                # Instantiate Agents
                ag1 = get_socratic_supervisor()
                ag2 = get_legal_researcher()
                ag3 = get_writing_coach()
                ag4 = get_citation_integrator()
                ag5 = get_journal_publisher()

                # Dynamic Task Definition & Agent Selection
                if "Phase 1" in selected_phase:
                    active_agents = [ag1]
                    task = Task(
                        description=(
                            f"Evaluate input: '{student_input}'.\n"
                            "GUARDRAIL ENFORCEMENT: Do NOT write paper text for the student.\n"
                            "1. Ask 3 sharp Socratic questions challenging the scope and legal claims.\n"
                            "2. Require the student to narrow their normative research question."
                        ),
                        expected_output="Socratic critique and scope-narrowing questions.",
                        agent=ag1
                    )
                elif "Phase 2" in selected_phase:
                    active_agents = [ag2]
                    task = Task(
                        description=(
                            f"Execute retrieval tools for topic: '{student_input}'.\n"
                            "1. Call 'Search Global Scholarly Literature' for peer-reviewed papers.\n"
                            "2. Call 'Search Pakistan Code' for primary statutory references.\n"
                            "3. Return a verified source matrix."
                        ),
                        expected_output="Verified statutory and scholarly reference list with DOIs/Citations.",
                        agent=ag2
                    )
                elif "Phase 3" in selected_phase:
                    active_agents = [ag3]
                    task = Task(
                        description=(
                            f"Analyze this draft text using IRAC: '{student_input}'.\n"
                            "Tag paragraphs as [Issue], [Rule], [Application], or [Conclusion]. "
                            "Flag logical gaps and unsupported legal leaps."
                        ),
                        expected_output="Detailed IRAC structural critique.",
                        agent=ag3
                    )
                elif "Phase 4" in selected_phase:
                    active_agents = [ag4]
                    task = Task(
                        description=(
                            f"Convert raw citations into OSCOLA and Bluebook footnote format: '{student_input}'."
                        ),
                        expected_output="Formatted footnote citations following OSCOLA standards.",
                        agent=ag4
                    )
                else: # Phase 5
                    active_agents = [ag5]
                    task = Task(
                        description=(
                            f"Evaluate topic against HEC / Scopus journal standards: '{student_input}'.\n"
                            "Provide a double-blind anonymization checklist and target journal criteria."
                        ),
                        expected_output="Journal selection guide and anonymization checklist.",
                        agent=ag5
                    )

                # Initialize Crew with Agent Memory Enabled
                crew = Crew(
                    agents=active_agents,
                    tasks=[task],
                    process=Process.sequential,
                    memory=True,  # Enables Short-Term, Long-Term, and Entity Memory
                    verbose=True
                )

                result = crew.kickoff()

                st.success("Workflow Execution Completed Successfully!")
                st.markdown("### 📋 AI Supervisor Output")
                st.markdown(str(result))

            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
