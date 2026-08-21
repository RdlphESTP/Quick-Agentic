from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState


def fake_llm(state: MessagesState):
    response = (
        "This is a fake LLM response. "
        "It is used to test the functionality of the graph, "
        "the streaming of tokens and the display in Chainlit."
    )
    return {"messages": [AIMessage(content=response)]}
