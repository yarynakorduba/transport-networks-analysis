import json
import networkx as nx


class GraphSpaces:
    def __init__(self, stops_file, routes_file):
        self.stops_file = stops_file
        self.routes_file = routes_file

    def get_graph(self, space):
        return self._build(space)

    def number_of_routes(self):
        starting_stops = set()
        with open(self.routes_file, "r") as file:
            for line in file:
                if line[1] == "S":
                    starting_stops.add(line[38:42])
        return len(starting_stops)

    def _build(self, space):
        if space.lower() == "l":
            print("SPACE: L")
            return self._build_graph_l_space_from_json()
        elif space.lower() == "p":
            print("SPACE: P")
            return self._build_graph_p_space_from_json()
        elif space.lower() == "c":
            print("SPACE: C")
            return self._build_graph_c_space_from_json()
        else:
            return "No config for such space is available. We support only L-, P- and C- spaces."

    def _build_graph_c_space_from_json(self):
        graph = nx.Graph()
        with open(self.stops_file, 'r') as init_file:
            stops = json.loads(init_file.read())
        for stop in stops:
            for source_route_ind in range(0, len(stop["routes"])):
                graph.add_node(stop["routes"][source_route_ind])
                for target_route_ind in range(source_route_ind + 1, len(stop["routes"])):
                    graph.add_node(stop["routes"][target_route_ind])
                    if stop["routes"][source_route_ind] != stop["routes"][target_route_ind]:
                        graph.add_edge(stop["routes"][source_route_ind], stop["routes"][target_route_ind])
        return graph

    def _build_graph_l_space_from_json(self):
        graph = nx.Graph()
        with open(self.stops_file, 'r') as init_file:
            stops = json.loads(init_file.read())
        stops_dict = {stop["id"]: stop for stop in stops}

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
                if stop_node != target_node:
                    graph.add_edge(stop_node, target_node)
        return graph

    def _build_graph_p_space_from_json(self):
        graph = nx.Graph()
        with open(self.stops_file, "r") as stops_file:
            stops_data = json.loads(stops_file.read())
        with open(self.routes_file, "r") as routes_file:
            routes_data = json.loads(routes_file.read())
        stops_dict = {stop["id"]: stop for stop in stops_data}
        for route in routes_data:
            for source_stop_ind in range(0, len(route["stops"])):
                source_stop = route["stops"][source_stop_ind]
                if "cluster" in stops_dict[source_stop]:
                    source_node = "cluster" + str(stops_dict[source_stop]["cluster"])
                else:
                    source_node = source_stop
                graph.add_node(source_node)

                for target_stop_ind in range(source_stop_ind + 1, len(route["stops"])):
                    target_stop = route["stops"][target_stop_ind]
                    if "cluster" in stops_dict[target_stop]:
                        target_node = "cluster" + str(stops_dict[target_stop]["cluster"])
                    else:
                        target_node = target_stop
                    if source_node != target_node and not graph.has_edge(source_node, target_node):
                        graph.add_edge(source_node, target_node)

        return graph
