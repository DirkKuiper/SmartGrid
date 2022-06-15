# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# main runs all the necessary functions: spine of the program

from multiprocessing import cpu_count
import pandas as pd
import numpy as np

from classes.house import House
from classes.battery import Battery
from classes.cable import Cable

from output import draw_rep_plot, draw_all_plot, find_cable_length
from output import make_json, jason_remakes, length_csv, csv_hist

from algorithms.algo_combi import (find_random_combi, find_closest_combi,
                                   make_dist_list, convert_dist_to_id)
from algorithms.algo_astar import make_cable

NUMBER_HOUSES = 150
NUMBER_BATTERIES = 5

# these are the 3 possible combinations of settings
# 1) house-battery combi is random, searching within 150 random configurations
# 2) hou-bat combi is ordered close->far, switching houses only (150 options)
# 3) hou-bat combi is ordered close->far, switching houses&batteries (750 options)
# see README.md for more extensive explanation
config_switch_settings = [['random', '', 150],
                          ['farthest', 'only houses', NUMBER_HOUSES],
                          ['farthest', 'both', NUMBER_HOUSES * NUMBER_BATTERIES]]

# load in the locations of the houses and batteries as provided
def load_district(DISTRICT):
    # read the csv's into dataframes
    df_bat = pd.read_csv(
        "data/district_{0}/district-{0}_batteries.csv".format(DISTRICT))
    df_hou = pd.read_csv(
        "data/district_{0}/district-{0}_houses.csv".format(DISTRICT))

    # make objects of each instance in the dataframe
    for idx, bat in df_bat.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = list(map(int, bat['positie'].split(',')))
        battery = Battery(idx, coord_pair[0], coord_pair[1], bat['capaciteit'])

    for idx, hou in df_hou.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = [int(hou['x']), int(hou['y'])]
        house = House(idx, coord_pair[0], coord_pair[1],
                      hou['maxoutput'], 'here will be a cable')

    # creates bitmap for grid to checks for edges
    bitmap = np.pad([[1 for x in range(51)] for y in range(51)], pad_width=1)

    return bitmap

# find house-battery configurations to later calculate shortest length
def make_configurations():

    configurations = []

    if CONFIG == 'random':
        while len(configurations) < number_options:

            legal_solution = False
            while not legal_solution:
                Battery._registry = []
                House._registry = []

                # load in all houses, batteries and borders
                bitmap = load_district(DISTRICT)

                # find a house-battery configuration
                legal_solution, combi_dict = find_random_combi()

            configurations.append(combi_dict)

        print("Found {} configurations".format(len(configurations)))
        print("\n")

    elif CONFIG == 'farthest':

        orders = []
        current_attempt = 0

        while current_attempt < number_options:

            legal_solution = False
            while not legal_solution:
                Battery._registry = []
                House._registry = []

                # load in all houses, batteries and borders
                bitmap = load_district(DISTRICT)

                # make a (shuffled based on current_attempt) new possible config order
                dist_list = make_dist_list(current_attempt, SWITCH)
                id_list = convert_dist_to_id(dist_list)

                # find a house-battery configuration
                legal_solution, combi_dict = find_closest_combi(dist_list)

                current_attempt += 1

                # make sure the search stops after number_option attempts,
                # even if no legal solutions are found
                if current_attempt == number_options:
                    legal_solution = True

            if id_list not in orders:
                configurations.append(combi_dict)
                orders.append(id_list)

        print("Found {} configurations".format(len(configurations)))
        print("Out of a possible {} options\n".format(number_options))

    return bitmap, configurations

# for each config, pull cables, find length, save the shortest
def connect_grid(bitmap, configurations):

    min_cable_length = 10**6

    # save a list of each length
    lengths = []

    # for each config, pull cables, find length, save the shortest
    for idx, combi_dict in enumerate(configurations):

        make_cable(combi_dict, bitmap)

        cablen = find_cable_length()
        lengths.append(cablen)

        # find the shortest configuration
        if cablen < min_cable_length:
            min_cable_length = cablen
            make_json(DISTRICT)

        # reset variables related to cables
        Cable._registry = []
        for bat in Battery._registry:
            bat.cables = []
        for hou in House._registry:
            hou.cable = "emptied"
        
    return lengths

def run_all():

    # find house-battery configurations to later calculate shortest length
    bitmap, configurations = make_configurations()

    # for each config, pull cables, find length, save the shortest in json
    lengths = connect_grid(bitmap, configurations)

    # save lengths of all options in a csv
    length_csv(lengths)

    # make a histogram of that csv
    csv_hist(DISTRICT, CONFIG, SWITCH, number_options)

    # for the shortest option, remake all objects from the saved json
    jason_remakes()

    # plot the best result
    draw_all_plot(DISTRICT, CONFIG, SWITCH)

    # draw_rep_plot doesnt work perfectly; not necessary for results anyway
    # draw_rep_plot(DISTRICT, CONFIG, SWITCH)

    # delete all object instances after an approach
    House._registry = []
    Battery._registry = []
    Cable._registry = []

    return

# RUN ALL CODE FOR ALL OPTIONS
for DISTRICT in [1, 2, 3]:
    print("START district: {}".format(DISTRICT))
    for CONFIG, SWITCH, number_options in config_switch_settings:
        print("{} -- {} \n".format(CONFIG, SWITCH))
        run_all()