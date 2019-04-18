import json

from Visualization import plot_lin_lin


def visualize_all_stops_distances(city):
    path = "./data/" + city + "_parsed" + "/clustering_test/"
    path_to_points = path + city + "AllStopsDistances.json"

    with open(path_to_points, "r") as file:
        data = json.loads(file.read())
        data_dict = {str(i/len(data)*100): data[i] for i in range(0, len(data))}
    plot_lin_lin([data_dict, [[2.5], []]], y_label="distance", x_label="%")

visualize_all_stops_distances("lviv")