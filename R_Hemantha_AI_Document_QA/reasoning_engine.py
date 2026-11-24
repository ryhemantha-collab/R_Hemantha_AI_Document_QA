"""Lexical retrieval and explicit forward-chaining inference."""
import re
STOP = {"what","where","when","who","why","how","is","are","was","were","the","a","an","of","in","on","for","to","and","does","do","tell","me","about","please","which","with"}

def terms(text):
    return [t for t in re.findall(r"[A-Za-z0-9]+", text.casefold()) if t not in STOP]

RULES = [
    {"if_all": ["university", "campus"], "then": "The document identifies an institution and provides campus-related information."},
    {"if_all": ["solar", "planet"], "then": "The Solar System includes the Sun and objects that orbit it, including planets."}
]

def answer_question(question, kb):
    qterms = set(terms(question))
    scored = []
    for fact in kb:
        fterms = set(fact["terms"])
        overlap = len(qterms & fterms)
        score = overlap / max(1, len(qterms))
        if overlap:
            scored.append((score, overlap, fact["text"]))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    evidence = [x[2] for x in scored[:3] if x[0] >= 0.20]
    confidence = min(1.0, scored[0][0]) if scored else 0.0

    # Forward chaining: derive a conclusion only when every premise term is present
    # in the retrieved evidence set. Conclusions are explicitly labelled as inferences.
    combined = " ".join(evidence).casefold()
    inferred = []
    for rule in RULES:
        if all(premise in combined for premise in rule["if_all"]):
            inferred.append(rule["then"])
    if evidence:
        answer = evidence[0]
        method = "Lexical search + evidence ranking"
        if inferred:
            answer += " Rule-based inference: " + inferred[0]
            method += " + forward chaining"
    elif inferred:
        answer = inferred[0]
        method = "Forward chaining"
        confidence = 0.35
    else:
        answer = "The uploaded knowledge base does not contain enough matching evidence to answer this question."
        method = "Abstention (insufficient evidence)"
    return {"answer": answer, "evidence": evidence, "confidence": confidence, "method": method}
