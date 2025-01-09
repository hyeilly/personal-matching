from config.db import MongoDB

def fetch_data_from_mongo(source_db_name, source_collection_name, query=None):
    query = query or {}
    with MongoDB(db_name=source_db_name) as db_client:
        collection = db_client[source_collection_name]
        results = collection.find(query, {'articleId': 1, 'contents': 1, 'tags': 1, 'reporters': 1, 'sections': 1})
        limit_results = results.limit(1)
        documents = list(limit_results)
    return documents

def transform_data(raw_data):
    transformed = []
    for item in raw_data:
        transformed.append({
            "title": item.get("title", "Untitled"),
            "content": item.get("content", ""),
            "author": item.get("author", "Unknown"),
            "tags": item.get("tags", []),
            "source_db_id": str(item.get("_id")),  # Track the original document ID
            "created_at": item.get("created_at")
        })
    return transformed


def save_to_mongo(target_db_name, target_collection_name, data):
    if not data:
        print("No data to insert.")
        return

    with MongoDB(db_name=target_db_name) as db_client:
        collection = db_client[target_collection_name]
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into '{target_collection_name}' collection.")