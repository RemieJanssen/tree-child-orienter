import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import csv
import time

from phyloroot.main_cli import get_class_checker_and_chain_length, LevelStuff
from phyloroot import ClassRootableStupid

def start():
    global start_time
    start_time = time.perf_counter()

def end(tag="Elapsed time"):
    if "start_time" in globals():
       print("{}: {:.9f} [sec]".format(tag, time.perf_counter() - start_time))
    else:
       print("Function start is not called.")

# Function readcsv
def readcsv(filename):
    distance_matrix = []
    with open(filename + '.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')  # Specify the delimiter
        for row in csv_reader:
            row = [float(value) for value in row]
            distance_matrix.append(row)
    G = nx.from_numpy_array(np.array(distance_matrix))
    return G

# Input

filename = input("File Name: ")
start()
G = readcsv(filename)

# Run orientation algorithm Huber2024 Stupid
ClassChecker, length = get_class_checker_and_chain_length("TC")
orientations = ClassRootableStupid(G, ClassChecker)

if orientations:
    root_edge = next(iter(orientations))
    reticulations = orientations[root_edge]
    N2 = OrientationAlgorithmBinary(G, root_edge, reticulations)
    v_color = ['lightblue' if N2.in_degree(v) == 1 else 'red' if N2.in_degree(v) == 2 else 'lightgreen' for v in N2.nodes()]
    end()
    nx.draw(N2, pos=nx.kamada_kawai_layout(N2), with_labels=True, node_size=100, font_size=8, arrows=True, node_color=v_color)
    plt.savefig(filename + '_BF.pdf', format='pdf')  # Image format (here saved as pdf)
    plt.show()
    print("TC-Orientability: YES")
else: # If orientation not possible, output ‘NO’.
    end()
    print("TC-Orientability: NO")

