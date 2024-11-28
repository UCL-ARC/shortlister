

RESULT= {}

def comparison(list):
    pair = get_pair(list)
    winner = choose(pair)
    save_results(pair,winner)

def get_pair(object_list):
    """get every possible item pair in the list"""
    pairing = []
    for item in object_list:
        comparison_list = [opponent for opponent in object_list if not item]
        for opponent in comparison_list:
            if item and opponent in RESULT.keys():
                continue
            else:
                pairing.append(set(item,opponent))
    return pairing

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
    # 
    for key,value in RESULT:
        if key[value] == value:
            ...


    # rank placement

    
# Ranking

# elo system?
# total number of applicants
# imported list is sorted based on score
# a vs b, b vs c, c vs