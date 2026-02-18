from langchain_ollama import ChatOllama

LOGIC_MODEL = "qwen2.5:7b-instruct-q5_k_m"
CREATIVE_MODEL = "gemma2:9b-instruct-q5_k_m"
BASE_URL = "http://localhost:11434"


def get_llm_for_agent(agent_name: str, temperature: float = 0.7):
    """
    Returns the specialized LLM instance for a specific agent.
    """

    if agent_name == "researcher":
        return ChatOllama(
            model=LOGIC_MODEL, base_url=BASE_URL, temperature=0.0, keep_alive=0
        )

    elif agent_name == "editor":
        return ChatOllama(
            model=LOGIC_MODEL, base_url=BASE_URL, temperature=0.2, keep_alive=0
        )

    elif agent_name == "writer":
        return ChatOllama(
            model=CREATIVE_MODEL, base_url=BASE_URL, temperature=0.7, keep_alive=0
        )

    elif agent_name == "fact_checker":
        return ChatOllama(
            model=LOGIC_MODEL, base_url=BASE_URL, temperature=0.0, keep_alive=0
        )

    elif agent_name == "polisher":
        return ChatOllama(
            model=CREATIVE_MODEL, base_url=BASE_URL, temperature=0.6, keep_alive=0
        )

    return ChatOllama(
        model=LOGIC_MODEL, base_url=BASE_URL, temperature=temperature, keep_alive=0
    )
