import networkx as nx
import itertools
from phyloroot.main_cli import get_class_checker_and_chain_length
from phyloroot import LevelStuff, ClassAllNetworks, OrientationAlgorithmBinary

from unittest import mock


def NewRootAtEdge(network,rootEdge,min_cycle,ClassChecker=ClassAllNetworks):
    noOfReticulations = len(network.edges)-len(network.nodes)+1

    # Select one vertex from each minimal cycle
    for reticulations in itertools.product(*min_cycle):
        set_of_reticulations = set(reticulations)
        if len(set_of_reticulations) != noOfReticulations:
          continue
        result = OrientationAlgorithmBinary(network,rootEdge,set_of_reticulations)
        if result and ClassChecker(result):
            return reticulations
    return False

def NewClassRootableStupid(network,ClassChecker=ClassAllNetworks):
    rootings = dict()
    # Array for storing minimal cycles
    min_cycle = nx.minimum_cycle_basis(network)
    for e in network.edges:
        result = NewRootAtEdge(network,e,min_cycle,ClassChecker)
        if result:
            rootings[e]=result
    return rootings

def tree_child_orient_hybrid(G):
  # Run orientation algorithm Huber2024 FPT
  ClassChecker, length = get_class_checker_and_chain_length("TC")
  with mock.patch("phyloroot.rooting.ClassRootableStupid", NewClassRootableStupid):
    orientations = LevelStuff(G, length, ClassChecker)

  if orientations:
      return True
  return False