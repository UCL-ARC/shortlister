from itertools import combinations
from typing import List

RESULT= {}

def comparison(list):
    """Starts the comparison process"""
    pairs = get_pair(list) # returns a list of pairs that can be used to compare

    for pair in pairs: 
        winner = choose(pair)
        save_results(pair,winner)
    # goes to the next pair

def get_pair(object_list):
    """Return every unique item pair in the list"""
    unique_pairs = list(combinations(object_list, 2))
    pairs_to_compare =[pair for pair in unique_pairs if pair not in RESULT]
    # then check against compared pairs in RESULTS
    # return not compared pairs
    return pairs_to_compare

def choose(candidates:tuple):
    choice = input()
    if choice == "r":
        winner = candidates[0]
    elif choice == "l":
        winner = candidates[1]
    return winner

def save_results(pair,winner):
    RESULT[set(pair)] = winner

def rank(list:List):
    # checking from result where the winners should be placed

    wins = {}
    
    for object in list:
        #award 1 point for every win
        score = RESULT.values().count(object)
        wins[object] = score

    ranked = list.sort(key=lambda item:wins[item],reverse=True)
    return ranked
    

    
# Ranking notes:

# if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs