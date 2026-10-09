import numpy as np

class SimpleRAGStore:
    def __init__(self):
        self.chunks = []
        
    def add_document(self, doc_id, text):
        # Chunk text by paragraphs/sentences
        sentences = text.split("\n")
        for s in sentences:
            if len(s.strip()) > 10:
                self.chunks.append({"doc_id": doc_id, "text": s.strip()})
                
    def query(self, question):
        """Simple keyword-grounded search retrieval."""
        matches = []
        q_words = question.lower().split()
        for chunk in self.chunks:
            score = sum(1 for w in q_words if w in chunk["text"].lower())
            if score > 0:
                matches.append((score, chunk["text"]))
                
        matches.sort(key=lambda x: x[0], reverse=True)
        if matches:
            return matches[0][1]
        return "The available documents do not contain enough information to answer this question."

rag_engine = SimpleRAGStore()