import unittest
from document_processor import build_knowledge_base, extract_text
from reasoning_engine import answer_question

class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.kb = build_knowledge_base("Ramaiah University is located in Bengaluru, India. Eight planets orbit the Sun.")
    def test_sentence_extraction(self):
        self.assertEqual(len(self.kb), 2)
    def test_retrieval_finds_location(self):
        result = answer_question("Where is the university located?", self.kb)
        self.assertIn("Bengaluru", result["answer"])
    def test_abstains_when_unknown(self):
        result = answer_question("What is the capital of France?", self.kb)
        self.assertIn("not contain enough", result["answer"])
    def test_text_extraction(self):
        self.assertIn("hello", extract_text(b"hello world", "note.txt"))
    def test_duplicate_removal(self):
        self.assertEqual(len(build_knowledge_base("Repeated sentence here. Repeated sentence here.")), 1)

if __name__ == "__main__":
    unittest.main()
