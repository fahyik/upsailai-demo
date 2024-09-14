import json
from typing import List

from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from .module.embeddings import CLIPEmbeddings
from .module.splitter import ProductDocumentSplitter
from .module.vectorstore import MultiModalChroma

from .util import product_to_string


class StyleSuggestion(BaseModel):
    style: str = Field(description="A name of suggested style")
    description: str = Field(description="explanation of the style and why the suggested clothes match")
    target_cloth: str = Field(description="The description of the cloth provided by user.")
    clothes: List[str] = Field(description="list of short description of the clothes to be used as a query")


class ProductSuggestion(BaseModel):
    name: str = Field(description="The name of the product")
    url: str = Field(description="the url of the product")
    description: str = Field(description="Why this product can match user's clothes")



def load_retriever(persist_directory, docstore_path):
    child_splitter = ProductDocumentSplitter()
    vectorstore = MultiModalChroma(
        collection_name="full_documents",
        embedding_function=CLIPEmbeddings(),
        persist_directory=persist_directory,
    )

    # The storage layer for the parent documents
    fs = LocalFileStore(docstore_path)
    store = create_kv_docstore(fs)

    return ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        search_kwargs={"k": 10},
    )


def format_docs(docs):
    print("getting %s docs" % len(docs))
    product_strs = [
        product_to_string(json.loads(doc.page_content))
        for doc in docs
    ]
    return "\n\n".join(product_strs)


def build_stylist_chain(llm):
    style_output_parser = JsonOutputParser(pydantic_object=StyleSuggestion)

    system_prompt = """
        You are a fashion stylist. Your task is to suggest matching clothes based on either a photo or a description provided by the user, aligning with their preferences. Follow these steps:

            1.	If the user specifies a style, incorporate this style when recommending matching clothes. If no style is provided, suggest the best matching style based on the given clothes and the user’s potential preferences.
            2.	Briefly describe each recommended piece of clothing in a short sentence, as these descriptions will be used as queries in a Retrieval-Augmented Generation (RAG) system.
            3.	Provide a concise explanation of the overall style that the recommended outfit would create, including the reason for choosing the matching clothes.

        This version emphasizes clarity and structure for easy processing in your RAG system.

        Answer the user query.
        {format_instructions}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "user",
                [
                    {
                        "type": "image_url",
                        "image_url": {"url": "{image_url}"},
                    }
                ],
            ),
        ]
    ).partial(format_instructions = style_output_parser.get_format_instructions())

    chain = (
        prompt
        | llm
        | style_output_parser
    )

    return chain


def build_chain(retriever, llm):

    template = """
    You are a sales assistant for Vanessa-Bruno.
    Use the provided context, which includes details about products the customer may be interested in,
    to answer their question or offer a product recommendation.
    If you are unsure of the answer, simply state that you don't know—avoid guessing.
    Please give multiple choices to the user.
    Keeping your reply concise.

    {context}

    Question: {question}

    Helpful Answer:"""

    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | StrOutputParser()
    )

    return rag_chain

def build_openai_chain(persist_directory, docstore_path, openai_key):
    retriever = load_retriever(
        persist_directory=persist_directory,
        docstore_path=docstore_path
    )
    import os

    os.environ["OPENAI_API_KEY"] = openai_key

    llm = ChatOpenAI(model="gpt-4o-mini")

    rag_chain = build_chain(retriever, llm)

    return rag_chain
