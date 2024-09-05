from rag.chain import build_openai_chain


if __name__ == "__main__":
    rag = build_openai_chain(
        "/Users/szhang/workspace/personal/upsail-demo/discord/data/chroma_db",
        "/Users/szhang/workspace/personal/upsail-demo/discord/data/doc_store",
        "sk-proj-bPZqEs92C38iN9sUNTWBT3BlbkFJARac9Feph9oJlZLe4JUt",
    )
    print(rag.invoke("What's the best blue skirt for a wedding ?"))

