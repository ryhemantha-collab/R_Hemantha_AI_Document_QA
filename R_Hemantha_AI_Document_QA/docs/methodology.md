# Methodology and design rationale

## 1. Document processing
The uploaded file is decoded or read using a format-specific parser. Text is split at punctuation boundaries and line breaks. Each non-trivial unique segment becomes a knowledge record with an identifier, original text, and a list of lowercase alphanumeric terms.

## 2. Knowledge representation
Each record is represented as `{id, text, terms}`. This lightweight fact representation preserves the source statement and supports inspection. A term-to-record inverted index is conceptually suitable for scaling; this prototype directly scores term overlap over the stored records for clarity.

## 3. Question processing and reasoning
Question terms are extracted by a simple regular expression. A small stop-word list removes common question words. Each fact is scored using the proportion of question terms that overlap the fact terms. The top evidence statements are selected above a threshold. Explicit IF–THEN rules are checked against the retrieved evidence to demonstrate forward chaining. This is deterministic symbolic/lexical processing, not an NLP pipeline.

## 4. Answer generation
The top-ranked evidence statement is returned verbatim, optionally accompanied by a labelled rule conclusion. If no statement reaches the evidence threshold, the system abstains rather than inventing an answer.

## 5. Evaluation
A fixed benchmark CSV contains questions and expected terms. The evaluator measures expected-term coverage (recall), a token-set precision estimate, F1, and overall pass rate. These are simple reproducible metrics; they do not replace expert assessment of factual correctness or answer fluency.

## Limitations
- Lexical overlap may miss paraphrases and synonyms.
- Sentence segmentation can be imperfect for abbreviations and complex layouts.
- PDF extraction quality depends on whether the PDF contains selectable text.
- The sample corpus is illustrative; users should upload the exact source document relevant to their task.
- The evaluation metrics are lightweight and should be interpreted with these limitations.
