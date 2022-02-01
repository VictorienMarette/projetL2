import random

def random_int_list(n, bound):
    '''
    n : int size of the list
    bound : int max number in the list
    '''
    return [int(random.random()*bound) for i in range(n)]

def random_symetric_int_matrix(n, bound, null_diag=True):
    mat = [[] for i in range(n)]
    for i in range(n):
        li = random_int_list(n-i, bound)
        mat[i] += li.copy()
        for j in range(i+1, n):
            mat[j].append(li[j-i])

    if(null_diag):
        for i in range(n):
            mat[i][i] = 0

    return mat

def afficheMatrix(mat):
    print("[")
    for li in mat:
        print(li)
    print("]")