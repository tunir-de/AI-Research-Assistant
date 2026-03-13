import matplotlib.pyplot as plt
import networkx as nx

def plot_paper_graph(graph):

    fig = plt.figure(figsize=(8,6))

    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=800,
        font_size=10,
        edge_color="gray"
    )

    plt.title("Research Paper Similarity Graph")

    return fig