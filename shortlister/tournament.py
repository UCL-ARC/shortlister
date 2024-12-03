from itertools import combinations
from typing import Dict, List

def comparison(mylist,result):
    """Starts the comparison process"""
    pairs = get_pair(mylist,result)  # returns a list of pairs that can be used to compare
    for pair in pairs:
        print(f"{pair[0].name}[l] : {pair[1].name}[r]")
        winner = choose(pair)
        save_results(pair, winner,result)
    # goes to the next pair


def get_pair(mylist,result):
    """Return every unique item pair in the list"""
    unique_pairs = frozenset(combinations(mylist, 2)) # tuple pair is dependent on the list order
    pairs_to_compare = [pair for pair in unique_pairs if pair not in result]
    # then check against compared pairs in RESULTS
    # return not compared pairs
    return pairs_to_compare


def choose(candidates: tuple):
    choice = input()
    if choice == "r":
        winner = candidates[1]
    elif choice == "l":
        winner = candidates[0]
    return winner

def save_results(pair, winner,result):
    result[pair] = winner

def rank(mylist: List, result: Dict):
    """Rank applicants"""
    # checking from result where the winners should be placed

    wins = {}
    outcome = list(result.values())

    for object in mylist:
        # award 1 point for every win
        score = outcome.count(object)
        wins[object] = score
    
    ranked = sorted(mylist, key=lambda item: wins[item], reverse=True)
    return ranked


def save_rank(ranked_list):
    """Save result to file"""
    with open("ranked.csv") as file:
        file.write(ranked_list)


# Ranking notes:

# if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs d ect.
