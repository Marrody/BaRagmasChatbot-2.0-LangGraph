from langgraph.graph import StateGraph, START, END
from ba_ragmas_chatbot.graph.state import AgentState
from ba_ragmas_chatbot.graph.nodes import (
    research_node,
    editor_node,
    writer_node,
    proofreader_node,
)


def create_graph():
    """
    Constructs the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("researcher", research_node)
    workflow.add_node("editor", editor_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("proofreader", proofreader_node)

    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "editor")
    workflow.add_edge("editor", "writer")
    workflow.add_edge("writer", "proofreader")
    workflow.add_edge("proofreader", END)

    app = workflow.compile()
    return app
