import numpy as np
from config.db import MongoDB
from config.embedding import Embedding

class LLMRecommender:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.collection = None

    def embed_query(self, query: str) -> np.ndarray:
        return Embedding.embed_text(query)

    def find_similar_items(self, query_vector: np.ndarray, top_n: int = 5):
        with MongoDB(self.db_name) as db:
            self.collection = db[self.collection_name]
            all_items = list(self.collection.find({}))
        results = []
        for item in all_items:
            item_vector = np.array(item['embedding'])
            similarity = self._calculate_cosine_similarity(query_vector, item_vector)
            results.append((item['id'], similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]

    @staticmethod
    def _calculate_cosine_similarity(vec1, vec2):
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = sum(a * a for a in vec1) ** 0.5
        norm_b = sum(b * b for b in vec2) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def recommend(self, query: str, top_n: int = 5):
        query_vector = self.embed_query(query)
        return self.find_similar_items(query_vector, top_n=top_n)