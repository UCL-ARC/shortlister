from random import choice

def load_data():
    ...

def comparison():
    ...


def get_pair(object_list):
    object_1 = choice(object_list)
    object_2 = choice(object_list) 
    return (object_1, object_2)

def choose(candidates:tuple):
    choice = input()
    winner = None
    if choice == "r":
        winner = candidates[0]
    elif choice == "l":
        winner = candidates[1]
    else:
        pass
    save_results(candidates,winner)

def save_results(pair,winner):
    ...