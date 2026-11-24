import streamlit as st
from pathlib import Path
from document_processor import extract_text, build_knowledge_base
from reasoning_engine import answer_question
from evaluation import evaluate_questions

st.set_page_config(page_title="KnowSphere | Document Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#eaf0ff; --muted:#9ba9c7; --panel:#121c35; --line:rgba(167,185,255,.14); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #26366d 0%, #111a34 38%, #080f20 100%); color:var(--ink); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101a33,#0b1225); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#eaf0ff !important; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.04em; color:#f4f6ff; }
p, label, .stMarkdown { color:#cbd5ed; }
.hero { padding:34px 36px; border:1px solid rgba(180,195,255,.2); border-radius:24px; background:linear-gradient(115deg,rgba(93,89,214,.35),rgba(25,173,190,.12)),linear-gradient(135deg,#1a2850,#111b36); box-shadow:0 20px 60px rgba(0,0,0,.18); margin-bottom:24px; }
.eyebrow { color:#a9b8ff; text-transform:uppercase; letter-spacing:.16em; font-size:11px; font-weight:700; }
.hero h1 { font-size:42px; line-height:1.08; margin:10px 0 12px; }
.hero p { color:#c1cbea; max-width:680px; font-size:15px; }
.metric { background:rgba(19,30,56,.82); border:1px solid var(--line); padding:18px 20px; border-radius:18px; min-height:100px; }
.metric .num { font-size:28px; font-weight:800; color:#fff; font-family:'Manrope'; }
.metric .cap { color:#9eaccb; font-size:12px; margin-top:4px; }
.panel { background:rgba(18,28,53,.86); border:1px solid var(--line); padding:22px; border-radius:20px; }
.pill { display:inline-block; background:rgba(128,115,255,.18); color:#c8c2ff; border:1px solid rgba(159,147,255,.28); border-radius:99px; padding:5px 10px; font-size:11px; font-weight:700; }
.answer { background:linear-gradient(135deg,rgba(52,190,173,.13),rgba(107,105,255,.12)); border:1px solid rgba(107,218,201,.25); border-radius:18px; padding:20px; color:#efffff; }
.small-muted { color:#96a6c8; font-size:12px; }
div.stButton > button { border-radius:12px; border:1px solid rgba(160,170,255,.3); background:linear-gradient(100deg,#6c63df,#398eae); color:white; font-weight:700; padding:.62rem 1.1rem; }
div.stButton > button:hover { border-color:#a8dfff; color:white; transform:translateY(-1px); }
.stTextInput input, .stTextArea textarea { background:#101a32 !important; color:#f1f4ff !important; border:1px solid rgba(167,185,255,.2) !important; border-radius:12px !important; }
[data-testid="stFileUploader"] { background:rgba(18,28,53,.65); border:1px dashed rgba(160,180,255,.3); border-radius:16px; padding:12px; }
hr { border-color:rgba(167,185,255,.14); }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

SAMPLE = Path(__file__).parent / "data" / "sample_knowledge.txt"
if "kb" not in st.session_state:
    st.session_state.kb = build_knowledge_base(SAMPLE.read_text(encoding="utf-8"))
if "source_name" not in st.session_state:
    st.session_state.source_name = "Sample Knowledge Pack"

with st.sidebar:
    st.markdown("## ✦ KnowSphere")
    st.caption("DOCUMENT INTELLIGENCE")
    page = st.radio("WORKSPACE", ["Overview", "Ask a question", "Knowledge base", "Evaluation", "About project"], label_visibility="visible")
    st.markdown("---")
    st.markdown("**PROJECT OWNER**")
    st.write("R Hemantha")
    st.caption("25ETAI410054 · AID201A")
    st.markdown("---")
    st.caption("Rule-based AI · No NLP · No RAG")

if page == "Overview":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">AID201A · ARTIFICIAL INTELLIGENCE</div>
      <h1>Answers grounded<br>in your documents.</h1>
      <p>KnowSphere transforms a document into a structured knowledge base, then uses transparent search and rule-based reasoning to answer questions with traceable evidence.</p>
      <span class="pill">DOCUMENT QUESTION ANSWERING</span>&nbsp; <span class="pill">RULE-BASED AI</span>
    </div>""", unsafe_allow_html=True)
    a,b,c = st.columns(3)
    for col, n, cap in [(a,str(len(st.session_state.kb)),"Knowledge statements"),(b,"3","Reasoning stages"),(c,"0","NLP / RAG components")]:
        col.markdown(f'<div class="metric"><div class="num">{n}</div><div class="cap">{cap}</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right = st.columns([1.2,1])
    with left:
        st.markdown('<div class="panel"><div class="eyebrow">HOW IT WORKS</div><h3>From file to answer</h3><p>01 · Extract text from an uploaded document.</p><p>02 · Segment it into factual statements and index its terms.</p><p>03 · Match a question to evidence and apply explicit IF–THEN rules.</p><p>04 · Return an answer with supporting source statements, or abstain when evidence is weak.</p></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="eyebrow">QUICK START</div><h3>Try the knowledge assistant</h3><p>Use the sample knowledge pack or upload a TXT, MD, CSV, PDF, or DOCX document.</p></div>',unsafe_allow_html=True)
        if st.button("Go to question workspace →", use_container_width=True):
            st.session_state.quick_nav = True
    st.caption(f"Active source: {st.session_state.source_name}")

elif page == "Ask a question":
    st.markdown('<div class="eyebrow">QUESTION WORKSPACE</div><h1>Ask your document</h1><p class="small-muted">Answers are generated only from retrieved knowledge-base statements and rule conclusions.</p>',unsafe_allow_html=True)
    q = st.text_input("Your question", placeholder="e.g. What is the main campus address?")
    examples = ["What is the university name?","Where is the campus located?","What is the course duration?","What is the purpose of the Solar System?"]
    st.caption("Try an example: " + " · ".join(examples))
    chosen = st.selectbox("Example questions", ["Choose an example"]+examples, label_visibility="collapsed")
    if chosen != "Choose an example":
        q = chosen
    if st.button("Find answer  →", type="primary"):
        if not q.strip():
            st.warning("Enter a question first.")
        else:
            result = answer_question(q, st.session_state.kb)
            st.markdown("#### Answer")
            st.markdown(f'<div class="answer">{result["answer"]}</div>',unsafe_allow_html=True)
            st.caption(f'Confidence: {result["confidence"]:.0%} · Method: {result["method"]} · Retrieved statements: {len(result["evidence"])}')
            if result["evidence"]:
                st.markdown("#### Evidence from the document")
                for i, item in enumerate(result["evidence"],1):
                    st.markdown(f'<div class="panel"><span class="pill">EVIDENCE {i}</span><p>{item}</p></div>',unsafe_allow_html=True)
            else:
                st.info("No sufficiently relevant evidence was found. Try rephrasing the question or uploading a more relevant document.")

elif page == "Knowledge base":
    st.markdown('<div class="eyebrow">DOCUMENT INGESTION</div><h1>Build your knowledge base</h1><p class="small-muted">Upload a suitable document. The application extracts text and creates sentence-level facts plus a simple term index.</p>',unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a document", type=["txt","md","csv","pdf","docx"])
    if uploaded is not None and st.button("Process document  →"):
        try:
            raw = extract_text(uploaded.getvalue(), uploaded.name)
            st.session_state.kb = build_knowledge_base(raw)
            st.session_state.source_name = uploaded.name
            st.success(f"Knowledge base created from {uploaded.name}")
        except Exception as e:
            st.error(f"Could not process this file: {e}")
    st.markdown(f'<div class="metric"><div class="num">{len(st.session_state.kb)}</div><div class="cap">Statements currently stored · {st.session_state.source_name}</div></div>',unsafe_allow_html=True)
    with st.expander("Inspect stored knowledge"):
        for i, fact in enumerate(st.session_state.kb,1):
            st.write(f"**K{i:03d}**  {fact['text']}")
    if st.button("Restore sample knowledge pack"):
        st.session_state.kb = build_knowledge_base(SAMPLE.read_text(encoding="utf-8"))
        st.session_state.source_name = "Sample Knowledge Pack"
        st.rerun()

elif page == "Evaluation":
    st.markdown('<div class="eyebrow">SYSTEM VALIDATION</div><h1>Evaluation lab</h1><p class="small-muted">Run the included benchmark questions against the active knowledge base.</p>',unsafe_allow_html=True)
    if st.button("Run evaluation  →", type="primary"):
        questions_path = Path(__file__).parent/"tests"/"evaluation_questions.csv"
        metrics, rows = evaluate_questions(questions_path, st.session_state.kb)
        x,y,z = st.columns(3)
        x.metric("Pass rate",f'{metrics["pass_rate"]:.0%}')
        y.metric("Precision",f'{metrics["precision"]:.2f}')
        z.metric("Recall",f'{metrics["recall"]:.2f}')
        st.metric("F1 score",f'{metrics["f1"]:.2f}')
        st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption("Evaluation is based on expected-answer keyword coverage and is a lightweight project metric, not a human-quality assessment.")

elif page == "About project":
    st.markdown('<div class="eyebrow">PROJECT DOCUMENTATION</div><h1>Transparent by design.</h1>',unsafe_allow_html=True)
    st.markdown("""
    <div class="panel">
    **Student:** R Hemantha · **Register number:** 25ETAI410054<br>
    **Course:** AID201A – Artificial Intelligence<br>
    **Course leader:** M Tanushri<br>
    **Programme:** B.Tech., Semester 3, 2025<br><br>
    **Approach:** sentence-level knowledge representation, inverted term indexing, lexical overlap retrieval, forward chaining over explicit rules, evidence-grounded response generation, and benchmark evaluation.<br><br>
    **Excluded:** NLP pipelines, language models, embeddings, vector databases, and Retrieval-Augmented Generation (RAG).
    </div>
    """,unsafe_allow_html=True)
    st.markdown("#### Design justification")
    st.write("The selected methods are explainable, deterministic, and suitable for a small document QA prototype. Each answer can be traced to stored statements or a rule conclusion. A confidence threshold supports abstention when the document does not contain enough evidence.")
