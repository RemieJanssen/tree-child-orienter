import numpy as np
import networkx as nx
import csv
import time
import argparse

from algorithms.TC_orientation_bruteforce_huber2024_phyloroot import tree_child_orient_huber_bruteforce_phyloroot
from algorithms.TC_orientation_bruteforce_huber2024 import tree_child_orient_huber_bruteforce
from algorithms.TC_orientation_fpt_huber2024 import tree_child_orient_huber_fpt_phyloroot
from algorithms.TC_orientation_heuristic import tree_child_orient_heuristic
from algorithms.TC_orientation import tree_child_orient

def start():
    global start_time
    start_time = time.perf_counter()

def end(tag="Elapsed time"):
    if "start_time" in globals():
       elapsed_time = time.perf_counter() - start_time
       print("{}: {:.9f} [sec]".format(tag, elapsed_time))
       return elapsed_time
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

def experiment(filename, orientation_algorithm):
    G = readcsv(filename)
    start()
    orientable = orientation_algorithm(G)
    elapsed_time = end()
    return elapsed_time, orientable

def cmd_parser():
    parser = argparse.ArgumentParser(
        description="finds the orientations of an undirected phylogenetic network that belong to a given class of directed networks."
    )
    parser.add_argument(
        "-f",
        "--file",
        help="input file with an undirected phylogenetic network as a adjacency matrix in csv format.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        help="An algorithm, choose from: HSP (Huber stupid phyloroot), HS (Huber stupid), HFPT (Huber FPT), H (Heuristic), and N (New).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    cmd_args = cmd_parser()
    algo_dict = {
        "HSP": tree_child_orient_huber_bruteforce_phyloroot,
        "HS": tree_child_orient_huber_bruteforce,
        "HFPT": tree_child_orient_huber_fpt_phyloroot,
        "H": tree_child_orient_heuristic,
        "N": tree_child_orient,
    }
    elapsed_time, orientable = experiment(cmd_args.file, algo_dict[cmd_args.algorithm])
    out_string = f"elapsed time: {elapsed_time}, orientable: {orientable}"
    print(out_string)
    if cmd_args.output:
        with open(cmd_args.output, "w+") as f:
            f.write(out_string)
