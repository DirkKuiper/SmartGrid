# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_combi divides houses over batteries without overflowing their capacity

import random

from classes.house import House
from classes.battery import Battery

from algorithms.algo_astar import manhattan_distance


# randomly find a house-battery configuration that is legal
def find_random_combi():

    # combi dict is the dict in which to save the config
    combi_dict = dict()

    # make empty lists for each bat to save houses in later
    for bat in Battery._registry:
        combi_dict[bat] = []

    random_house_list = random.sample(House._registry, 150)
    for hou in random_house_list:

        while not hou.connected:

            random_battery_list = random.sample(Battery._registry, 5)
            for bat_to_cnct in random_battery_list:

                if hou.connected is False:
                    # if capacity available, connect and lower available cap
                    if bat_to_cnct.av_cap >= hou.maxoutput:
                        bat_to_cnct.av_cap -= hou.maxoutput
                        bat_to_cnct.connected_to.append(hou)
                        hou.connected = True

            if hou.connected is False:
                return False, combi_dict

        combi_dict[bat_to_cnct].append(hou)

    return True, combi_dict


# make a list of the order of all id's of the hous and bats for readability
def convert_dist_to_id(dist_list):
    id_list = []

    # for each combi of hou-bat
    for hou_bat_com in dist_list:
        bat_id_list = []
        # for each bat
        for idx in range(5):
            # add its id to a list
            bat_id_list.append(hou_bat_com[1][idx][0])

        id_list.append([hou_bat_com[0][0], bat_id_list])

    return id_list


# key for sorting the batteries per house
def key_bats(elem):
    return elem[2]


# key for sorting the houses on closest bat
def key_hous(elem):
    return elem[1][0][2]


# make a (each time shuffled) list of hou-bat combi's sorted on distance
# NOTE: if we want to go from far->close, add reverse=True in both sorteds
def make_dist_list(attempt, switch_what):
    dist_list = []

    for hou in House._registry:
        bat_dist = []
        for bat in Battery._registry:
            dist = manhattan_distance([hou.x, hou.y], [bat.x, bat.y])
            bat_dist.append([bat.id, bat, dist])
        dist_list.append([[hou.id, hou], sorted(
                    bat_dist, key=key_bats, reverse=True)])

    dist_list = sorted(dist_list, key=key_hous, reverse=True)

    # switch both batteries and houses
    if switch_what == 'both':
        for i in range(attempt):
            # every attempt, move a battery to the back
            dist_list[i % 150][1] = (dist_list[i % 150][1][1:] +
                                     [dist_list[i % 150][1][0]])

            # every 5 attempts, move a house to the back
            if i % 5 == 0 and i != 0:
                dist_list = dist_list[1:] + [dist_list[0]]

    # switch only houses
    elif switch_what == 'only houses':
        for i in range(attempt):
            dist_list = dist_list[1:] + [dist_list[0]]

    return dist_list


# for (semi-) ordered list of hou-bat-dist combi's
# make possible configurations
def find_closest_combi(dist_list):

    # combi dict is the dict in which to save the config
    combi_dict = dict()

    # make empty lists for each bat to save houses in later
    for bat in Battery._registry:
        combi_dict[bat] = []

    for comb in dist_list:
        hou = comb[0][1]
        bats = comb[1]

        while not hou.connected:
            for bat_to_cnct in bats:
                bat_to_cnct = bat_to_cnct[1]

                if hou.connected is False:
                    # if capacity available, connect and lower available cap
                    if bat_to_cnct.av_cap >= hou.maxoutput:
                        bat_to_cnct.av_cap -= hou.maxoutput
                        bat_to_cnct.connected_to.append(hou)
                        hou.connected = True

            if hou.connected is False:
                return False, combi_dict

        combi_dict[bat_to_cnct].append(hou)

    return True, combi_dict