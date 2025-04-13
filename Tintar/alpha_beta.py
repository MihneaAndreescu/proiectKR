from stare_tintar import stare_tintar
from evaluare_stare_tintar import evaluare_stare_tintar

def terminal(stare):
    if stare.piese_ramase_jucator1 > 0 or stare.piese_ramase_jucator2 > 0:
        return False
    if len(stare.piese_jucator1) < 3 or len(stare.piese_jucator2) < 3:
        return True
    if not list(stare.generare_stari_urmatoare()):
        return True
    return False


def alpha_beta(stare, adancime, evaluator, jucator_curent, alpha, beta):
    if adancime == 0 or terminal(stare):
        return evaluator.evalueaza(stare), stare
    
    stari_posibile = list(stare.generare_stari_urmatoare())

    if jucator_curent == 1:
        best_val = -float("inf")
        best_stare = None
        for s in stari_posibile:
            valoare, _ = alpha_beta(s, adancime - 1, evaluator, 2, alpha, beta)
            if valoare > best_val:
                best_val = valoare
                best_stare = s
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
        return best_val, best_stare
    else:
        best_val = float("inf")
        best_stare = None
        for s in stari_posibile:
            valoare, _ = alpha_beta(s, adancime - 1, evaluator, 1, alpha, beta)
            if valoare < best_val:
                best_val = valoare
                best_stare = s
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_stare