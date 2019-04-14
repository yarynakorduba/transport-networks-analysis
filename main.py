from GraphSpaces import GraphSpaces
from NetworkFeatures import NetworkFeatures
from Visualization import display_graph

dataset = init_dataset = "./data/bristol_parsed/processed/bristolStopsBusProcessed.json"
bristol_space = GraphSpaces(dataset, init_dataset)
space = "l"
bristol_graph = bristol_space.get_graph(space)
bristol_features = NetworkFeatures(bristol_graph)
print(bristol_graph.nodes, bristol_graph.edges)
display_graph(bristol_graph)