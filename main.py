import csv
from GraphSpaces import GraphSpaces
from NetworkFeatures import NetworkFeatures

transport_type = "All"
space_name = "c"


lviv_stops_dataset = "./data/lviv_parsed/processed/lvivAllStopsProcessed40m.json"
lviv_routes_dataset = "./data/lviv_parsed/processed/lvivAllJourneysProcessed40m.json"
lviv_space = GraphSpaces(lviv_stops_dataset, lviv_routes_dataset)
lviv_graph = lviv_space.get_graph(space_name)
lviv_space_features = NetworkFeatures(lviv_graph)


bristol_stops_dataset = "./data/bristol_parsed/processed/bristolAllStopsProcessed40m.json"
bristol_routes_dataset = "./data/bristol_parsed/processed/bristolAllJourneysProcessed40m.json"
bristol_space = GraphSpaces(bristol_stops_dataset, bristol_routes_dataset)
bristol_graph = bristol_space.get_graph(space_name)
bristol_space_features = NetworkFeatures(bristol_graph)


with open("./results_clustered_at_40m/tables/general_topology_results.csv", "a+") as file:
    info_writer = csv.writer(file, delimiter=',', quotechar='"')
    info_writer.writerow(["space", "property", "lviv", "bristol"])
    info_writer.writerow([space_name, "nodes", round(lviv_space_features.number_of_nodes(), 3),\
                          round(bristol_space_features.number_of_nodes(), 3)])
    info_writer.writerow([space_name, "edges", round(lviv_space_features.number_of_edges(), 3), \
                          round(bristol_space_features.number_of_edges(), 3)])
    info_writer.writerow([space_name, "betweenness centrality", round(lviv_space_features.mean_betweenness_centrality(), 3), \
                          round(bristol_space_features.mean_betweenness_centrality(), 3)])
    info_writer.writerow([space_name, "assortativity", round(lviv_space_features.graph_assortativity(), 3), \
                          round(bristol_space_features.graph_assortativity(), 3)])
    info_writer.writerow([space_name, "clustering coefficient", round(lviv_space_features.mean_clustering_coefficient(), 3), \
                          round(bristol_space_features.mean_clustering_coefficient(), 3)])
    info_writer.writerow([space_name, "mean degree", round(lviv_space_features.mean_degree(), 3), \
                          round(bristol_space_features.mean_degree(), 3)])
    info_writer.writerow([space_name, "mean square degree", round(lviv_space_features.mean_square_degree(), 3), \
                          round(bristol_space_features.mean_square_degree(), 3)])
    info_writer.writerow([space_name, "max degree", round(lviv_space_features.max_degree(), 3), \
                          round(bristol_space_features.max_degree(), 3)])
    info_writer.writerow([space_name, "mean shortest path", round(lviv_space_features.mean_shortest_path(), 3), \
                          round(bristol_space_features.mean_shortest_path(), 3)])
    info_writer.writerow([space_name, "max shortest path", round(lviv_space_features.max_shortest_path(), 3), \
                          round(bristol_space_features.max_shortest_path(), 3)])
    info_writer.writerow([space_name, "path length efficiency", round(lviv_space_features.path_length_efficiency(), 3),\
                          round(bristol_space_features.path_length_efficiency(), 3)])
    info_writer.writerow([space_name, "molloy reed criterion", round(lviv_space_features.molloy_reed_criterion(), 3), \
                          round(bristol_space_features.molloy_reed_criterion(), 3)])
    info_writer.writerow([space_name, "random graph clustering coefficient", \
                          round(lviv_space_features.random_graph_clustering_coefficient(), 3), \
                          round(bristol_space_features.random_graph_clustering_coefficient(), 3)])
    info_writer.writerow([space_name, "random graph mean shortest path", \
                          round(lviv_space_features.random_graph_average_path(), 3), \
                          round(bristol_space_features.random_graph_average_path(), 3)])

