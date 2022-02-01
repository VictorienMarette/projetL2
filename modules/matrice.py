import random

def random_int_list(n, bound):
    '''
    n : int size of the list
    bound : int max number in the list
    '''
    return [int(random.random()*bound) for i in range(n)]

def random_int_matrix(n, bound, null_diag=True):
    '''
    n : int size of the sides of the matrix
    bound : int max number in the matrix
    null_diag : bool if true the matrix has null diagonal
    returns a rendom matrix
    '''
    if not null_diag:
        return [random_int_list(n,bound) for i in range(n)]
    return [random_int_list(i,bound) + [0] + random_int_list(n - i - 1,bound) for i in range(n)]

def random_symetric_int_matrix(n, bound, null_diag=True):
    '''
    return a random symetric int matrix
    n : int size of the matrix
    bound : int max number in the matrix
    null_diag : True if the diagonale must be empty
    '''
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

def random_oriented_int_matrix(n, bound,null_diag=True):
    '''
    n : int size of the sides of the matrix
    bound : int max number in the matrix
    null_diag : bool if true the matrix has null diagonal
    returns a rendom oriented matrix
    '''
    l = random_int_matrix(n, bound, null_diag=null_diag)
    for i in range(1,n):
        for j in range(0,i):
            if l[i][j] != 0 and l[j][i] != 0:
                if (int(random.random()*2) == 1):
                    l[i][j] = 0
                else:
                    l[j][i] = 0 
    return l

def random_triangular_int_matrix(n, bound, null_diag=True):
    '''
    n : int size of the sides of the matrix
    bound : int max number in the matrix
    null_diag : bool if true the matrix has null diagonal
    returns a rendom upper triangular matrix
    '''
    if not null_diag:
        return [[0 for j in range(i)] + random_int_list(n - i,bound) for i in range(n)]
    return [[0 for j in range(i+1)] + random_int_list(n - i - 1,bound) for i in range(n)]

def afficheMatrix(mat):
    print("[")
    for li in mat:
        print(li)
    print("]")