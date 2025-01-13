import re
from config.db import MongoDB

def clean_text(raw_text):
    cleaned_text = re.sub(r'\[\%\%[A-Z]+\d+\%\%\]', '', raw_text)
    cleaned_text = re.sub(r'<[^>]*>', '', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

def reformat_array_data(input_array):
    output_array = []
    for item in input_array:
        output_array.append({
            'type_id': item.get("name"),
            'type_value': item.get("value")
        })
    return output_array

def reformat_subscribe_array_data(input_array):
    output_array = []
    for item in input_array:
        if item.get("media") != "news":
            continue
        output_array.append(item.get("id", None))
    return output_array


def get_first_parent_code(data):
    result = []
    for item in data:
        if "parent_info" in item and item["parent_info"]:
            first_parent = item["parent_info"][0]
            if "section_code" in first_parent:
                result.append(first_parent["section_code"])
    return result

def reformat_section_array_data(input_array):
    output_array = []
    for item in input_array:
        section_list = get_first_parent_code(item.get('sections', []))
        output_array.append(section_list)
    return output_array

def search_article_list_from_mongo(article_list=[]):
    subscribe_article_db = "subscr_renew"
    subscribe_article_collection = "articles"
    with MongoDB(db_name=subscribe_article_db) as db_client:
        collection = db_client[subscribe_article_collection]
        results = collection.find({"articleId":{"$in":article_list}}, {'articleId': 1, 'sections': 1})
        documents = list(results)
    return documents