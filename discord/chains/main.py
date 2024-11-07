# import base64
# import json
import os

# from langchain_openai import ChatOpenAI

# from chains.chain import load_retriever, build_stylist_chain

# os.environ["OPENAI_API_KEY"] = "sk-proj-bPZqEs92C38iN9sUNTWBT3BlbkFJARac9Feph9oJlZLe4JUt"

import json

from chains.chain_manager import ChainManager

if __name__ == "__main__":

    manager = ChainManager(
        persist_directory=os.environ["DB_PATH"],
        docstore_path=os.environ["DOC_STORE_PATH"],
        openai_token=os.environ["OPENAI_API_KEY"],
    )

    docs = manager.retriever.invoke("blue boots")

    product = json.loads(docs[0].page_content)

    print(json.dumps(product, indent=2))

#     llm_4o = ChatOpenAI(model="gpt-4o")
#     stylist_chain = build_stylist_chain(llm_4o)
#     retriever = load_retriever(
#         persist_directory="/Users/szhang/workspace/personal/upsail-demo/discord/data/chroma_db",
#         docstore_path="/Users/szhang/workspace/personal/upsail-demo/discord/data/doc_store"
#     )

#     with open('/Users/szhang/workspace/personal/upsail-demo/clothe.jpg', 'rb') as fh:
#         base64_encoded_image = base64.b64encode(fh.read()).decode('utf-8')
#     image_data = "data:image/jpeg;base64,%s" % base64_encoded_image

#     style_suggestions = stylist_chain.invoke({"image_url": image_data})
#     products = {}
#     for query in style_suggestions['clothes']:
#         docs = retriever.invoke(query)
#         for doc in docs:
#             product = json.loads(doc.page_content)
#             products[product['url']] = product

#     len(products)

#     # rag = build_openai_chain(
#     #     "/Users/szhang/workspace/personal/upsail-demo/discord/data/chroma_db",
#     #     "/Users/szhang/workspace/personal/upsail-demo/discord/data/doc_store",
#     #     "sk-proj-bPZqEs92C38iN9sUNTWBT3BlbkFJARac9Feph9oJlZLe4JUt",
#     # )
#     # print(rag.invoke("White high-waisted trousers with a straight cut for a clean contrast"))
