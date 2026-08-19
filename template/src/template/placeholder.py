# TODO: Replace with the generated graph.py. Need to change path in langgraph.json

from langchain_core.messages import AIMessage
from langgraph.config import get_stream_writer
from langgraph.graph import END, START, MessagesState, StateGraph


def update_step(name: str, icon: str):
    writer = get_stream_writer()

    writer(
        {
            "name": name,
            "icon": icon,  # ["hourglass", "search", "rocket", "pencil-line"]
        }
    )


# LangGraph
def fake_llm(state: MessagesState):
    update_step(
        "Writing...",
        "pencil-line",
    )

    response = (
        "This is a fake LLM response. "
        "It is used to test the functionality of the graph, "
        "the streaming of tokens and the display in Chainlit."
    )

    # Simulation de génération token par token
    return {"messages": [AIMessage(content=response)]}


graph = StateGraph(MessagesState)

graph.add_node("fake", fake_llm)

graph.add_edge(START, "fake")
graph.add_edge("fake", END)

agent_graph = graph.compile()
