from random import choice

RESULT= {}

def comparison(list):
    pair = get_pair(list)
    winner = choose(pair)
    save_results(pair,winner)

def get_pair(object_list):
    object_1 = choice(object_list)
    object_2 = choice(object_list) 
    return (object_1, object_2)

def choose(candidates:tuple):
    choice = input()
    if choice == "r":
        winner = candidates[0]
    elif choice == "l":
        winner = candidates[1]
    return winner

def save_results(pair,winner):
    RESULT[set(pair)] = winner