from phyloroot.main_cli import get_class_checker_and_chain_length
from phyloroot import LevelStuff

def tree_child_orient_huber_fpt_phyloroot(G):
  # Run orientation algorithm Huber2024 FPT
  ClassChecker, length = get_class_checker_and_chain_length("TC")
  orientations = LevelStuff(G, length, ClassChecker)

  if orientations:
      return True
  return False
