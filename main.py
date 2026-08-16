import json

with open("user_graph.json", "r") as f:
    user_graph = json.load(f)

# print(json.dumps(user_graph, indent=4, ensure_ascii=False))


def generate_app(graph: dict) -> str:
    imports = ["from langgraph.graph import END, START, MessagesState, StateGraph"]
    commands = ["graph = StateGraph(MessagesState)\n"]

    for node in graph["nodes"]:
        node_id = node["id"]
        imports.append(f"from nodes.{node_id} import {node_id}")
        commands.append(f"graph.add_node('{node_id}', {node_id})")

    commands.append("")  # Add a blank line for readability

    for edge in graph["edges"]:
        source = edge["source"] if edge["source"] == "START" else f"'{edge['source']}'"
        target = edge["target"] if edge["target"] == "END" else f"'{edge['target']}'"
        commands.append(f"graph.add_edge({source}, {target})")

    commands.append("\ngraph = graph.compile()\n")

    return "\n".join(imports) + "\n\n" + "\n".join(commands)


print(generate_app(user_graph))

# INPUT
# graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})  # type: ignore
