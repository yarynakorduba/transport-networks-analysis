import json
import re
import networkx as nx
import pandas as pd

class GraphSpaces:
    def __init__(self, file="data/bristolBusFullStopsTimes.CIF", initial_file="data/bristolBusFullStopsTimes.CIF"):
        self.file = file
        self.initial_file = initial_file

    def get_graph(self, space):
        return self._build(space)

    def number_of_routes(self):
        starting_stops = set()
        with open(self.initial_file, "r") as file:
            for line in file:
                if line[1] == "S":
                    starting_stops.add(line[38:42])
        return len(starting_stops)

    def _build(self, space):
        if space.lower() == "l" and self.file.split(".")[-1] == "csv":
            print("SPACE: L (from CSV file)")
            return self._build_graph_l_space_from_csv()
        elif space.lower() == "p" and self.file.split(".")[-1] == "csv":
            print("SPACE: P (from CSV file)")
            return self._build_graph_p_space_from_csv()
        elif space.lower() == "c" and self.file.split(".")[-1] == "csv":
            print("SPACE: C (from CSV file)")
            return self._build_graph_c_space_from_csv()
        elif space.lower() == "l":
            print("SPACE: L")
            return self._build_graph_l_space_from_json()
        elif space.lower() == "p":
            print("SPACE: P")
            return self._build_graph_p_space()
        elif space.lower() == "c":
            print("SPACE: C")
            return self._build_graph_c_space()
        else:
            return "No config for such space is available. We support only L-, P- and C- spaces."


    def _build_graph_l_space_from_json(self):
        graph = nx.Graph()
        with open(self.initial_file,'r') as init_file:
            stops = json.loads(init_file.read())
        stops_dict = {stop["id"]: stop for stop in stops}
        # for stop in stops:
        #     stops_dict[stop["id"]] = stop
        for stop_id, stop in stops_dict.items():
            if "cluster" in stop:
                stop_node = "cluster" + str(stop["cluster"])
            else:
                stop_node = stop_id
            graph.add_node(stop_node)

            for connection in stop["connections"]:
                if "cluster" in stops_dict[connection]:
                    target_node = "cluster" + str(stops_dict[connection]["cluster"])
                else:
                    target_node = connection
                graph.add_edge(stop_node, target_node)
        return graph

    def _build_graph_l_space_from_csv(self):
        graph = nx.Graph()
        data = pd.read_csv(self.initial_file, encoding="utf-8", sep=",", \
                                 header=0, low_memory=False)
        route_ids = data["route_id"].unique()
        for route_id in route_ids:
            stop_names = data[data["route_id"] == route_id]["stop_name"].values
            for stop_name_index in range(0, len(stop_names)):
                if stop_name_index + 1 < len(stop_names):
                    graph.add_edge(stop_names[stop_name_index], stop_names[stop_name_index + 1])
        return graph


    def _build_graph_p_space_from_csv(self):
        graph = nx.Graph()
        data = pd.read_csv(self.initial_file, encoding="utf-8", sep=",", \
                                 header=0, low_memory=False)
        route_ids = data["route_id"].unique()
        for route_id in route_ids:
            stop_names = data[data["route_id"] == route_id]["stop_name"].unique()
            for source_stop_ind in range(0, len(stop_names)):
                for target_stop_ind in range(source_stop_ind+1, len(stop_names)):
                    graph.add_edge(stop_names[source_stop_ind], stop_names[target_stop_ind])
        return graph


    def _build_graph_c_space_from_csv(self):
        graph = nx.Graph()
        data = pd.read_csv(self.initial_file, encoding="utf-8", sep=",", \
                                 header=0, low_memory=False)
        stops = data["stop_name"].unique()
        for stop in stops:
            routes = data[data["stop_name"] == stop]["route_short_name"].unique()
            for source_route in range(0, len(routes)):
                graph.add_node(routes[source_route])
                for target in range(source_route+1, len(routes)):
                    graph.add_edge(routes[source_route], routes[target])
        return graph


    def _build_graph_l_space(self):
        graph = nx.Graph()
        with open(self.file, "r") as file:
            data = file.readlines()
        for line in range(0, len(data)):
            if (line + 1 < len(data)) and data[line][:2] != "QS" and data[line][:2] != "QE" \
                    and data[line + 1][:2] != 'QS' and data[line+1][:2] != "QE":
                graph.add_edge(data[line][2:14], data[line + 1][2:14], \
                               weight=(float(data[line + 1][14:16]) * 60 \
                                       + float(data[line + 1][16:18]) \
                                       - (float(data[line][14:16]) * 60 \
                                          + float(data[line][16:18])))
                               )
        return graph

    def _build_graph_p_space(self):
        graph = nx.Graph()
        with open(self.file, "r") as file:
            data = file.readlines()
        for line in range(0, len(data)):
            if data[line][:2] == "QS":
                source = line + 1
                while not (source >= len(data) or data[source][:2] == 'QS'):
                    target = source + 1
                    while not (target >= len(data) or data[target][:2] == 'QS'):
                        graph.add_edge(data[source][2:14], data[target][2:14])
                        target += 1
                    source += 1
        return graph

    def _build_graph_c_space(self):
        i = 0
        graph = nx.Graph()
        stops_attributes = dict()
        route_id = None
        with open(self.file, "r") as file:
            data = file.readlines()
        # building a dictionary of view
        #  {stop1: {routeY, routeX, ...}, stop2: {routeY, routeZ, ...}...}
        while i < len(data):
            if data[i][1] == "S":
                route_id = data[i][37:41]
            else:
                # if stop has no routes yet
                if stops_attributes.get(data[i][2:14].strip(), set()) == set():
                    stops_attributes[data[i][2:14].strip()] = set()
                # adds a route to the stop
                stops_attributes[data[i][2:14].strip()].add(route_id)
            i += 1
        for stop in stops_attributes:
            subgraph = nx.complete_graph(len(stops_attributes[stop]))
            labels = dict()
            i = 0
            for route in stops_attributes[stop]:
                labels[i] = route.strip()
                i += 1
            subgraph = nx.relabel_nodes(subgraph, labels)
            graph = nx.compose(graph, subgraph)
        with open("data/bristol_c_space.json", "w") as final_file:
            json.dump([list(graph.nodes), list(graph.edges)], final_file)
        return graph

    def write_stops_lviv_l_space_to_file(self, file):
        nodes = []
        graph = self.get_graph("l")
        lviv_dataset = pd.read_csv(self.initial_file, encoding="utf-8", sep=",", \
                            header=0, low_memory=False)
        for node in graph.nodes:
            stop_from_dataset = lviv_dataset[lviv_dataset["stop_id"] == node]
            routes = stop_from_dataset["route_id"].unique().tolist()
            nodes.append({"id": str(stop_from_dataset["stop_id"].values[0]),\
                          "label": stop_from_dataset["stop_name"].values[0],
                          "connections": [str(n) for n in graph.neighbors(node)], \
                          "lat": stop_from_dataset["stop_lat"].values[0],
                          "lon":  stop_from_dataset["stop_lon"].values[0],
                          "routes": [str(route) for route in routes]
                          })
        with open(file, "w") as final_file:
            json.dump(nodes, final_file,  ensure_ascii=False)

    def write_stops_l_space_to_file(self, file):
        graph = self.get_graph("l")
        with open(self.initial_file, "r") as init_file:
            initial_data = init_file.read()
        nodes = []
        for node in graph.nodes:
            node_name = re.search("QLN" + node.strip() + "[A-Za-z ]*", initial_data)
            node_coordinates = re.search("QBN" + node + "[0-9 ]*", initial_data)
            print(node)
            node_cleaned_name = node_name.group()[15:-2].strip()
            node_cleaned_coordinates = node_coordinates.group()[15:].split()
            nodes.append({"id": node, "label": node_cleaned_name, \
                          "connections": [n for n in graph.neighbors(node)],
                          "connections": [n for n in graph.neighbors(node)],
                          "lat": node_cleaned_coordinates[0] if node_cleaned_coordinates[0] else None, \
                          "lon": node_cleaned_coordinates[1] if node_cleaned_coordinates[1] else None})
        with open(file, "w") as final_file:
            json.dump(list(nodes), final_file)

    def write_routes_c_space_to_file(self, file):
        graph = self.get_graph("c")
        nodes = []
        for node in graph.nodes:
            nodes.append({"id": node, "label": node, \
                          "connections": [n for n in graph.neighbors(node)]})
        with open(file, "w") as final_file:
            json.dump(list(nodes), final_file)
