def generate_code(graph: dict) -> str:
    """
    Generate the Python script for creating a langgraph based on the provided user_graph.

    Args:
        graph (dict): The JSON graph to be converted.

    Returns:
        str: The generated Python script.

    Example:
    .. code-block:: json
        graph = {
            "nodes": [
                {"id": "NodeA"},
                {"id": "NodeB"}
            ],
            "edges": [
                {"source": "START", "target": "NodeA"},
                {"source": "NodeA", "target": "NodeB"},
                {"source": "NodeB", "target": "END"}
            ]
        }
    """

    # ========== Initial setup ==========
    imports = [
        "from langgraph.config import get_stream_writer",
        "from langgraph.graph import END, START, MessagesState, StateGraph",
    ]
    commands = [
        """
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

    return wrapper\n\n""",
        "graph = StateGraph(MessagesState)\n",
    ]

    # ========== Populate the nodes ==========
    for node in graph["nodes"]:
        node_id = node["id"]

        # Add the imports for the node
        imports.append(f"from template.nodes.{node_id} import {node_id}")

        # Add the nodes to the graph accounting for the step name and icon if they exist
        name = node.get("step")
        icon = node.get("icon")

        if name and icon:
            commands.append(
                f"graph.add_node('{node_id}', with_step({node_id}, '{name}', '{icon}'))"
            )
        else:
            commands.append(f"graph.add_node('{node_id}', {node_id})")

    commands.append("")

    # ========== Populate the edges ==========
    for edge in graph["edges"]:
        source = edge["source"] if edge["source"] == "START" else f"'{edge['source']}'"
        target = edge["target"] if edge["target"] == "END" else f"'{edge['target']}'"
        commands.append(f"graph.add_edge({source}, {target})")

    commands.append("\nagent_graph = graph.compile()\n")

    return "\n".join(imports) + "\n\n" + "\n".join(commands)
