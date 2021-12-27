

""" Viterbi algorithm"""
def viterbi(A, B, delta,delta_index,  obs):
    # Iterate until there are no more observations
    oi = 1
    for o in obs:
        probs = list()
        # Calculate all possible probabilities 
        # with the help of step t-1 of delta
        for h1 in range(len(A[0])):
            element_probs = list()
            for h2 in range(len(A[0])):
                element_probs.append(delta[oi-1][h2]* A[h2][h1]* B[h1][int(o)])
            probs.append(element_probs)

        # Make new delta values from the max probabilties of timestep t
        
        pi = 0
        
        for prob in probs:
            delta[oi][pi] = max(prob)
            delta_index[oi-1][pi] = prob.index(max(prob))
            pi += 1
        # Add the corresponding backpointer
        oi += 1
        
    # Go through the viterbi trellis with the help of the pointers backwards
    # and find the most likely hidden state sequence
    hidden_state_sequence = list()
    end_hidden_state = delta[-1].index(max(delta[-1]))

    hidden_state_sequence.append(end_hidden_state)
    for idx in range(len(delta_index)-1,-1,-1):
        # Update hidden states from t -> 0
        hidden_state_sequence.insert(0, delta_index[idx][end_hidden_state])
        end_hidden_state = delta_index[idx][end_hidden_state]

    return hidden_state_sequence


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

    delta = [[float("-inf") for i in range(len(A[0]))] for j in range(len(obs))]
    delta_index = [[float("-inf") for i in range(len(A[0]))] for j in range(len(obs)-1)]
    #delta0 = [pi[0][i]*B[i][int(obs[0])] for i in range(len(pi[0]))]
    for i in range(len(pi[0])):
        delta[0][i] = pi[0][i]*B[i][int(obs[0])]
    hidden_sequence = viterbi(A, B, delta, delta_index ,obs[1:])
    print(" ".join([str(h) for h in hidden_sequence]))

main()