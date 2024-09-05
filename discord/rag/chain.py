import json

from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from .module.embeddings import CLIPEmbeddings
from .module.splitter import ProductDocumentSplitter
from .module.vectorstore import MultiModalChroma

from .util import product_to_string


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
        | llm
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
