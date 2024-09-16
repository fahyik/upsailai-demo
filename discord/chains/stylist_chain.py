# app/chains/stylist_chain.py

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from chains.models.suggestions import StyleSuggestion


def build_stylist_chain(llm, with_image=True):
    style_output_parser = JsonOutputParser(pydantic_object=StyleSuggestion)
    system_prompt = """
    You are a fashion stylist. Your task is to suggest matching clothes based on either a photo or a description provided by the user, aligning with their preferences.

    {format_instructions}
    """

    messages = [
        {"type": "text", "text": "{user_query}"},
    ]
    if with_image:
        messages.append({"type": "image_url", "image_url": {"url": "{image_url}"}})

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", messages),
    ]).partial(format_instructions=style_output_parser.get_format_instructions())

    chain = prompt | llm | style_output_parser
    return chain
