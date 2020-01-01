# -*- coding: utf-8 -*-

__author__ = "Nantha Kumar Sunder"
__version__ = "0.1.0"
__license__ = "MIT"

import numpy as np
import math
import matplotlib.pyplot as plt
import time

def tspread(add):
    # function to read .tsp file and store data in a list
    file = open(add, "r")
    i = 6
    tsp_file = file.readlines()
    coord = list()

    # storing each line until EOF
    while True:
        if tsp_file[i] == 'EOF\n':
            break
        temp_str = tsp_file[i].split()[1:]
        coord.append([int(temp_str[0]),int(temp_str[1])])
        i = i + 1

    return coord

def eucli_2d(coord1, coord2, tsp):
    # Function to calculate Euclidean Distance
    return int(math.sqrt((tsp[coord1-1][0]-tsp[coord2-1][0])**2 + (tsp[coord1-1][1]-tsp[coord2-1][1])**2))

def plot_points(coord, points, name):
    # Function to save the plot of the vertices, tour
    plt.scatter(np.array(coord)[:,0], np.array(coord)[:,1],color = 'k')
    plt.plot(np.array(coord)[points,0], np.array(coord)[points,1], color='r')
    plt.savefig(name)
    plt.close()
    return 0

def greedy_search(tsp_file, mst_list, parent_list):
    # function to Create MST tree
    while True:
        # Loop to add all the vertices to the tree
        weight = 10000
        node = 0

        # Brute Force loop to get closest node
        for j in mst_list:
            for i in range(len(tsp_file)):

                # Checking the current node is in mst list
                if i+1 not in mst_list and i+1 !=  j:
                    temp_weight = eucli_2d(i+1,j,tsp_file)

                    # Checking if the current node is closest
                    if temp_weight < weight:
                        weight = temp_weight
                        node = i+1
                        node_parent = j
        # Updating the parent
        parent_list[node-1] = node_parent
        mst_list.append(node)

        # Exiting the loop if all the vertices is added to the tree
        if len(mst_list) == len(tsp_file):
            break
    return parent_list, mst_list

def mst_cal(tsp_file):
    # Function to choose random edge and to call the greedy algorithm function
    # Choosing random edge
    node_list = np.arange(len(tsp_file))
    shuf = node_list.copy()
    np.random.shuffle(shuf)
    node1 = shuf[0]
    node2 = shuf[1]
    mst_list = list()
    mst_list.append(node1)
    mst_list.append(node2)

    # Calling greedy_search function
    parent_list = np.zeros(len(tsp_file))
    parent_list, mst_list = greedy_search(tsp_file, mst_list, parent_list)

    return parent_list

def dfs(tsp_file, parent_list):
    # Function to calculate depth first search to reduce
    stack = list()
    visited = list()
    start_node = np.where(parent_list == 0)[0]
    visited.append(start_node[0])
    stack.append(start_node[0])
    stack.append(start_node[1])
    visited.append(start_node[1])

    ## DFS algorithm
    while stack:
        current_node = stack[-1]

        ## check neighbouring node
        indexes = np.where(np.array(parent_list) == current_node + 1)[0]
        next_node_idx =[]

        # Adding the index to the Visited
        for index in indexes:
            if index in visited:
                continue
            else:
                stack.append(index)
                visited.append(index)
                next_node_idx = index
                break

        # IF child then go to next index
        if next_node_idx == []:
            stack.pop()
            continue

    return visited

def cal_total_distance(tour, tsp_file):
    # function to calculate the total distance travelled by the salesperson
    tour = np.array(tour) + 1
    total_weight = 0

    #Calculating the distacne
    for i in range(len(tour)-1):
        total_weight = total_weight + eucli_2d(tour[i],tour[i+1],tsp_file)
        if i == len(tour)-2:
            total_weight = total_weight + eucli_2d(tour[i+1],tour[0],tsp_file)
    return total_weight

def two_opt(tour, tsp_file):
    # Function to compute heuristics
    print("Inside Heuristics")
    total_weight = cal_total_distance(tour, tsp_file)
    new_weight = total_weight + 1

    # Choosing the node
    for i0 in range(len(tour)):
        # choosing the another node
        for j0 in range(len(tour)):

            # Choosing the nodes for Edge
            if i0 < len(tour) - 1:
                i1 = i0 + 1
            else:
                i1 = 0

            if j0 < len(tour) - 1:
                j1 = j0 + 1
            else:
                j1 = 0

            # Checking if the edges are adjacent
            if j0 == i0 or j0 == i1 or j1 == i0 or j1 == i1:
                continue
            else:
                # Checking if the improve the tour length
                new_tour = tour.copy()
                if j0 < i1:
                    new_tour[j0:i1+1] = new_tour[j0:i1+1][::-1]
                elif i0 < j1:
                    new_tour[i0:j1+1] = new_tour[i0:j1+1][::-1]
                new_weight = cal_total_distance(new_tour, tsp_file)
                if new_weight < total_weight:
                    tour = new_tour.copy()
                    total_weight = new_weight

    return tour

def file_write(tour,name, length, n):
    # function to write output file
    f_str = 'NAME : ' + name + '.out.tour\n'
    f_str = f_str + 'COMMENT : Tour for ' + name + '.tsp (' + str(length) +')\n'
    f_str = f_str + 'TYPE: TOUR\n'
    f_str = f_str + 'DIMENSION: ' + str(n) + '\n'
    f_str = f_str + 'TOUR_SELECTION\n'

    # loop to add the tours
    for i in tour:
        f_str = f_str + str(i+1) + '\n'

    f_str = f_str + '-1\nEOF\n'

    # iopening the file
    f = open(name + '.out.tour','w')

    # writing the file
    f.write(f_str)
    f.close()

    return 0

def given_data():
    # Function to compute MST for the given the Data
    option = input("Enter the any one option:\n 1. eil51\n 2. eil76\n 3. eil101\n---> ")
    tic = time.clock()
    np.random.seed(0)

    if option == '1':
        n = 51
        name = 'eil51'
        tsp_file = tspread("eil51.tsp")

    elif option =='2':
        n = 76
        name = 'eil76'
        tsp_file = tspread("eil76.tsp")

    else:
        n = 101
        name = 'eil101'
        tsp_file = tspread("eil101.tsp")

    # getting the parent list from the mst_cal
    parent_list = mst_cal(tsp_file)

    # computing the dfs
    tour = dfs(tsp_file, parent_list)

    # calulating the total distance
    total_weight = cal_total_distance(tour, tsp_file)
    print('Weight Without Heuristics:',total_weight)
    plot_points(tsp_file, tour,name + '.png')

    # Computing 2 opt
    tour = two_opt(tour, tsp_file)

    # computing the Total distance
    total_weight = cal_total_distance(tour, tsp_file)
    print('Weight With Heuristics:',total_weight)

    plot_points(tsp_file, tour, name + '_final' + '.png')

    mst_length = find_mst_length(parent_list, tsp_file)
    print('Mst Length:', mst_length)

    toc = time.clock()
    print('Time taken:',toc-tic)

    file_write(tour, name, total_weight, n)
    return 0

def find_mst_length(parent, tsp_file):
    # function to calculate mst length
    mst_length = 0
    for i in range(len(parent)):
        if parent[i] == 0:
            continue
        else:
            mst_length = mst_length + eucli_2d(i+1, int(parent[i]), tsp_file)
    return mst_length

def main():
    # main function
    given_data()

if __name__ == "__main__":
    main()
