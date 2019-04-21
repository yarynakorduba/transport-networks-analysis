import json

from GraphSpaces import GraphSpaces
from NetworkFeatures import NetworkFeatures
from Visualization import plot_lin_lin


def visualize_all_stops_distances(cities, radius, cumulative=False):
    points = []
    for city in cities:
        path = "./data/" + city + "_parsed" + "/clustering_test/max_stops_distances_in_clusters/"
        path_to_points = path + city + "MaxStopsDistancesInClusters" + radius + "m.json"
        with open(path_to_points, "r") as f:
            data = json.loads(f.read())
            if cumulative:
                points.append({data[i] * 1000: sum(data[i:]) / sum(data) for i in range(0, len(data))})
            else:
                points.append({str(i / len(data) * 100): data[i] * 1000 for i in range(0, len(data))})
    if cumulative:
        plot_lin_lin(points, y_label="P(D)", x_label="D", \
                     labels=[city.capitalize() for city in cities],
                     figname="citiesCumulativeMaxCluster"+radius+"mDistances.png")
    else:
        plot_lin_lin(points, y_label="distance (in meters) for R=" + radius, x_label="", \
                     labels=[city.upper() for city in cities],
                     figname="citiesMaxCluster" + radius + "mDistances.png")


def plot_distributions(distribution, clusterR, space_name):
    lviv_stops_dataset = "./data/lviv_parsed/processed/lvivAllStopsProcessed" + clusterR + "m.json"
    lviv_routes_dataset = "./data/lviv_parsed/processed/lvivAllJourneysProcessed" + clusterR + "m.json"
    bristol_stops_dataset = "./data/bristol_parsed/processed/bristolBusStopsProcessed" + str(clusterR) + "m.json"
    bristol_routes_dataset = "./data/bristol_parsed/processed/bristolBusJourneysProcessed" + str(clusterR) + "m.json"

    lviv_space = GraphSpaces(lviv_stops_dataset, lviv_routes_dataset)
    lviv_graph = lviv_space.get_graph(space_name)
    lviv_space_features = NetworkFeatures(lviv_graph)
    bristol_space = GraphSpaces(bristol_stops_dataset, bristol_routes_dataset)
    bristol_graph = bristol_space.get_graph(space_name)
    bristol_space_features = NetworkFeatures(bristol_graph)

    if distribution == "degree":
        lviv_distribution = [lviv_space_features.degree_distribution()[0], \
                             [el * 100 for el in lviv_space_features.degree_distribution()[1]]]
        bristol_distribution = [bristol_space_features.degree_distribution()[0], \
                                [el * 100 for el in bristol_space_features.degree_distribution()[1]]]
        folder = "/distributions_images/node_degrees/"
        x_label = "ступінь вузла k"
        y_label = "% вузлів у мережі"
    elif distribution == "path":
        lviv_distribution = [lviv_space_features.shortest_path_distribution()[0], \
                             [el * 100 for el in lviv_space_features.shortest_path_distribution()[1]]]
        bristol_distribution = [bristol_space_features.shortest_path_distribution()[0], \
                                [el * 100 for el in bristol_space_features.shortest_path_distribution()[1]]]
        folder = "/distributions_images/path_lengths/"
        x_label = "найкоротший шлях l"
        y_label = "% шляхів у мережі"
    else:
        print("Specify the distribution")
        return -1

    plot_lin_lin([lviv_distribution, bristol_distribution], y_label=y_label, \
                 x_label=x_label, s=15, labels=["Львів", "Брістоль"], \
                 figname="./results_clustered_at_" + str(clusterR) + "m" + folder + \
                         "lviv_bristol_" + space_name + "_space_" + distribution + ".png")


# plot_distributions("degree", "30", "l")
visualize_all_stops_distances(["bristol","lviv"], "30", True)
