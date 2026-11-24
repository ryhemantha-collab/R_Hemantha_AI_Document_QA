"""Document ingestion and sentence-level knowledge representation.
No NLP libraries, embeddings, or RAG are used.
"""
import csv, io, re
from pathlib import Path

def extract_text(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext in {".txt", ".md"}:
        return data.decode("utf-8", errors="replace")
    if ext == ".csv":
        rows = list(csv.reader(io.StringIO(data.decode("utf-8", errors="replace"))))
        return "\n".join(" | ".join(cell.strip() for cell in row if cell.strip()) for row in rows)
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError as exc:
            raise RuntimeError("Install pypdf to process PDF files.") from exc
    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError as exc:
            raise RuntimeError("Install python-docx to process DOCX files.") from exc
    raise ValueError("Supported formats: TXT, MD, CSV, PDF, DOCX.")

def build_knowledge_base(text: str):
    # Deterministic punctuation-based segmentation; no linguistic parsing.
    pieces = re.split(r"(?<=[.!?])\s+|\n+", text)
    facts, seen = [], set()
    for piece in pieces:
        clean = re.sub(r"\s+", " ", piece).strip(" \t\r\n-•")
        if len(clean) < 12:
            continue
        key = clean.casefold()
        if key in seen:
            continue
        seen.add(key)
        terms = re.findall(r"[A-Za-z0-9]+", clean.casefold())
        facts.append({"id": f"K{len(facts)+1:03d}", "text": clean, "terms": terms})
    return facts
