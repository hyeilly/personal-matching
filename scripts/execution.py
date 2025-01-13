from scripts.data_processing import *
import os
from dotenv import load_dotenv

from config.embedding import *
import pandas as pd

load_dotenv()

# MongoDB settings
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGODB_NAME", "test")
MONGO_DB_COLLECTION = os.getenv("MONGODB_COLLECTION_RECOMMEND", "recommend_contents")

def run_etl_pipeline(source_db_name, source_collection_name, target_db_name, target_collection_name, query=None):

    print("Extract")
    raw_data = fetch_data_from_mongo(source_db_name, source_collection_name, query)
    print("Transforming data...")
    transformed_data = transform_data(raw_data)

    for article in transformed_data:
        article['embedding'] = Embedding.embed_text(article['content'])
    df = pd.DataFrame(transformed_data)
    replace_df = convert_numpy_to_list(df)
    input_data = replace_df.to_dict(orient='records')

    save_to_mongo(target_db_name, target_collection_name, input_data)
    print("ETL pipeline completed.")

def run_etl_user_pipeline(source_db_name, source_collection_name, target_db_name, target_collection_name, query=None):
    print("Extract")
    raw_data = fetch_user_data_from_mongo(source_db_name, source_collection_name, query)
    print("Transforming data...")
    transformed_data = transform_user_data(raw_data)
    save_to_mongo(target_db_name, target_collection_name, transformed_data)
    print("ETL pipeline completed.")

if __name__ == "__main__":
    # SOURCE_DB = "newsapp_renew"
    # SOURCE_COLLECTION = "articles"
    # TARGET_DB = MONGO_DB_NAME
    # TARGET_COLLECTION = MONGO_DB_COLLECTION
    # QUERY = {"articleId": {"$gt": 1026601}}
    #
    # run_etl_pipeline(SOURCE_DB, SOURCE_COLLECTION, TARGET_DB, TARGET_COLLECTION, QUERY)
    SOURCE_DB = "subscr_renew"
    SOURCE_COLLECTION = "usersubscr"
    TARGET_DB = MONGO_DB_NAME
    TARGET_COLLECTION = os.getenv("MONGODB_COLLECTION_USER")
    QUERY = {}
    run_etl_user_pipeline(SOURCE_DB, SOURCE_COLLECTION, TARGET_DB, TARGET_COLLECTION, QUERY)