from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import GROQ_API_KEY, MODEL_NAME


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=GROQ_API_KEY,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0.3,
        max_tokens=600,
    )


def call_llm(system: str, history: list) -> str:
    try:
        llm = get_llm()
        messages = [SystemMessage(content=system)]
        for message in history[-10:]:
            if message["role"] == "user":
                messages.append(HumanMessage(content=message["content"]))
            elif message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"]))
        return llm.invoke(messages).content
    except Exception as exc:  # noqa: BLE001 - surface any LLM/API failure to the UI
        return f"Error: {exc}"

