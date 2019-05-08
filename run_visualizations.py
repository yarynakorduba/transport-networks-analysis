import json

from GraphSpaces import GraphSpaces
from NetworkFeatures import NetworkFeatures
from Visualization import generate_plot


# For maximal stop distance in each cluster
def visualize_all_stops_distances(cities, radius, cumulative=False, plot_type="linlin"):
    points = []
    for city in cities:
        path = "./data/" + city + "_parsed" + "/clustering_test/data/"
        path_to_points = path + city + "MaxStopsDistancesInClusters" + radius + "m.json"
        with open(path_to_points, "r") as f:
            data = json.loads(f.read())
            if cumulative:
                points.append({data[i] * 1000: sum(data[i:]) / sum(data) for i in range(0, len(data))})
            else:
                points.append({str(i / len(data) * 100): data[i] * 1000 for i in range(0, len(data))})
    if cumulative:
        generate_plot(points, plot_type, y_label="P(D)", x_label="D", \
                      labels=[city.capitalize() for city in cities],
                      figname="citiesCumulativeMaxCluster" + radius + "mDistances.png")
    else:
        generate_plot(points, plot_type, y_label="distance (in meters) for R=" + radius, x_label="", \
                      labels=[city.upper() for city in cities],
                      figname="citiesMaxCluster" + radius + "mDistances.png")


# For node degree and path length distributions
def plot_distributions(distribution, clusterR, space_name, cumulative=False, plot_type="linlin",
                       saveFiq=False, x_lim=(0, 30), y_lim=(0, 1.5), with_fit=False, with_line=False):
    lviv_stops_dataset = "./data/lviv_parsed/processed/lvivAllStopsProcessed" + clusterR + "m.json"
    lviv_routes_dataset = "./data/lviv_parsed/processed/lvivAllJourneysProcessed" + clusterR + "m.json"
    bristol_stops_dataset = "./data/bristol_parsed/processed/bristolAllStopsProcessed" + str(clusterR) + "m.json"
    bristol_routes_dataset = "./data/bristol_parsed/processed/bristolAllJourneysProcessed" + str(clusterR) + "m.json"

    lviv_space = GraphSpaces(lviv_stops_dataset, lviv_routes_dataset)
    lviv_graph = lviv_space.get_graph(space_name)
    lviv_space_features = NetworkFeatures(lviv_graph)
    bristol_space = GraphSpaces(bristol_stops_dataset, bristol_routes_dataset)
    bristol_graph = bristol_space.get_graph(space_name)
    bristol_space_features = NetworkFeatures(bristol_graph)

    if distribution == "degree":
        if cumulative:
            lviv_degrees = lviv_space_features.cumulative_degree_distribution()
            bristol_degrees = bristol_space_features.cumulative_degree_distribution()
            folder = "/distributions_images/node_degrees/cumulative_"

        else:
            lviv_degrees = lviv_space_features.degree_distribution()
            bristol_degrees = bristol_space_features.degree_distribution()
            folder = "/distributions_images/node_degrees/"

        lviv_distribution = lviv_degrees
        bristol_distribution = bristol_degrees
        print(lviv_degrees)
        print(bristol_degrees)
        x_label = "k"
        y_label = "P(k)"
    elif distribution == "path":
        if cumulative:
            lviv_paths = lviv_space_features.cumulative_shortest_path_distribution()
            bristol_paths = bristol_space_features.cumulative_shortest_path_distribution()
            folder = "/distributions_images/path_lengths/cumulative_"
        else:
            lviv_paths = lviv_space_features.shortest_path_distribution()
            bristol_paths = bristol_space_features.shortest_path_distribution()
            folder = "/distributions_images/path_lengths/"

        lviv_distribution = lviv_paths
        bristol_distribution = bristol_paths
        x_label = "l"
        y_label = "P(l)"
    else:
        print("Specify the distribution")
        return -1

    if saveFiq:
        generate_plot([lviv_distribution, bristol_distribution], plot_type, y_label=y_label,
                      x_label=x_label, s=15, labels=["Lviv", "Bristol"],
                      figname="./results_clustered_at_" + str(clusterR) + "m" + folder + plot_type +
                              "_lviv_bristol_" + space_name + "_space_" + distribution + "Connected.png",
                      x_lim=x_lim, y_lim=y_lim, with_fit=with_fit, with_line=with_line)
    else:
        generate_plot([lviv_distribution, bristol_distribution], plot_type, y_label=y_label,
                      x_label=x_label, s=15, labels=["Lviv", "Bristol"],
                      x_lim=x_lim, y_lim=y_lim, with_fit=with_fit, with_line=with_line)

