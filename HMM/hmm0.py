def matrixMult(A, B):
    AB = list()
    for i in range(len(A)):
        ab = list()
        for j in range(len(B[0])):
            ab.append(0)
        AB.append(ab)

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                AB[i][j] += A[i][k] * B[k][j]
    return AB

def nextDist(A, B, pi):
    AB = matrixMult(A, B)
    e = matrixMult(pi, AB)
    return e


def main():


    # A, B, pi = readFile(args[1])
    sample = """4 4 0.2 0.5 0.3 0.0 0.1 0.4 0.4 0.1 0.2 0.0 0.4 0.4 0.2 0.3 0.0 0.5
4 3 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.2 0.6 0.2
1 4 0.0 0.0 0.0 1.0"""
    sample_out = """1 3 0.3 0.6 0.1
"""
    A = list()
    B = list()
    pi = list()
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
        n, m = int(tmp[0]), int(tmp[1])
        tmp = tmp[2:]
        for i in range(n):
            if k==0:
                A.append(tmp[i*m:(i+1)*m])
            if k==1:
                B.append(tmp[i*m:(i+1)*m])
            if k== 2:
                pi.append(tmp[i*m:(i+1)*m])
        k += 1
        if k==3:
            break
    e = nextDist(A,B,pi)

    out = str(len(e)) + " " + str(len(e[0]))
    for i in e[0]:
        out += " " + str(i)
    
    print(out, end="")

    # for i in sys.stdin:
    # ab = i.split()
    # a = int(ab[0])
    # b = int(ab[1])
    # # Solve the test case and output the answer
main()