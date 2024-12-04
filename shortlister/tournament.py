from itertools import combinations
from pathlib import Path
import pickle
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
    # return uncompared pairs
    return pairs_to_compare


def get_pair_ver2(mylist,result):
    # assume list is ranked by score from high to low, start with the highest scored
    index = 0
    pair_index = 1

    # get a pair of first object with the object next in the list
        # make the comparison, and the next pair will be the one that didnt win, and the next index

    while True:
        pair = frozenset(mylist[index],mylist[pair_index])
        try: 
            choice = input("r or l")
            if choice == "r":
                winner = pair[1]
            elif choice == "l":
                winner = pair[0]
        except Exception:
            print("selection must be r or l")
        if winner == mylist[index]:
            index += 1
            pair_index += 1
            pair = frozenset(mylist[index],mylist[pair_index])
        elif winner == mylist[index+1]:
            pair_index += 1
            pair = frozenset(mylist[index],mylist[pair_index])
            return pair




def choose(candidates: tuple):
    while True:
        try: 
            choice = input()
            if choice == "r":
                winner = candidates[1]
            elif choice == "l":
                winner = candidates[0]
            return winner
        except Exception:
            print("selection must be r or l")

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
    save_rank(result)
    return ranked

def save_rank(match_result,file:Path):
    """Save dictionary of the comparison result to file"""
    with open(file,"wb") as pickle_file:
        pickle.dump(match_result,pickle_file)

def open_existing_result(file:Path):
    with open(file,"rb") as pickle_file:
        return pickle.load(pickle_file)
    
# Ranking notes:

# if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs d ect.
