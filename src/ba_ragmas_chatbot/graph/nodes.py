from langchain_core.messages import SystemMessage, HumanMessage
from ba_ragmas_chatbot.graph.state import AgentState
from ba_ragmas_chatbot.llm.factory import get_llm_for_agent
from ba_ragmas_chatbot.graph.utils import get_agent_config, get_task_config
from ba_ragmas_chatbot.tools.vectorstore import get_retriever
from ba_ragmas_chatbot.tools.search_tool import perform_web_search


def research_node(state: AgentState):
    """
    Fetches context from the vector store (if docs exist) and generates bullet points.
    """
    print("Researcher is working...")

    agent_cfg = get_agent_config("researcher")
    task_cfg = get_task_config("research_task")

    context_text = "No documents provided."
    retriever = get_retriever(k=4)

    if retriever and state.get("source_documents"):

        print(f"📚 Retrieving context for topic: {state['topic']}")
        try:
            docs = retriever.invoke(state["topic"])
            context_text = "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            print(f"⚠️ Retrieval failed: {e}")

    system_prompt = agent_cfg["role"].format(
        topic=state["topic"], language=state["language"]
    )
    system_prompt += (
        f"\n\nBackstory: {agent_cfg['backstory'].format(topic=state['topic'])}"
    )

    user_prompt = task_cfg["description"].format(topic=state["topic"])
    user_prompt += f"\n\nCONTEXT FROM DOCUMENTS:\n{context_text}"
    user_prompt += f"\n\nEXPECTED OUTPUT:\n{task_cfg['expected_output'].format(topic=state['topic'], language=state['language'])}"

    llm = get_llm_for_agent("researcher")
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    return {
        "research_data": [response.content],
        "current_status": "Research completed.",
    }


def editor_node(state: AgentState):
    """
    Creates an outline based on the research data.
    """
    print("Editor is working...")

    agent_cfg = get_agent_config("editor")
    task_cfg = get_task_config("editor_task")

    research_summary = "\n".join(state.get("research_data", []))
    history_str = (
        "\n".join(state.get("history", [])) if state.get("history") else "None"
    )

    system_prompt = agent_cfg["role"].format(
        topic=state["topic"], language=state["language"]
    )

    user_prompt = task_cfg["description"].format(
        topic=state["topic"],
        length=state["target_len"],
        information_level=state["target_audience"],
        language_level=state["target_audience"],
        tone=state["tone"],
        language=state["language"],
        additional_information=state["additional_info"],
        history=history_str,
    )
    user_prompt += f"\n\nRESEARCH MATERIAL:\n{research_summary}"
    user_prompt += f"\n\nEXPECTED OUTPUT:\n{task_cfg['expected_output'].format(topic=state['topic'], language=state['language'])}"

    llm = get_llm_for_agent("editor")
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    return {"outline": [response.content], "current_status": "Outline created."}


def writer_node(state: AgentState):
    """
    Writes the text based on the outline.
    """
    print("Writer is working...")

    agent_cfg = get_agent_config("writer")
    task_cfg = get_task_config("writer_task")

    outline_str = "\n".join(state.get("outline", []))
    history_str = (
        "\n".join(state.get("history", [])) if state.get("history") else "None"
    )

    system_prompt = agent_cfg["role"].format(
        topic=state["topic"], language=state["language"]
    )

    user_prompt = task_cfg["description"].format(
        topic=state["topic"],
        length=state["target_len"],
        information_level=state["target_audience"],
        language_level=state["target_audience"],
        tone=state["tone"],
        language=state["language"],
        additional_information=state["additional_info"],
        history=history_str,
    )
    user_prompt += f"\n\nOUTLINE TO FOLLOW:\n{outline_str}"

    llm = get_llm_for_agent("writer")
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    return {"draft": response.content, "current_status": "Draft written."}


def proofreader_node(state: AgentState):
    """
    Checks facts and language.
    """
    print("Proofreader is working...")

    agent_cfg = get_agent_config("proofreader")
    task_cfg = get_task_config("proofreader_task")

    draft_text = state.get("draft", "")
    history_str = (
        "\n".join(state.get("history", [])) if state.get("history") else "None"
    )

    web_results = perform_web_search(state["topic"], max_results=3)
    web_context = "\n".join([f"- {r['title']}: {r['body']}" for r in web_results])

    system_prompt = agent_cfg["role"].format(
        topic=state["topic"], language=state["language"]
    )

    user_prompt = task_cfg["description"].format(
        topic=state["topic"],
        length=state["target_len"],
        information_level=state["target_audience"],
        language_level=state["target_audience"],
        tone=state["tone"],
        language=state["language"],
        additional_information=state["additional_info"],
        history=history_str,
    )
    user_prompt += f"\n\nDRAFT TO REVIEW:\n{draft_text}"
    user_prompt += f"\n\nLATEST WEB FACTS (Verification):\n{web_context}"

    llm = get_llm_for_agent("proofreader")
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    return {
        "final_article": response.content,
        "current_status": "Proofreading finished.",
    }
