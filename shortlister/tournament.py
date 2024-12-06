from itertools import combinations
from pathlib import Path
import pickle
from typing import Dict, List
from readchar import readkey

COMPARISON_RESULT_FILE_NAME = "ranked.pickle"

def comparison(list_to_rank, result: Dict=None):
    """Starts pair comparison for a list of items.
    The result parameter could be dictionary with existing results or empty dictionary"""
    print("TOURNAMENT COMPARISON")
    print()

    # start with an empty dict if we don't have existing results
    if result is None:
        result = {}

    # Queue is a list of pairs that have not been compared yet
    queue = get_pair(list_to_rank, result)

    # Loop while there are still pairs to be compared in the queue
    while len(queue) > 0:
        # Remove the first pair in the queue and start the comparison
        pair = queue.pop(0)
        first, second = tuple(pair)

        print(f"1. {first}")
        print(f"2. {second}")
        print()

        print("1 OR 2?")
        print()

        # Limits key choice to "u", "1", "2" so there is no need for exception checking
        while True:
            choice = readkey()
            if choice in ["1", "2", "q"] or choice == "u" and result:
                break

        if choice == "q":
            print("EXITING TOURNAMENT COMPARISON")
            print()
            return
        # if undo last choice
        elif choice == "u":
            # take the key and requeue the pair
            pair = result.popitem()[0]
            queue.insert(0, pair)
        # otherwise it can be evaluate by choose() function to get the winner, and the result is saved
        else:
            winner = choose(choice, (first, second))
            save_results(pair, winner, result)

    # all comparisons done
    return result


def get_pair(list_to_rank, result):
    """Return every unique item pair in the list."""
    # Pairs are saved as frozenset here so that if order of list_to_rank is changed there won't be duplication pairs since "A","B" will be same as "B"","A"
    unique_pairs = [frozenset(pair) for pair in combinations(list_to_rank, 2)]

    # Only provide combinations that are not compared yet
    pairs_to_compare = [pair for pair in unique_pairs if pair not in result]
    return pairs_to_compare


def choose(choice, candidates: tuple):
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
        # Count how many wins an object got
        score = outcome.count(object)
        # create an entry in wins dictionary of the object and the score it earned
        wins[object] = score

    # sort the list by highest scored to lowest
    ranked = sorted(list_to_rank, key=lambda item: wins[item], reverse=True)

    # save the result to pickle file
    save_rank(result, Path(COMPARISON_RESULT_FILE_NAME))
    return ranked


def save_rank(match_result, file: Path):
    """Save dictionary of the comparison result to file"""
    with open(file, "wb") as pickle_file:
        pickle.dump(match_result, pickle_file)


def get_existing_result(path: Path):
    # Checks if there is existing result data
    if path.exists():
        with open(path, "rb") as pickle_file:
            result = pickle.load(pickle_file)
    # If not, start a fresh comparison record
    else:
        result = {}
    return result