# For attack simulations
def plot_all_city_simulations(city, space, pathToFiles, pathToImages, plot_type="linlin"):
    # labels_to_plot = ["випадкова атака", "k (з пересортуванням)", "k (без пересортування)", \
    #                   r"$C_{b}$" + " (з пересортуванням)", r"$C_{b}$" + " (без пересортування)"]
    labels_to_plot = ["RA", "$k$", "$k^i$", r"$C_{\beta}$", r"$C_{\beta}^i$"]

    with open(pathToFiles + city + "_" + space + "_space_random_attack.json", "r") as random_attack_file:
        random_attack = json.loads(random_attack_file.read())[0]
    with open(pathToFiles + "/" + city + "_" + space + "_space_targeted_attack_by_degrees_initial.json",
              "r") as by_init_degrees_attack_file:
        degrees_init_attack = json.loads(by_init_degrees_attack_file.read())[0]
    with open(pathToFiles + "/" + city + "_" + space + "_space_targeted_attack_by_degrees_recalculated.json",
              "r") as by_recalc_degrees_attack_file:
        degrees_recalc_attack = json.loads(by_recalc_degrees_attack_file.read())[0]
    with open(pathToFiles + "/" + city + "_" + space + "_space_targeted_attack_by_betweenness_initial.json",
              "r") as by_init_betweenness_attack_file:
        betweenness_init_attack = json.loads(by_init_betweenness_attack_file.read())[0]
    with open(pathToFiles + "/" + city + "_" + space + "_space_targeted_attack_by_betweenness_recalculated.json",
              "r") as by_recalc_betweenness_attack_file:
        betweenness_recalc_attack = json.loads(by_recalc_betweenness_attack_file.read())[0]
    simulations_to_plot = [random_attack, degrees_recalc_attack, degrees_init_attack, \
                           betweenness_recalc_attack, betweenness_init_attack]
    file_to_save_plot = pathToImages + city + "_" + space + "_space_all.png"

    generate_plot(simulations_to_plot, plot_type, "c", "S", labels=labels_to_plot,
                  figname=file_to_save_plot)


def plot_stops_on_radius_around_centroid_dependence():
    with open("data/pointsInLatticeRadiusAroundCentroidDependence.json", "r") as test_file:
        test_stops = json.loads(test_file.read())
    generate_plot([test_stops], "loglog", "R", "N", labels=["2D Lattice"])

# plot_stops_on_radius_around_centroid_dependence()
    # with open("./data/lviv_parsed/before_processing/lvivStopsOnRadiusAroundCentroidDependence.json", "r") as lviv_file:
    #     lviv_stops = json.loads(lviv_file.read())
    # with open("./data/bristol_parsed/before_processing/bristolStopsOnRadiusAroundCentroidDependence.json",
    #           "r") as bristol_file:
    #     bristol_stops = json.loads(bristol_file.read())
    # generate_plot([lviv_stops, bristol_stops], "loglog", "R", "N", labels=["Lviv", "Bristol"])


# For number stops while specific clustering radius is applied
def plot_stops_on_clustering_radius_dependence():
    with open("./data/lviv_parsed/clustering_test/testClusteringlvivStopsNumber.json", "r") as lviv_file:
        lviv_stops = json.loads(lviv_file.read())
    with open("./data/bristol_parsed/clustering_test/testClusteringbristolStopsNumber.json",
              "r") as bristol_file:
        bristol_stops = json.loads(bristol_file.read())
    generate_plot([lviv_stops, bristol_stops], "linlin", "R", "N",
                  labels=["Lviv", "Bristol"], figname="testClusteringLvivBristolStopsNumber.png")


# for path distributions
# plot_distributions("path", "40", "l", False, "linlin", False, x_lim=(0, 80), y_lim=(0.01, 0.2), with_fit=True)
# plot_distributions("path", "40", "l", False, "loglog", True, x_lim=(0.9, 80), y_lim=(0.01, 0.2))
# plot_distributions("path", "40", "l", False, "linlog", True, x_lim=(0, 80), y_lim=(0.01, 0.2))
# #
# plot_distributions("path", "40", "c", True, "linlog", True, x_lim=(0, 10), y_lim=(0.01, 1.09))
# plot_distributions("path", "40", "c", True, "loglog", True, x_lim=(0.9, 10), y_lim=(0.01, 2))
# plot_distributions("path", "40", "c", False, "linlin", True, x_lim=(-0.001, 6), y_lim=(-0.001, 1.09))
# #
# plot_distributions("path", "40", "p", True, "linlog", True, x_lim=(0, 10), y_lim=(0.01, 1.09))
# plot_distributions("path", "40", "p", True, "loglog", True, x_lim=(0.9, 10), y_lim=(0.01, 2))
# plot_distributions("path", "40", "p", False, "linlin", False, x_lim=(0, 10), y_lim=(0.01, 1.09))


# for degree distributions
# plot_distributions("degree", "40", "l", False, "linlin", False, x_lim=(0, 30), y_lim=(0.01, 1.09), with_line=True)
# plot_distributions("degree", "40", "l", True, "loglog", False, x_lim=(0.9, 30), y_lim=(0.01, 2), with_line=True)
# plot_distributions("degree", "40", "l", False, "linlog", False, x_lim=(0, 30), y_lim=(0.01, 1.09), with_fit=True)
#
# plot_distributions("degree", "40", "c", True, "linlog", True, x_lim=(0, 100), y_lim=(0.09, 1.09))
# plot_distributions("degree", "40", "c", True, "loglog", False, x_lim=(0.9, 100), y_lim=(0.09, 2), with_fit=True)
# plot_distributions("degree", "40", "c", True, "linlin", True, x_lim=(0, 100), y_lim=(0.0, 1.09))
#
plot_distributions("degree", "40", "p", True, "linlog", False, x_lim=(0, 500), y_lim=(0.03, 1.09))
# plot_distributions("degree", "40", "p", True, "loglog", False, x_lim=(0.09, 500), y_lim=(0.01, 2))
# plot_distributions("degree", "40", "p", True, "linlin", True, x_lim=(0, 500), y_lim=(0.01, 1.09))


# plot_all_city_simulations("lviv", "p", "./results_clustered_at_40m/points_for_plots/",
#                           "./results_clustered_at_40m/simulation_images/")
# visualize_all_stops_distances(["bristol","lviv"], "30", True)
# plot_stops_on_radius_around_centroid_dependence()
