from stare_tintar import stare_tintar

class BayesianEvaluator:
    def __init__(self):
        self.p_good = 0.5
        
        self.params = {
            "diff_piese": {
                "good": {-1: 0.2, 0: 0.5, 1: 0.8},
                "bad":  {-1: 0.8, 0: 0.5, 1: 0.2}
            },
            "diff_mobility": {
                "good": {-1: 0.3, 0: 0.5, 1: 0.7},
                "bad":  {-1: 0.7, 0: 0.5, 1: 0.3}
            },
            "diff_mori": {
                "good": {-1: 0.2, 0: 0.5, 1: 0.8},
                "bad":  {-1: 0.8, 0: 0.5, 1: 0.2}
            },
            "diff_potential": {
                "good": {-1: 0.3, 0: 0.5, 1: 0.7},
                "bad":  {-1: 0.7, 0: 0.5, 1: 0.3}
            }
        }

    def discretize(self, value):
        if value < 0:
            return -1
        elif value > 0:
            return 1
        else:
            return 0

    def calc_mobility(self, stare, player):

        free_positions = stare.pozitii_libere()
        

        if (player == 1 and stare.piese_ramase_jucator1 > 0) or \
           (player == 2 and stare.piese_ramase_jucator2 > 0):
            return len(free_positions)

        moves = 0
        pieces = stare.piese_jucator1 if player == 1 else stare.piese_jucator2
        for pos in pieces:
            for neighbor in stare.pozitii_adjacente[pos]:
                if neighbor in free_positions:
                    moves += 1
        return moves

    def calc_potential(self, stare, player):

        counter = 0
        player_positions = stare.piese_jucator1 if player == 1 else stare.piese_jucator2
        
        for (x, y, z) in stare.MORILE:
            count = 0
            empty = 0
            for pos in (x, y, z):
                if pos in player_positions:
                    count += 1
                elif pos in stare.pozitii_libere():
                    empty += 1
            if count == 2 and empty == 1:
                counter += 1
        
        return counter

    def eval_state(self, stare, ai_player=1):

        if ai_player == 1:
            diff_piese = len(stare.piese_jucator1) - len(stare.piese_jucator2)
            diff_mobility = self.calc_mobility(stare, 1) - self.calc_mobility(stare, 2)
            diff_mori = len(stare.piese_in_mori(stare.piese_jucator1)) - \
                        len(stare.piese_in_mori(stare.piese_jucator2))
            diff_potential = self.calc_potential(stare, 1) - self.calc_potential(stare, 2)
        else:

            diff_piese = len(stare.piese_jucator2) - len(stare.piese_jucator1)
            diff_mobility = self.calc_mobility(stare, 2) - self.calc_mobility(stare, 1)
            diff_mori = len(stare.piese_in_mori(stare.piese_jucator2)) - \
                        len(stare.piese_in_mori(stare.piese_jucator1))
            diff_potential = self.calc_potential(stare, 2) - self.calc_potential(stare, 1)
        

        dp = self.discretize(diff_piese)
        dm = self.discretize(diff_mobility)
        dmo = self.discretize(diff_mori)
        dpot = self.discretize(diff_potential)

        likelihood_good = self.p_good * (
            self.params["diff_piese"]["good"][dp] *
            self.params["diff_mobility"]["good"][dm] *
            self.params["diff_mori"]["good"][dmo] *
            self.params["diff_potential"]["good"][dpot]
        )
        likelihood_bad = (1 - self.p_good) * (
            self.params["diff_piese"]["bad"][dp] *
            self.params["diff_mobility"]["bad"][dm] *
            self.params["diff_mori"]["bad"][dmo] *
            self.params["diff_potential"]["bad"][dpot]
        )

        posterior_good = likelihood_good / (likelihood_good + likelihood_bad)
        return posterior_good

def alege_mutare_bayesian(stare, bayes_eval, ai_player=2):
    stari_posibile = list(stare.generare_stari_urmatoare())
    
    if not stari_posibile:
        return None 
    
    best_state = None
    best_prob = -1
    
    for s in stari_posibile:
        prob = bayes_eval.eval_state(s, ai_player=ai_player)
        if prob > best_prob:
            best_prob = prob
            best_state = s
    
    return best_state
