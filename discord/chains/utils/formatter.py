# app/utils/formatter.py

import json
from .util import product_to_string

def format_docs(docs):
    print(f"Getting {len(docs)} docs")
    product_strs = [product_to_string(json.loads(doc.page_content)) for doc in docs]
    return "\n\n".join(product_strs)
