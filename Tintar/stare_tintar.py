class stare_tintar:
    pozitii_adjacente = {
        1: [2, 10],
        2: [1, 3, 5],
        3: [2, 15],
        4: [5, 11],
        5: [2, 4, 6, 8],
        6: [5, 14],
        7: [8, 12],
        8: [5, 7, 9],
        9: [8, 13],
        10: [1, 11, 22],
        11: [4, 10, 12, 19],
        12: [7, 11, 16],
        13: [9, 14, 18],
        14: [6, 13, 15, 21],
        15: [3, 14, 24],
        16: [12, 17],
        17: [16, 18, 20],
        18: [13, 17],
        19: [11, 20],
        20: [17, 19, 21, 23],
        21: [14, 20],
        22: [10, 23],
        23: [20, 22, 24],
        24: [15, 23]
    }

    MORILE = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
        (13, 14, 15),
        (16, 17, 18),
        (19, 20, 21),
        (22, 23, 24),
        (1, 10, 22),
        (2, 5, 8),
        (3, 15, 24),
        (4, 11, 19),
        (6, 14, 21),
        (7, 12, 16),
        (9, 13, 18),
        (17, 20, 23)
    ]

    def __init__(self, piese_jucator1=None, piese_jucator2=None,
                 piese_ramase_jucator1=9, piese_ramase_jucator2=9,
                 jucator_curent=1):
        self.piese_jucator1 = set(piese_jucator1) if piese_jucator1 else set()
        self.piese_jucator2 = set(piese_jucator2) if piese_jucator2 else set()
        self.piese_ramase_jucator1 = piese_ramase_jucator1
        self.piese_ramase_jucator2 = piese_ramase_jucator2
        self.jucator_curent = jucator_curent

    def __repr__(self):
        return (f"stare_tintar(J1={sorted(self.piese_jucator1)}, "
                f"J2={sorted(self.piese_jucator2)}, "
                f"r1={self.piese_ramase_jucator1}, r2={self.piese_ramase_jucator2}, "
                f"curent={self.jucator_curent})")

    def este_in_faza_de_plasare(self) -> bool:
        if self.jucator_curent == 1:
            return self.piese_ramase_jucator1 > 0
        else:
            return self.piese_ramase_jucator2 > 0

    def pozitii_libere(self) -> set:
        toate_pozitiile = set(self.pozitii_adjacente.keys())
        return toate_pozitiile - self.piese_jucator1 - self.piese_jucator2

    def _schimba_jucatorul(self):
        self.jucator_curent = 1 if self.jucator_curent == 2 else 2

    def _copie_stare(self):
        return stare_tintar(
            piese_jucator1=self.piese_jucator1.copy(),
            piese_jucator2=self.piese_jucator2.copy(),
            piese_ramase_jucator1=self.piese_ramase_jucator1,
            piese_ramase_jucator2=self.piese_ramase_jucator2,
            jucator_curent=self.jucator_curent
        )

    def a_format_moara(self, poz_noua, piese_jucator):
        for (x, y, z) in self.MORILE:
            if poz_noua in (x, y, z):
                if {x, y, z}.issubset(piese_jucator):
                    return True
        return False

    def piese_in_mori(self, piese_jucator):
        rezultat = set()
        for (x, y, z) in self.MORILE:
            if x in piese_jucator and y in piese_jucator and z in piese_jucator:
                rezultat.update([x, y, z])
        return rezultat

    def generare_stari_urmatoare(self):
        stari_noi = set()
        piese_curent = self.piese_jucator1 if self.jucator_curent == 1 else self.piese_jucator2
        piese_adv = self.piese_jucator2 if self.jucator_curent == 1 else self.piese_jucator1
        if self.este_in_faza_de_plasare():
            for poz_libera in self.pozitii_libere():
                stare_noua = self._copie_stare()
                if self.jucator_curent == 1:
                    stare_noua.piese_jucator1.add(poz_libera)
                    stare_noua.piese_ramase_jucator1 -= 1
                else:
                    stare_noua.piese_jucator2.add(poz_libera)
                    stare_noua.piese_ramase_jucator2 -= 1
                if stare_noua.a_format_moara(
                        poz_libera,
                        stare_noua.piese_jucator1 if self.jucator_curent == 1
                        else stare_noua.piese_jucator2):
                    stari_dupa_lovitura = stare_noua._genereaza_stari_dupa_lovitura()
                    for s in stari_dupa_lovitura:
                        s._schimba_jucatorul()
                        stari_noi.add(s)
                else:
                    stare_noua._schimba_jucatorul()
                    stari_noi.add(stare_noua)
        else:
            for pozitie in piese_curent:
                for vecin in self.pozitii_adjacente[pozitie]:
                    if vecin not in self.piese_jucator1 and vecin not in self.piese_jucator2:
                        stare_noua = self._copie_stare()
                        if self.jucator_curent == 1:
                            stare_noua.piese_jucator1.remove(pozitie)
                            stare_noua.piese_jucator1.add(vecin)
                        else:
                            stare_noua.piese_jucator2.remove(pozitie)
                            stare_noua.piese_jucator2.add(vecin)
                        if stare_noua.a_format_moara(
                                vecin,
                                stare_noua.piese_jucator1 if self.jucator_curent == 1
                                else stare_noua.piese_jucator2):
                            stari_dupa_lovitura = stare_noua._genereaza_stari_dupa_lovitura()
                            for s in stari_dupa_lovitura:
                                s._schimba_jucatorul()
                                stari_noi.add(s)
                        else:
                            stare_noua._schimba_jucatorul()
                            stari_noi.add(stare_noua)
        return stari_noi

    def _genereaza_stari_dupa_lovitura(self):
        stari_dupa_lovitura = set()
        if self.jucator_curent == 1:
            piese_adv = self.piese_jucator2
        else:
            piese_adv = self.piese_jucator1
        piese_adv_in_mori = self.piese_in_mori(piese_adv)
        piese_scoatere_posibile = piese_adv - piese_adv_in_mori
        if not piese_scoatere_posibile:
            piese_scoatere_posibile = piese_adv
        for piesa_de_scos in piese_scoatere_posibile:
            stare_lov = self._copie_stare()
            if self.jucator_curent == 1:
                stare_lov.piese_jucator2.remove(piesa_de_scos)
            else:
                stare_lov.piese_jucator1.remove(piesa_de_scos)
            stari_dupa_lovitura.add(stare_lov)
        return stari_dupa_lovitura

