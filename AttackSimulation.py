import json
import random
from NetworkFeatures import NetworkFeatures
from GraphSpaces import GraphSpaces


class RandomNodeAttackSimulation:
    def __init__(self, space, incoming_routes, all_routes, info):
        self.simulation_info=info
        self.space = GraphSpaces(incoming_routes, all_routes).get_graph(space)
        self.simulation_results = []

    def __str__(self):
        return "Simulation tables: " + str(self.simulation_results)
    
    def get_simulation_results(self):
        return self.simulation_results

    def _configure_simulation(self):
        simulation_graph = self.space.copy()
        graph_estimations = NetworkFeatures(simulation_graph)
        one_percent_of_nodes = round(len(simulation_graph.nodes) / 100)
        initial_nodes_number = len(simulation_graph.nodes)
        simulation_results = dict({0: len(graph_estimations.build_GCC().nodes) / initial_nodes_number})
        return initial_nodes_number, one_percent_of_nodes, simulation_graph, simulation_results, graph_estimations

    def sort_nodes_by_degree_before_simulation(self, graph):
        sorted_node_degrees = sorted(NetworkFeatures(graph).degree(), key=lambda node: node[1], reverse=True)
        node_labels = list(map(lambda x: x[0], sorted_node_degrees))
        return node_labels

    def sort_nodes_by_betweenness_centrality_before_simulation(self, graph):
        betweenness_centralities = NetworkFeatures(graph).betweenness_centrality()
        return sorted(betweenness_centralities, key=lambda node: betweenness_centralities[node],
                      reverse=True)

    def sort_nodes_for_simulation(self, delete_by, graph):
        if delete_by.lower() == "degrees":
            return self.sort_nodes_by_degree_before_simulation(graph)
        else:
            return self.sort_nodes_by_betweenness_centrality_before_simulation(graph)

    def _random_failure_simulation(self):
        initial_nodes_number, one_percent_of_nodes, simulation_graph, simulation_results, graph_estimations = self._configure_simulation()
        ind = one_percent_of_nodes
        while True:
            if one_percent_of_nodes < len(simulation_graph.nodes):
                nodes_to_delete = random.sample(simulation_graph.nodes, one_percent_of_nodes)
            else:
                break
            simulation_graph.remove_nodes_from(nodes_to_delete)
            simulation_results[ind / initial_nodes_number] = \
                len(graph_estimations.build_GCC().nodes) / initial_nodes_number
            ind += one_percent_of_nodes
        return simulation_results

    def _targeted_attack_simulation(self, delete_by, recalculated):
        initial_nodes_number, one_percent_of_nodes, simulation_graph, simulation_results, graph_estimations = self._configure_simulation()
        nodes = self.sort_nodes_for_simulation(delete_by, simulation_graph)
        ind = one_percent_of_nodes
        while True:
            if one_percent_of_nodes < len(simulation_graph.nodes):
                if recalculated:
                    nodes = self.sort_nodes_for_simulation(delete_by, simulation_graph)
                nodes_to_delete = nodes[:one_percent_of_nodes]
                nodes = nodes[one_percent_of_nodes:]
            else:
                break
            simulation_graph.remove_nodes_from(nodes_to_delete)
            simulation_results[ind / initial_nodes_number] = len(graph_estimations.build_GCC().nodes) / initial_nodes_number
            ind += one_percent_of_nodes
        simulation_results[1] = 0
        return simulation_results

    def simulations(self, delete_by=None, recalculated=False):
        if delete_by is None:
            self.simulation_info += "_random_attack"
            n = 5
        else:
            self.simulation_info += "_targeted_attack_by_" + delete_by
            if recalculated:
                self.simulation_info += "_recalculated"
            else:
                self.simulation_info += "_initial"
            n = 1
        for index in range(0, n):
            if delete_by is None:
                print("Random attack")
                random_f = self._random_failure_simulation()
                self.simulation_results.append(random_f)
            else:
                print("Targeted attack, deletion by: " + delete_by + ", recalculated: " + str(recalculated))
                targeted_att = self._targeted_attack_simulation(delete_by, recalculated)
                self.simulation_results.append(targeted_att)

    def write_simulation_data_to_file(self):
        with open(self.simulation_info + ".json", "w") as file:
            json.dump(self.get_simulation_results(), file)