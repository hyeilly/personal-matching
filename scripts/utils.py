import re

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