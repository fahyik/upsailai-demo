# app/chains/sale_assistant_chain.py

from chains.models.suggestions import ProductSuggestions
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


def build_sale_assistant_chain(llm: ChatOpenAI):
    output_parser = JsonOutputParser(pydantic_object=ProductSuggestions)
    template = """
    You are a sales assistant for Vanessa-Bruno.

    {format_instructions}

    Context:
    {context}

    Question: {question}

    Helpful Answer:
    """

    prompt = PromptTemplate.from_template(template).partial(
        format_instructions=output_parser.get_format_instructions()
    )

    chain = prompt | llm | output_parser
    return chain
