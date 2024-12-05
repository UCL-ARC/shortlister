from itertools import combinations
from pathlib import Path
import pickle
from typing import Dict, List
from readchar import readkey

def comparison(list_to_rank, result):
    """Starts the comparison process."""
    # Queue is a list of pair that has not been compared yet
    queue = get_pair(list_to_rank, result)

    # Loop when there are still pairs to be compared in the queue
    while len(queue) > 0:
        # Remove the first pair in the queue and start the comparison
        pair = tuple(queue.pop(0))
        print(f"{pair[0]}[1] : {pair[1]}[2]")
        # 
        while True:
            choice = readkey()
            if choice in ["u","l","r"]:
                break
        # if the choice is undo
        if choice == "u" and result:
            # take the key and requeue the pair
            pair = result.popitem()[0]
            queue.insert(0,pair)
            continue
        # anything else is sent to be evaluated by another function
        else:
            winner = choose(choice,pair)
            save_results(frozenset(pair), winner, result)


def get_pair(list_to_rank, result):
    """Return every unique item pair in the list."""
    unique_pairs = combinations(list_to_rank, 2) # tuple pair is dependent on the list order
    # will skip pairs that are already compared
    pairs_to_compare = [pair for pair in unique_pairs if pair not in result]
    return pairs_to_compare

def choose(choice,candidates: tuple):
    """Get user choice of which object out of the pair they prefer."""
    if choice == "1":
        winner = candidates[0]
    elif choice == "2":
        winner = candidates[1]
    return winner


def save_results(pair, winner, result):
    """Save the pair comparison result to dictionary."""
    result[pair] = winner


def rank(list_to_rank: List, result: Dict):
    """Rank applicants.(Basic,inaccurate when there are ties)"""
    # checking from result where the winners should be placed

    wins = {}
    outcome = list(result.values())

    for object in list_to_rank:
        # award 1 point for every win
        score = outcome.count(object)
        wins[object] = score

    ranked = sorted(list_to_rank, key=lambda item: wins[item], reverse=True)
    save_rank(result,"ranked.pickle")
    return ranked

def save_rank(match_result, file: Path):
    """Save dictionary of the comparison result to file"""
    with open(file, "wb") as pickle_file:
        pickle.dump(match_result, pickle_file)

def get_existing_result(path:Path):
    if path.exists():
        with open(path, "rb") as pickle_file:
            result = pickle.load(pickle_file)
    else:
        result = {}
    return result
    

# Ranking notes:

# if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs d ect.

# bubblerank:
# addition of new items to already ranked list
# make a copy of the list, and swap items in that list to make the pair using bubble sort method, without changing the original list
