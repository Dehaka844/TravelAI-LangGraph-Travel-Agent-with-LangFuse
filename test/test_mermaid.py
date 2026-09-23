from src.graph.graph import app


mermaid = app.get_graph().draw_mermaid()

print("=" * 70)
print("DIAGRAMA MERMAID")
print("=" * 70)
print(mermaid)