from config.db import MongoDB
from scripts.utils import *
import numpy as np
from datetime import datetime

def fetch_data_from_mongo(source_db_name, source_collection_name, query=None):
    query = query or {}
    with MongoDB(db_name=source_db_name) as db_client:
        collection = db_client[source_collection_name]
        results = collection.find(query, {'articleId': 1, 'contents': 1, 'svcUrl': 1, 'tags': 1, 'reporters': 1, 'sections': 1})
        limit_results = results.limit(30)
        documents = list(limit_results)
    return documents

def fetch_user_data_from_mongo(source_db_name, source_collection_name, query=None):
    query = query or {}
    with MongoDB(db_name=source_db_name) as db_client:
        collection = db_client[source_collection_name]
        results = collection.find(query, {'h_id':1, 'h_id_media':1, 'tags.id': 1, 'tags.media': 1, 'scraps.id': 1, 'scraps.media': 1, 'reporters.id': 1})
        limit_results = results.sort("created_at", -1).limit(300)
        documents = list(limit_results)
    return documents

def transform_data(raw_data):
    transformed = []
    for data in raw_data:
        contents_data = data.get("contents", [])
        replace_contents = clean_text(contents_data.get("body", "no contents"))

        transformed.append({
            "id": data.get("articleId", 0),
            "title": contents_data.get("title", "Untitled"),
            "content": replace_contents,
            "source": data.get("svcUrl", ""),
            "updated_at": datetime.now()
        })
    return transformed

def transform_user_data(raw_data):
    transformed = []
    for data in raw_data:
        h_id_media = data.get("h_id_media", None)
        scraps_list = reformat_subscribe_array_data(data.get("scraps", []))
        search_article_list = search_article_list_from_mongo(scraps_list)
        section_list = reformat_section_array_data(search_article_list)
        section_list = [item[0] for item in section_list]
        transformed.append({
            "h_id": data.get("h_id", None),
            "tags": reformat_subscribe_array_data(data.get("tags", [])),
            "reporters": reformat_subscribe_array_data(data.get("reporters", [])),
            "sections": section_list
        })
    return transformed

def convert_numpy_to_list(df):
    for column in df.columns:
        if isinstance(df[column].iloc[0], np.ndarray):
            df[column] = df[column].apply(lambda x: x.tolist())
    return df

def save_to_mongo(target_db_name, target_collection_name, data):
    if not data:
        print("No data to insert.")
        return
    with MongoDB(db_name=target_db_name) as db_client:
        collection = db_client[target_collection_name]
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into '{target_collection_name}' collection.")

def delete_all_from_mongo(target_db_name, target_collection_name):
    with MongoDB(db_name=target_db_name) as db_client:
        collection = db_client[target_collection_name]
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from '{target_collection_name}' collection.")
