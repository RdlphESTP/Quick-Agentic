from langgraph.config import get_stream_writer
from langgraph.graph import END, START, MessagesState, StateGraph

from template.nodes.fake_llm import fake_llm


def update_step(name: str, icon: str):
    writer = get_stream_writer()

    writer(
        {
            "name": name,
            "icon": icon,
        }
    )


def with_step(func, name: str, icon: str):
    def wrapper(state):
        update_step(name, icon)
        return func(state)

    return wrapper


graph = StateGraph(MessagesState)

graph.add_node('fake_llm', with_step(fake_llm, 'Writing...', 'pencil-line'))

graph.add_edge(START, 'fake_llm')
graph.add_edge('fake_llm', END)

agent_graph = graph.compile()
