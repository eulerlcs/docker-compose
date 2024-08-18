from prompt_template import system_template_text, user_template_text
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from xiaohongshu_model import Xiaohongshu


def generate_xiaohongshu(theme, openai_api_key):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])

    model="gpt-4o-2024-08-06"
    model="gpt-4o-mini"

    llm = ChatOpenAI(model=model, api_key=openai_api_key)
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)
    chain = prompt | llm | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme
    })
    return result

# import os

# result = generate_xiaohongshu("大模型", os.getenv("OPENAI_API_KEY"))
# print(result)
