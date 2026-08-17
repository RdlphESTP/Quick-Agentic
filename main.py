import json

from quick_agentic.generate_code import generate_code

with open("user_graph.json", "r") as f:
    user_graph = json.load(f)

# print(json.dumps(user_graph, indent=4, ensure_ascii=False))

print(generate_code(user_graph))
