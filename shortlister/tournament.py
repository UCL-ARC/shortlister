from copy import deepcopy
from itertools import combinations
from pathlib import Path
import pickle
from typing import Dict, List


def comparison(mylist, result):
    """Starts the comparison process"""
    pairs = get_pair(
        mylist, result
    )  # returns a list of pairs that can be used to compare
    for pair in pairs:
        print(f"{pair[0].name}[l] : {pair[1].name}[r]")
        print(f"{[(criterion.name,score) for criterion,score in pair[0].scores]}   {[(criterion.name,score) for criterion,score in pair[1].scores]}")
        print(f"{pair[0].notes}   {pair[1].notes}")

        winner = choose(pair)
        save_results(pair, winner, result)
    # goes to the next pair


def get_pair(mylist, result):
    """Return every unique item pair in the list"""
    unique_pairs = frozenset(
        combinations(mylist, 2)
    )  # tuple pair is dependent on the list order
    pairs_to_compare = [pair for pair in unique_pairs if pair not in result]
    # then check against compared pairs in RESULTS
    # return uncompared pairs
    return pairs_to_compare


# wip
def get_pair_ver2(mylist, result):
    # assume list is ranked by score from high to low, start with the highest scored
    index = 0
    pair_index = 1

    # get a pair of first object with the object next in the list
    # make the comparison, and the next pair will be the one that didnt win plus the next index in the list

    while True:
        pair = frozenset(mylist[index], mylist[pair_index])
        winner = choose(pair,result)
        if winner == mylist[index]:
            index += 1
            pair_index += 1
            pair = frozenset(mylist[index], mylist[pair_index])
        elif winner == mylist[index + 1]:
            pair_index += 1
            pair = frozenset(mylist[index], mylist[pair_index])


def choose(candidates: tuple):
    while True:
        try:
            choice = input()
            if choice == "r":
                winner = candidates[1]
            elif choice == "l":
                winner = candidates[0]
            return winner
        except Exception as e:
            print(f"{e}:selection must be r or l")


def save_results(pair, winner, result):
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
    save_rank(result,"ranked.pickle")
    return ranked

def bubble_rank(original_list,result):
    mylist = deepcopy(original_list)
    # outer loop to iterate through the list n times
    for n in range(len(mylist)-1,0,-1):
        
        # to see if any swaps happens
        swapped = False  

        # comparing adjacent items
        for i in range(n):
            print((mylist[i].name,mylist[i+1].name))

            # if the pair has been compared before, use the past result
            if frozenset((mylist[i],mylist[i+1])) in result:
                winner = result[frozenset((mylist[i],mylist[i+1]))]
            else:
                # if that is not the case, then user chooses which item is better
                winner = choose((mylist[i],mylist[i+1]))

            if winner == mylist[i+1]:
                # swap items if next index is better
                mylist[i], mylist[i+1] = mylist[i+1], mylist[i]
                # mark that a swap has occurred
                swapped = True
            save_results(frozenset((mylist[i],mylist[i+1])),winner,result)
            print([object.name for object in mylist])

        # end loop if no swap happens during an iteration
        if not swapped:
            print([object.name for object in mylist])
            break

def save_rank(match_result, file: Path):
    """Save dictionary of the comparison result to file"""
    with open(file, "wb") as pickle_file:
        pickle.dump(match_result, pickle_file)


def open_existing_result(file: Path):
    with open(file, "rb") as pickle_file:
        return pickle.load(pickle_file)


# Ranking notes:

# if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs d ect.

# bubblerank:
# addition of new items to already ranked list
# make a copy of the list, and swap items in that list to make the pair using bubble sort method, without changing the original list
