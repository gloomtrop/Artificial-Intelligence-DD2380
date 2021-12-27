# def matrixMult(A, B):
#     AB = list()
#     for i in range(len(A)):
#         ab = list()
#         for j in range(len(B[0])):
#             ab.append(0)
#         AB.append(ab)

#     for i in range(len(A)):
#         for j in range(len(B[0])):
#             for k in range(len(B)):
#                 AB[i][j] += A[i][k] * B[k][j]
#     return AB

""" elementwiseMult element by element"""
def elementwiseMult(A, B):
    AB = list()
    for i, j in zip(A,B):
        AB.append(i*j)
    return AB

""" Get column of a specific matrix"""
def getCol(M, col):
    colVector = list()
    for row in M:
        colVector.append(row[col])
    return colVector

""" Recursivley calculate new alpha"""
# def forward(A, B, alpha, obs):

#     # For every observation, sum all the alphas nodes for the corresponding depth 
#     for o in obs:
#         aA = [sum(elementwiseMult(alpha, getCol(A, i))) for i in range(len(A[0]))]
#         aAB = elementwiseMult(aA, getCol(B, int(o)))
#         alpha = aAB
#     return alpha

def forward(A, B, pi, obs):
    N = len(A[0])
    T = len(obs)
    #c = [0 for i in range(T)]
    alpha = [[0 for i in range(N)] for t in range(T) ]
    for i in range(N):
        alpha[0][i] = pi[0][i]* B[i][int(obs[0])]
        #c[0] += alpha[0][i]
    
    #c[0] = 1/c[0]
    # for i in range(N):
    #     alpha[0][i] = alpha[0][i]*c[0]

    for t in range(1,T):
        for i in range(N):
            for j in range(N):
                alpha[t][i] += alpha[t-1][j]*A[j][i]
            alpha[t][i] *= B[i][int(obs[t])]
        #     c[t] = c[t] + alpha[t][i]
        # c[t] = 1/c[t]
        # for i in range(N):
        #     alpha[t][i] *= c[t]
    #return alpha, c
    return alpha

def main():
    """# Process input data"""
    A, B, pi, obs = list(), list(), list(), list()

    k = 0
    sample = input()
    txt = sample
    while sample:
        try:
            sample = input()
            txt += "\n"+sample
        except EOFError:
            break
    for line in txt.split("\n"):
        tmp = list(map(float,line.strip().split()))
        if k == 3:
            n = int(tmp[0])
            tmp = tmp[1:]
        else:
            n, m = int(tmp[0]), int(tmp[1])
            tmp = tmp[2:]
        for i in range(n):
            if k==0:
                A.append(tmp[i*m:(i+1)*m])
            if k==1:
                B.append(tmp[i*m:(i+1)*m])
            if k== 2:
                pi.append(tmp[i*m:(i+1)*m])
            if k== 3:
                obs.append(tmp[i])
        k += 1
        if k==4:
            break
    
    """START ALGORITHM"""
    alphas = forward(A, B, pi, obs)
    print(sum(alphas[-1]))
main()