from phyloroot.main_cli import get_class_checker_and_chain_length
from phyloroot import ClassRootableStupid

def tree_child_orient_huber_bruteforce_phyloroot(G):
  # Run orientation algorithm Huber2024 Stupid
  ClassChecker, length = get_class_checker_and_chain_length("TC")
  orientations = ClassRootableStupid(G, ClassChecker)

  if orientations:
      return True
  return False
