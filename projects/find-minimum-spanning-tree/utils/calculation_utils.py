import itertools


def get_subsets(arr):
    return [sub for r in range(len(arr) + 1) for sub in itertools.combinations(arr, r)]