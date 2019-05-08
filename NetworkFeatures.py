import networkx as nx
import math
from itertools import groupby


class NetworkFeatures:
    def __init__(self, graph):
        self.data = []
        self.graph = graph
        self.GCC = None

    def __str__(self):
        return "Network representation"

    def get_graph(self):
        return self.graph

    def is_graph_connected(self):
        return nx.is_connected(self.graph)

    def number_of_nodes(self, GCC=False):
        if GCC:
            if not self.GCC:
                self.build_GCC()
            N = nx.number_of_nodes(self.GCC)
        else:
            N = nx.number_of_nodes(self.graph)
        return N

    def number_of_edges(self):
        M = nx.number_of_edges(self.graph)
        return M

    def mean_betweenness_centrality(self):
        node_quantity = self.number_of_nodes()
        b_centrality = self.betweenness_centrality()
        mean_b_centrality = sum(b_centrality.values()) / node_quantity
        return mean_b_centrality

    def graph_assortativity(self):
        r = nx.degree_assortativity_coefficient(self.graph)
        return round(r, 2)

    def mean_shortest_path(self):
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
            l = nx.average_shortest_path_length(self.GCC)
        else:
            l = nx.average_shortest_path_length(self.graph)
        return l

    def mean_clustering_coefficient(self):
        C = nx.average_clustering(self.graph)
        return round(C, 3)

    def build_GCC(self):
        sub_graphs = nx.connected_component_subgraphs(self.graph)
        self.GCC = max(sub_graphs, key=len)
        return self.GCC

    def degree(self):
        k = nx.degree(self.graph)
        return k

    def betweenness_centrality(self):
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
            b_centrality = nx.betweenness_centrality(self.GCC)
        else:
            b_centrality = nx.betweenness_centrality(self.graph)
        return b_centrality

    def mean_degree(self, GCC=False):
        if GCC:
            if not self.GCC:
                self.build_GCC()
            mean_k = nx.degree(self.GCC)
            n_nodes = nx.number_of_nodes(self.GCC)
        else:
            mean_k = nx.degree(self.graph)
            n_nodes = nx.number_of_nodes(self.graph)
        sum_nodes = sum(node[1] for node in mean_k)
        return round(sum_nodes / n_nodes, 4)

    def mean_square_degree(self):
        mean_k = nx.degree(self.graph)
        sum_nodes = sum(node[1] ** 2 for node in mean_k)
        n_nodes = nx.number_of_nodes(self.graph)
        return round(sum_nodes / n_nodes, 2)

    def max_degree(self):
        k = nx.degree(self.graph)
        max_k = max(node[1] for node in k)
        return max_k

    def random_graph_clustering_coefficient(self):
        k = self.mean_degree()
        N = self.number_of_nodes()
        C_rand = k / (N - 1)
        return C_rand

    # TODO: change base to natural
    def random_graph_average_path(self):
        alpha = 0.5772  # Euler-Mascherroni constant
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
        k = self.mean_degree(True)
        N = self.number_of_nodes(True)
        l = (math.log(N, 10) - alpha) / math.log(k, 10) + 0.5
        return l

    def max_shortest_path(self):
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
            return nx.diameter(self.GCC)
        return nx.diameter(self.graph)

    def path_length_efficiency(self):
        l = self.mean_shortest_path()
        l_rand = self.random_graph_average_path()
        return l / l_rand

    def mean_shortest_travel_time(self):  # not correct yet
        if not self.GCC:
            self.build_GCC()
        l_t_pairs = nx.average_shortest_path_length(self.GCC, weight="weight")
        return l_t_pairs

    def molloy_reed_criterion(self):
        return self.mean_square_degree() / self.mean_degree()

    def cumulative_shortest_path_distribution(self):
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
            shortest_paths = dict(nx.shortest_path_length(self.GCC))
        else:
            shortest_paths = dict(nx.shortest_path_length(self.graph))
        paths_values = []
        for element in list(shortest_paths.values()):
            paths_values += list(element.values())
        paths_occurences_dict = {key: len(list(group)) for key, group in groupby(sorted(paths_values))}
        paths_distribution = dict()

        for key in range(0, len(paths_occurences_dict)):
            paths_distribution[key] = sum([paths_occurences_dict[index] for index in list(paths_occurences_dict.keys())
                                                if index >= key]) / sum([paths_occurences_dict[ind] for ind in list(paths_occurences_dict.keys())])
        return paths_distribution

    def cumulative_degree_distribution(self):
        node_degrees = self.degree()
        values = set(map(lambda x: x[1], node_degrees))
        degrees_occurences_dict = {x: len([y[0] for y in node_degrees if y[1] == x]) for x in values}
        degrees_distribution_dict = dict()
        for key in range(0, len(degrees_occurences_dict)):
            degrees_distribution_dict[key] = sum([degrees_occurences_dict[index] for index in list(degrees_occurences_dict.keys())
                                                if index >= key]) / sum([degrees_occurences_dict[ind] for ind in list(degrees_occurences_dict.keys())])
        return degrees_distribution_dict

    def shortest_path_distribution(self):
        if not nx.is_connected(self.graph):
            if not self.GCC:
                self.build_GCC()
            shortest_paths = dict(nx.shortest_path_length(self.GCC))
        else:
            shortest_paths = dict(nx.shortest_path_length(self.graph))
        paths_values = []
        for element in list(shortest_paths.values()):
            paths_values += list(element.values())
        paths_occurences_dict = {key: len(list(group)) for key, group in groupby(sorted(paths_values))}
        paths_distribution = dict()

        for key in range(0, len(paths_occurences_dict)):
            paths_distribution[key] = paths_occurences_dict[key] / sum([paths_occurences_dict[ind]
                                                                        for ind in list(paths_occurences_dict.keys())])
        return paths_distribution

    def degree_distribution(self):
        node_degrees = self.degree()
        values = set(map(lambda x: x[1], node_degrees))
        degrees_occurences_quantities = {x: len([y[0] for y in node_degrees if y[1] == x]) for x in values}
        degrees_occurences_values = list(degrees_occurences_quantities.values())
        y = []
        for val in range(0, len(degrees_occurences_values)):
            y.append(degrees_occurences_values[val] / sum(degrees_occurences_values))
        x = [val for val in degrees_occurences_quantities.keys()]
        return [x, y]

