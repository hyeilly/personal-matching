from sentence_transformers import SentenceTransformer

class Embedding:
    _model = None

    @staticmethod
    def get_model():
        if Embedding._model is None:
            Embedding._model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # 한글 지원 모델
        return Embedding._model

    @staticmethod
    def embed_text(text: str):
        model = Embedding.get_model()
        return model.encode(text, convert_to_numpy=True)