# KnowSphere — AI Document Question Answering System

**Student:** R Hemantha  
**Register number:** 25ETAI410054  
**Course:** AID201A — Artificial Intelligence  
**Course leader:** M Tanushri  
**Programme:** B.Tech., Semester 3 / 2025  
**Institution:** Department of Computer Science and Engineering, Faculty of Engineering & Technology, Ramaiah University of Applied Sciences

## Overview
KnowSphere accepts a document, extracts text, converts it into sentence-level knowledge records, retrieves relevant records for a question, applies transparent IF–THEN reasoning rules, and returns an evidence-grounded answer. It includes a benchmark evaluation page and unit tests.

## Important assignment constraint
This implementation does **not** use NLP techniques or RAG. It does not use language models, embeddings, vector databases, semantic encoders, or external answer-generation APIs. Processing is deterministic: punctuation-based segmentation, simple alphanumeric term matching, ranked lexical overlap, and explicit rule evaluation.

## Features
- Upload TXT, Markdown, CSV, PDF, and DOCX documents.
- Build and inspect a sentence-level knowledge base.
- Search and rank evidence for user questions.
- Apply explicit forward-chaining rules.
- Abstain when the evidence is insufficient.
- Run benchmark questions and display precision, recall, F1, and pass rate.
- Modern responsive Streamlit interface with dark gradient styling.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Run `python -m venv .venv` and activate it.
4. Run `pip install -r requirements.txt`.
5. Run `streamlit run app.py`.

## Test
Run `python -m unittest discover -s tests -v`.

## Folder structure
- `app.py` — Streamlit user interface
- `document_processor.py` — file extraction and knowledge-base construction
- `reasoning_engine.py` — retrieval, ranking, and rule inference
- `evaluation.py` — benchmark evaluation
- `data/` — sample document and rules
- `tests/` — test suite and benchmark questions
- `IEEE_Report.pdf` — report (maximum six pages)
- `screenshots/` — labelled interface design previews
- `docs/` — methodology and references

## Evidence note
The PNG files in `screenshots/` are **design previews** prepared to document the intended interface layout. They are not captured screenshots of a running application. For final submission, run the app and replace/add actual screenshots of document upload, question answering, and evaluation outputs. Attach any faculty-required laboratory/tool test evidence in the prescribed order.
