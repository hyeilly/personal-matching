import os
import argparse
from services.llm_recommender import LLMRecommender
from dotenv import load_dotenv

load_dotenv()

# MongoDB settings
MONGO_DB_NAME = os.getenv("MONGODB_NAME", "test")
MONGO_DB_COLLECTION = os.getenv("MONGODB_COLLECTION_RECOMMEND", "recommend_contents")

def main():
    parser = argparse.ArgumentParser(description="Search and Recommend CLI")
    parser.add_argument("query", type=str, help="Query string for recommendation")
    parser.add_argument("--top_n", type=int, default=5, help="Number of top recommendations to return")
    args = parser.parse_args()

    service = LLMRecommender(db_name=MONGO_DB_NAME, collection_name=MONGO_DB_COLLECTION)
    recommendations = service.recommend(query=args.query, top_n=args.top_n)
    print(f"추천 문장: '{args.query}':")

    for idx, (item_id, similarity) in enumerate(recommendations, start=1):
        print(f"{idx}. Item ID: {item_id}, Similarity: {similarity:.4f}")

if __name__ == "__main__":
    main()
