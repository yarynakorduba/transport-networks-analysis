import csv

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

DEFAULT_COLORS = ["red", "blue", "orange", "brown", "green", "black", "pink"]


def plot_lin_lin(points, x_label="", y_label="", colors=DEFAULT_COLORS, labels=None, figname="", s=6):
    if points:
        plt.rcParams.update({'font.size': 12})
        fig, ax = plt.subplots()
        for ind in range(0, len(points)):
            if isinstance(points[ind], dict):
                sequence = [[float(key) for key in points[ind].keys()], points[ind].values()]
            else:
                sequence = points[ind]
            if len(sequence[1]) == 0:
                ax.axvline(x=sequence[0][0])
            elif len(sequence[0]) == 0:
                ax.axvline(y=sequence[1][0])
            elif labels is not None:
                ax.scatter(*sequence, c=colors[ind], alpha=0.5, s=s, label=labels[ind])
                ax.legend()
            else:
                ax.scatter(*sequence, c=colors[ind], alpha=0.5, s=s)


        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if figname:
            plt.savefig(figname)
        else:
            plt.show()
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


"""
Finds the average area under the curve among array of sequences. Writes it to the file specified.
"""
def compute_areas_under_the_curve(sequences, city, space, filepath, delete_by=False, recalculated=False):
    results_sum = 0
    for ind in range(0, len(sequences)):
        if isinstance(sequences[ind], dict):
            sequence_y = list(sequences[ind].values())
            sequence_x = [float(num) for num in list(sequences[ind].keys())]
        results_sum += np.trapz(y=sequence_y, x=sequence_x)
    with open(filepath, "a+") as file:
        result = round(results_sum / len(sequences), 3)
        info_writer = csv.writer(file, delimiter=',', quotechar='"')
        info_writer.writerow([city, space, delete_by, recalculated, result])
    return result


def display_graph(graph, with_labels=False):
    if graph:
        nx.draw(graph, node_size=30, edge_color="DarkTurquoise", node_color="DarkCyan", with_labels=with_labels)
        plt.show()
    else:
        print("No graph was received")
