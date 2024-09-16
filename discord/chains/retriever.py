# app/chains/retriever.py

from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore

from chains.modules.embeddings import CLIPEmbeddings
from chains.modules.splitter import ProductDocumentSplitter
from chains.modules.vectorstore import MultiModalChroma


def load_retriever(persist_directory, docstore_path):
    child_splitter = ProductDocumentSplitter()
    vectorstore = MultiModalChroma(
        collection_name="full_documents",
        embedding_function=CLIPEmbeddings(),
        persist_directory=persist_directory,
    )

    fs = LocalFileStore(docstore_path)
    store = create_kv_docstore(fs)

    return ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        search_kwargs={"k": 10},
    )
