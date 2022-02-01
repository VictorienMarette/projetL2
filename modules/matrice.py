import random

def random_int_list(n, bound):
    '''
    n : int size of the list
    bound : int max number in the list
    '''
    return [int(random.random()*bound) for i in range(n)]

