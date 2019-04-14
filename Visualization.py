import csv

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

DEFAULT_COLORS = ["red", "blue", "orange", "brown", "green", "black", "pink"]


def plot_lin_lin(points, x_label="", y_label="", colors=DEFAULT_COLORS, labels=DEFAULT_COLORS, figname="", s=6):
    if points:
        fig, ax = plt.subplots()
        for ind in range(0, len(points)):
            if isinstance(points[ind], dict):
                sequence = [[float(key) for key in points[ind].keys()], points[ind].values()]
            else:
                sequence = points[ind]
            if ind < len(points):
                ax.scatter(*sequence, c=colors[ind], alpha=0.5, s=s, label=labels[ind])
            else:
                ax.scatter(*sequence, s=3)
        ax.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(figname)
    else:
        print("No points were received")


def plot_log_log(points, x_label="", y_label="", colors=DEFAULT_COLORS, labels=DEFAULT_COLORS, figname="", s=6, ylim=None, xlim=None):
    if points:
        fig, ax = plt.subplots()
        for ind in range(0, len(points)):
            if isinstance(points[ind], dict):
                sequence = [[float(key) for key in points[ind].keys()], points[ind].values()]
            else:
                sequence = points[ind]
            if ind < len(points):
                ax.scatter(*sequence, c=colors[ind], alpha=0.5, s=s, label=labels[ind])
            else:
                ax.scatter(*sequence, s=3)
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.legend()
        if ylim:
            plt.ylim(*ylim)
        if xlim:
            plt.xlim(*xlim)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(figname)
    else:
        print("No points were received")


def plot_lin_log(points, x_label="", y_label="", s=6, ylim=None, xlim=None):
    if points:
        if isinstance(points, dict):
            points = [points.keys(), points.values()]
        fig, ax = plt.subplots()
        ax.scatter(*points, c='red', alpha=0.5, s=s)
        ax.set_yscale('log')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    else:
        print("No points were received")


# TODO: change dx to equal to step
# IMPORTANT!!! THE DX VALUE DEPENDS ON THE STEP IN ATTACK SIMULATION!!!
# CHANGE IT IF YOU CHANGE THE STEP!!!
def compute_areas_under_the_curve(sequences, city, space, delete_by=False, recalculated=False):
    results_sum = 0
    for ind in range(0, len(sequences)):
        if isinstance(sequences[ind], dict):
            sequence = list(sequences[ind].values())
        results_sum += np.trapz(y=sequence, dx=0.01)
    with open("results/RESILIENCE_AREA_CURVES.csv", "a+") as file:
        result = results_sum / len(sequences)
        info_writer = csv.writer(file, delimiter=',', quotechar='"')
        info_writer.writerow([city, space, delete_by, recalculated, result])
    return result


def display_graph(graph, with_labels=False):
    if graph:
        nx.draw(graph, node_size=30, edge_color="DarkTurquoise", node_color="DarkCyan", with_labels=with_labels)
        plt.show()
    else:
        print("No graph was received")
