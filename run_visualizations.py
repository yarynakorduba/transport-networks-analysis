import json

from Visualization import plot_lin_lin

labels_to_plot=["RA", "$k$", "$k^i$", r"$C_{\beta}$", r"$C_{\beta}^i$"]


# # for Bristol PSpace
# with open("points_for_plots/bristol_c_space_random_attack.json", "r") as c_space_random_attack_file:
#     c_space_random_attack = json.loads(c_space_random_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_degrees_initial.json", "r") as c_space_by_init_degrees_attack_file:
#     c_space_degrees_init_attack = json.loads(c_space_by_init_degrees_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_t argeted_attack_by_degrees_recalculated.json", "r") as c_space_by_recalc_degrees_attack_file:
#     c_space_degrees_recalc_attack = json.loads(c_space_by_recalc_degrees_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_betweenness_initial.json","r") as c_space_by_init_betweenness_attack_file:
#     c_space_betweenness_init_attack = json.loads(c_space_by_init_betweenness_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_betweenness_recalculated.json", "r") as c_space_by_recalc_betweenness_attack_file:
#     c_space_betweenness_recalc_attack = json.loads(c_space_by_recalc_betweenness_attack_file.read())[0]
# simulations_to_plot = [c_space_random_attack, c_space_degrees_recalc_attack, c_space_degrees_init_attack,\
#                             c_space_betweenness_recalc_attack,  c_space_betweenness_init_attack ]
# file_to_save_plot = "simulation_images/bristol/LSpace/c_space_all.png"


#
# # for Bristol СSpace
# with open("points_for_plots/bristol_c_space_random_attack.json", "r") as c_space_random_attack_file:
#     c_space_random_attack = json.loads(c_space_random_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_degrees_initial.json", "r") as c_space_by_init_degrees_attack_file:
#     c_space_degrees_init_attack = json.loads(c_space_by_init_degrees_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_degrees_recalculated.json", "r") as c_space_by_recalc_degrees_attack_file:
#     c_space_degrees_recalc_attack = json.loads(c_space_by_recalc_degrees_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_betweenness_initial.json","r") as c_space_by_init_betweenness_attack_file:
#     c_space_betweenness_init_attack = json.loads(c_space_by_init_betweenness_attack_file.read())[0]
# with open("points_for_plots/bristol_c_space_targeted_attack_by_betweenness_recalculated.json", "r") as c_space_by_recalc_betweenness_attack_file:
#     c_space_betweenness_recalc_attack = json.loads(c_space_by_recalc_betweenness_attack_file.read())[0]
# simulations_to_plot = [c_space_random_attack, c_space_degrees_recalc_attack,  c_space_degrees_init_attack,\
#                              c_space_betweenness_recalc_attack, c_space_betweenness_init_attack]
# file_to_save_plot = "simulation_images/bristol/CSpace/c_space_all.png"



# for Lviv CSpace
with open("points_for_plots/lviv_c_space_random_attack.json", "r") as c_space_random_attack_file:
    c_space_random_attack = json.loads(c_space_random_attack_file.read())[0]
with open("points_for_plots/lviv_c_space_targeted_attack_by_degrees_initial.json", "r") as c_space_by_init_degrees_attack_file:
    c_space_degrees_init_attack = json.loads(c_space_by_init_degrees_attack_file.read())[0]
with open("points_for_plots/lviv_c_space_targeted_attack_by_degrees_recalculated.json", "r") as c_space_by_recalc_degrees_attack_file:
    c_space_degrees_recalc_attack = json.loads(c_space_by_recalc_degrees_attack_file.read())[0]
with open("points_for_plots/lviv_c_space_targeted_attack_by_betweenness_initial.json","r") as c_space_by_init_betweenness_attack_file:
        c_space_betweenness_init_attack = json.loads(c_space_by_init_betweenness_attack_file.read())[0]
with open("points_for_plots/lviv_c_space_targeted_attack_by_betweenness_recalculated.json", "r") as c_space_by_recalc_betweenness_attack_file:
    c_space_betweenness_recalc_attack = json.loads(c_space_by_recalc_betweenness_attack_file.read())[0]
simulations_to_plot = [c_space_random_attack, c_space_degrees_recalc_attack, c_space_degrees_init_attack, \
                            c_space_betweenness_recalc_attack,  c_space_betweenness_init_attack]
labels_to_plot=["RA", "$k$", "$k^i$", r"$C_{\beta}$", r"$C_{\beta}^i$"]
file_to_save_plot = "simulation_images/lviv/LSpace/lviv_c_space_all.png"



plot_lin_lin(simulations_to_plot, "c", "S", labels=labels_to_plot, figname=file_to_save_plot)
