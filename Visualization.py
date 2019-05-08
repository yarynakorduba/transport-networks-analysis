import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.optimize import curve_fit

DEFAULT_COLORS = ["red", "blue", "orange", "brown", "green", "black", "pink"]


def unimodal_func(x, a, b, c):
    return a * x * np.exp(-b * x ** 2 + c * x)


def exponential_law(x, epsylon):
    return np.exp(-epsylon * x)

def power_law(x, gamma):
    return 1/(x**(gamma))


def generate_plot(points, plotType="linlin", x_label="", y_label="", colors=DEFAULT_COLORS,
                  labels=None, figname="", s=6, x_lim=None, y_lim=None, with_fit=False, with_line=False):
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
            if with_fit:
                x = np.array(sequence[0])
                y = np.array(list(sequence[1]))
                xdata = np.linspace(x.min(), x.max(), 100)
                if plotType == "linlin":
                    popt, pcov = curve_fit(unimodal_func, x, y)
                    ydata = unimodal_func(xdata, *popt)
                elif plotType == "linlog":
                    popt, pcov = curve_fit(exponential_law, x, y)
                    ydata = exponential_law(x, *popt)
                elif plotType == "loglog":
                    popt, pcov = curve_fit(power_law, x, y)
                    ydata = power_law(x, *popt)
                print(popt, pcov)
                plt.plot(xdata, ydata, c=colors[ind], alpha=0.5, linewidth=0.7)

        if plotType == "loglog":
            ax.set_yscale("log")
            ax.set_xscale("log")
        elif plotType == "linlog":
            ax.set_yscale("log")
        if x_lim:
            plt.xlim(*x_lim)
        if y_lim:
            plt.ylim(*y_lim)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        if figname:
            plt.savefig(figname)
        else:
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
