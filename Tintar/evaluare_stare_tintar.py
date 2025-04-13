from stare_tintar import stare_tintar

# {'coef_piese': 0.9087442167730713, 'coef_mobility': 0.4770010908412682, 'coef_mori': 0.9276174199121775, 'coef_mills_potential': 0.2470996236439741}

class evaluare_stare_tintar:
    def __init__(self):
        self._coef_piese = 0.9087442167730713
        self._coef_mobility = 0.4770010908412682
        self._coef_mori = 0.9276174199121775
        self._coef_mills_potential = 0.2470996236439741

    def _calc_mobility(self, stare, player):
        free_positions = stare.pozitii_libere()
        if (player == 1 and stare.piese_ramase_jucator1 > 0) or (player == 2 and stare.piese_ramase_jucator2 > 0):
            return len(free_positions)
        moves = 0
        pieces = stare.piese_jucator1 if player == 1 else stare.piese_jucator2
        for pos in pieces:
            for neighbor in stare.pozitii_adjacente[pos]:
                if neighbor in free_positions:
                    moves += 1
        return moves

    def _calc_potential_mills(self, stare, player):
        counter = 0
        for (x, y, z) in stare.MORILE:
            player_positions = stare.piese_jucator1 if player == 1 else stare.piese_jucator2
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

    def evalueaza(self, stare):
        if len(stare.piese_jucator1) < 3:
            return -1000
        if len(stare.piese_jucator2) < 3:
            return 1000
        diff_piese = len(stare.piese_jucator1) - len(stare.piese_jucator2)
        diff_mobility = self._calc_mobility(stare, 1) - self._calc_mobility(stare, 2)
        mills1 = len(stare.piese_in_mori(stare.piese_jucator1))
        mills2 = len(stare.piese_in_mori(stare.piese_jucator2))
        diff_mori = mills1 - mills2
        potential1 = self._calc_potential_mills(stare, 1)
        potential2 = self._calc_potential_mills(stare, 2)
        diff_potential = potential1 - potential2
        score = (self._coef_piese * diff_piese +
                 self._coef_mobility * diff_mobility +
                 self._coef_mori * diff_mori +
                 self._coef_mills_potential * diff_potential)
        return score
