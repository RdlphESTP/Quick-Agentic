def generate_code(graph: dict) -> str:
    """
    Generate the Python script for creating a langgraph based on the provided graph.

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
    imports = ["from langgraph.graph import END, START, MessagesState, StateGraph"]
    commands = ["graph = StateGraph(MessagesState)\n"]

    for node in graph["nodes"]:
        node_id = node["id"]
        imports.append(f"from nodes.{node_id} import {node_id}")
        commands.append(f"graph.add_node('{node_id}', {node_id})")

    commands.append("")

    for edge in graph["edges"]:
        source = edge["source"] if edge["source"] == "START" else f"'{edge['source']}'"
        target = edge["target"] if edge["target"] == "END" else f"'{edge['target']}'"
        commands.append(f"graph.add_edge({source}, {target})")

    commands.append("\ngraph = graph.compile()\n")

    return "\n".join(imports) + "\n\n" + "\n".join(commands)
