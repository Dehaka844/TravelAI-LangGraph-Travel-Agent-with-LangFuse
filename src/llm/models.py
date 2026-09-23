from langchain_openai import ChatOpenAI

from src.config.settings import OPENAI_API_KEY


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)