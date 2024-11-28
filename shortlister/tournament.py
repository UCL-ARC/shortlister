from itertools import combinations

RESULT= {}

def comparison(list):
    """"""
    pair = get_pair(list) # returns a list of pairs that can be used to compare
    winner = choose(pair)
    save_results(pair,winner)

def get_pair(object_list):
    """get every possible item pair in the list"""
    unique_pairs = list(combinations(object_list, 2))
    return unique_pairs

def choose(candidates:tuple):
    choice = input()
    if choice == "r":
        winner = candidates[0]
    elif choice == "l":
        winner = candidates[1]
    return winner

def save_results(pair,winner):
    RESULT[set(pair)] = winner

def rank(list):
    # checking from result where the winners should be placed
    # if object1 is winner, then it should be placed above object2 and all other objects that object2 won against ect.
    for key,value in RESULT:
        if key[value] == value:

            


    # rank placement

    
# Ranking

# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs