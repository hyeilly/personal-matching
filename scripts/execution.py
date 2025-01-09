from scripts.data_processing import *
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB settings
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGODB_NAME", "test")

def run_etl_pipeline(source_db_name, source_collection_name, target_db_name, target_collection_name, query=None):

    print("Extract")
    raw_data = fetch_data_from_mongo(source_db_name, source_collection_name, query)
    print(raw_data)

    # print("Transforming data...")
    # transformed_data = transform_data(raw_data)
    #
    # print("Loading data into target MongoDB...")
    # save_to_mongo(target_db_name, target_collection_name, transformed_data)
    #
    # print("ETL pipeline completed.")

if __name__ == "__main__":
    SOURCE_DB = "newsapp_renew"
    SOURCE_COLLECTION = "articles"
    TARGET_DB = MONGO_DB_NAME
    TARGET_COLLECTION = "recommend_contents"
    QUERY = {"articleId": {"$gt": 1026601}}

    run_etl_pipeline(SOURCE_DB, SOURCE_COLLECTION, TARGET_DB, TARGET_COLLECTION, QUERY)
