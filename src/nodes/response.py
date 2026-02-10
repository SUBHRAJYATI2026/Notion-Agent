import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import State
from src.templates.template import markdown_template

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

prompt = ChatPromptTemplate.from_template(template=markdown_template)


def node(state: State) -> State:
    model = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
    prompt_value = prompt.invoke({"message": state["message"]})
    result = model.invoke(prompt_value).content
    return {"message": result}


