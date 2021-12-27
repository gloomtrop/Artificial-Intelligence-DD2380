"""Code inspired of pseudo code 'A Revealing Introduction to Hidden Markov Models' by Mark Stamp"""

import math
""" Forward algorithm to compute alpha"""
def forward(A, B, pi, obs):
    N = len(A[0])
    T = len(obs)
    c = [0 for i in range(T)]
    alpha = [[0 for i in range(N)] for t in range(T) ]
    for i in range(N):
        alpha[0][i] = pi[0][i]* B[i][int(obs[0])]
        c[0] += alpha[0][i]
    
    c[0] = 1/c[0]
    for i in range(N):
        alpha[0][i] *= c[0]
    for t in range(1,T):
        for i in range(N):
            for j in range(N):
                alpha[t][i] +=  alpha[t-1][j]*A[j][i]
            alpha[t][i] *= B[i][int(obs[t])]
            c[t] += alpha[t][i]
        c[t] = 1/c[t]
        for i in range(N):
            alpha[t][i] *= c[t]
    return alpha, c

"""Backward algorithm to compute beta"""
def backward(A, B, obs, c):
    N = len(A[0])
    T = len(obs)
    beta = [[0 for i in range(N)] for t in range(T)]
    for i in range(N):
        beta[-1][i] = c[-1]
    for t in range(T-2, -1, -1):
        for i in range(N):
            for j in range(N):
                beta[t][i] += A[i][j]*B[j][int(obs[t+1])]*beta[t+1][j]
            beta[t][i] *= c[t]
    return beta

""" Compute di-gamma and gamma """
def computeGamma(A, B, obs, alpha, beta):
    N = len(A[0])
    T = len(obs)
    digamma = [[[0 for i in range(N)] for _ in range(N)] for _ in range(T)]
    gamma = [[0 for i in range(N)] for t in range(T)]
    
    for t in range(T-1):
        for i in range(N):
            for j in range(N):
                digamma[t][i][j] = alpha[t][i]*A[i][j]*B[j][int(obs[t+1])]*beta[t+1][j]
                gamma[t][i] += digamma[t][i][j]
    
    for i in range(N):
        gamma[-1][i] = alpha[-1][i]

    return digamma, gamma

""" Estimate A, B, pi with the help of di-gamma and gamma"""
def reEstimate(A, B, pi, obs, digamma, gamma):
    N = len(A[0])
    T = len(obs)
    M = len(B[0])
    # Re-estimate pi
    for i in range(N):
        pi[0][i] = gamma[0][i]
    
    # Re-estimate A
    for i in range(N):
        denom = 0
        for t in range(T-1):
            denom += gamma[t][i]
        for j in range(N):
            numer = 0
            for t in range(T-1):
                numer += digamma[t][i][j]
            A[i][j] = numer/denom

    # Re-estimate B
    for i in range(N):
        denom = 0
        for t in range(T):
            denom = denom + gamma[t][i]
        for j in range(M):
            numer = 0
            for t in range(T):
                if int(obs[t]) == j:
                    numer += gamma[t][i]
            B[i][j] = numer/denom
    
    return A, B, pi
    
""" Baum-Welch estimation model"""
def baumWelch(A, B, pi, obs):
    maxIters = 120
    iters = 0
    oldLogProb = float("-inf")
    logProb = -100000 
    while iters < maxIters and logProb - oldLogProb> 10e-7:

        alpha, c = forward(A, B, pi, obs)
        beta = backward(A, B, obs, c)
        digamma, gamma = computeGamma(A, B, obs,alpha, beta)
        A, B, pi = reEstimate(A, B, pi, obs, digamma, gamma)

        # Last
        oldLogProb = logProb
        logProb = 0
        for t in range(len(obs)):
            logProb += math.log(c[t])
        iters += 1
        logProb = -logProb
    # print(iters)
    return A, B, pi

""" Flatten matrix """
def flatten(M):
    return [i for sub in M for i in sub]


def main():
    """ Process input data"""
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
    
    # A =[[0.54, 0.26, 0.20], [0.19, 0.53, 0.28], [0.22, 0.18, 0.6]]
    # B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27],[0.19, 0.21,  0.15,0.45]]
    # pi = [[0.3, 0.2, 0.5]]
    A, B, pi = baumWelch(A, B, pi, obs)

    """ Output """
    print(len(A), len(A), end = " ")
    print(" ".join([str(h) for h in flatten(A)]))
    print(len(B), len(B[0]), end = " ")
    print(" ".join([str(h) for h in flatten(B)]))


main()