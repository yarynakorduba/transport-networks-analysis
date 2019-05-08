from AttackSimulation import RandomNodeAttackSimulation
from Visualization import compute_areas_under_the_curve, generate_plot
from run_visualizations import plot_all_city_simulations


def compute_figname(city, space, delete_by, recalculated):
    figname = "./results_clustered_at_40m/simulation_images/" + city + "/" + space.upper() + "Space/"
    if delete_by:
        figname += city + "_" + space + "_space_by_" + delete_by
    else:
        figname += city + "_" + space + "_space_random"
    if recalculated:
        figname += "_recalculated.png"
    else:
        figname += "_initial.png"
    return figname


space = "l"
transport_type = "all"
city = "bristol"
plot="linlin"
stops_file = "./data/" + city.lower() + "_parsed/processed/" \
             + city + transport_type.capitalize() + "StopsProcessed40m.json"
routes_file = "./data/" + city.lower() + "_parsed/processed/" \
              + city + transport_type.capitalize() + "JourneysProcessed40m.json"

results_table = "./results_clustered_at_40m/tables/RESILIENCE_AREA_CURVES.csv"
info = "./results_clustered_at_40m/points_for_plots/" + city + "_" + space + "_space"


# labels_to_plot=["RA", "$k$", "$k^i$", r"$C_{\beta}$", r"$C_{\beta}^i$"]


def run_each_simulation():
    delete_by = None
    recalculated = False
    simulation = RandomNodeAttackSimulation(space, stops_file, routes_file, info)
    simulation.simulations(delete_by, recalculated)
    simulation.write_simulation_data_to_file()
    generate_plot(simulation.get_simulation_results(), plot, "c", "S", \
                  labels=["1st trial", "2nd trial", "3rd trial", "4th trial", "5th trial"], \
                  figname=compute_figname(city, space, delete_by, recalculated))
    print(len(simulation.get_simulation_results()))
    print("Area under the curve: ", compute_areas_under_the_curve(simulation.get_simulation_results(), \
                                                                  city, space, results_table, delete_by, recalculated))

    delete_by = "degrees"
    recalculated = False
    simulation = RandomNodeAttackSimulation(space, stops_file, routes_file, info)
    simulation.simulations(delete_by, recalculated)
    simulation.write_simulation_data_to_file()
    generate_plot(simulation.get_simulation_results(), plot, "c", "S", \
                  labels=["$k^i$"], \
                  figname=compute_figname(city, space, delete_by, recalculated))
    print("Area under the curve: ", compute_areas_under_the_curve(simulation.get_simulation_results(), \
                                                                  city, space, results_table, delete_by, recalculated))

    delete_by = "degrees"
    recalculated = True
    simulation = RandomNodeAttackSimulation(space, stops_file, routes_file, info)
    simulation.simulations(delete_by, recalculated)
    simulation.write_simulation_data_to_file()
    generate_plot(simulation.get_simulation_results(), plot, "c", "S", \
                  labels=["$k$"], \
                  figname=compute_figname(city, space, delete_by, recalculated))
    print("Area under the curve: ", compute_areas_under_the_curve(simulation.get_simulation_results(), \
                                                                  city, space, results_table, delete_by, recalculated))

    delete_by = "betweenness"
    recalculated = False
    simulation = RandomNodeAttackSimulation(space, stops_file, routes_file, info)
    simulation.simulations(delete_by, recalculated)
    simulation.write_simulation_data_to_file()
    generate_plot(simulation.get_simulation_results(), plot, "c", "S", \
                  labels=[r"$C_{\beta}^i$"], \
                  figname=compute_figname(city, space, delete_by, recalculated))
    print("Area under the curve: ", compute_areas_under_the_curve(simulation.get_simulation_results(), \
                                                                  city, space, results_table, delete_by, recalculated))

    delete_by = "betweenness"
    recalculated = True
    simulation = RandomNodeAttackSimulation(space, stops_file, routes_file, info)
    simulation.simulations(delete_by, recalculated)
    simulation.write_simulation_data_to_file()
    generate_plot(simulation.get_simulation_results(), plot, "c", "S", \
                  labels=[r"$C_{\beta}$"], \
                  figname=compute_figname(city, space, delete_by, recalculated))
    print("Area under the curve: ", compute_areas_under_the_curve(simulation.get_simulation_results(), \
                                                                  city, space, results_table, delete_by, recalculated))


run_each_simulation()

