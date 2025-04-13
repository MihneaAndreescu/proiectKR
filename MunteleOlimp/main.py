from collections import defaultdict
import heapq
import random

muchii_mici = [ (7, 8), (8, 9),
                (9, 13), (13, 18),
                (18, 17), (17, 16),
                (16, 12), (12, 7),
                (5, 8),
                (13, 14),
                (17, 20), 
                (12, 11),
                (14, 15),
                (20, 23),
                (10, 11),
                (5, 2)]

muchii_medii = [(4, 5), (5, 6), (6, 14), (14, 21),
                (21, 20), (20, 19), (19, 11), (11, 4)]

muchii_mari = [(1, 2), (2, 3), (3, 15), (15, 24),
               (24, 23), (23, 22), (22, 10), (10, 1)]


assert len(muchii_mici) + len(muchii_medii) + len(muchii_mari) == 32

def solve(nod_start, noduri_scop, nr_pasi, algoritm, categ_muchii, categ_costuri_muchii):
    assert algoritm == "A*" or algoritm == "IDA*"
    assert len(categ_muchii) == 3
    assert len(categ_costuri_muchii) == 3

    graf = defaultdict(list)
    noduri = set()
    muchii = []

    for (mu, co) in zip(categ_muchii, categ_costuri_muchii):
        for (x, y) in mu:
            rand_add = random.uniform(0, co)
            new_cost = co + rand_add
            graf[x].append((y, new_cost))
            graf[y].append((x, new_cost))
            muchii.append((x, y, co))
            muchii.append((y, x, co))
            noduri.add(x)
            noduri.add(y)

    nr_noduri = len(noduri)
    assert nr_noduri == 24

    roy_floyd = defaultdict(lambda: float('inf'))
    for x in noduri:
        roy_floyd[(x, x)] = 0

    for (x, y, c) in muchii:
        roy_floyd[(x, y)] = min(roy_floyd[(x, y)], c)
         
    for k in noduri:
        for i in noduri:
            for j in noduri:
                roy_floyd[(i, j)] = min(roy_floyd[(i, j)], roy_floyd[(i, k)] + roy_floyd[(k, j)])
    
    def euristica(nod):
        assert (nod in noduri)
        best = float('inf')
        for scop in noduri_scop:
            best = min(best, roy_floyd[(nod, scop)])
        return best

    if False: 
        for x in noduri:
            for y in noduri:
                print(roy_floyd[(x, y)], end=' ')
            print()

    
    if algoritm == "A*":
        open_list = []
        valg = {nod_start: 0}
        toate = []
        heapq.heappush(open_list, (valg[nod_start] + euristica(nod_start), nod_start, 0))
        closed = set()

        while open_list:
            curf, curnod, curpasi = heapq.heappop(open_list)
            if curnod in noduri_scop:
                return curnod
            if curpasi == nr_pasi:
                toate.append((curnod, valg[curnod]))
                continue

            closed.add(curnod)

            for vecin, cost in graf[curnod]:
                if vecin in closed:
                    continue
                noug = valg[curnod] + cost
                if vecin not in valg or noug < valg[vecin]:
                    valg[vecin] = noug 
                    heapq.heappush(open_list, (valg[vecin] + euristica(vecin), vecin, curpasi + 1))
        return toate
    else:
        assert algoritm == "IDA*"
        last_open = defaultdict(lambda: float('inf'))

        def go(nod, g, adancime_acum, limita, drum):
            global last_open
            last_open[nod] = min(last_open[nod], g)
            f = g + euristica(nod)
            if f > limita:
                return ["MAI_INCEARCA", f]
            if nod in noduri_scop:
                return ["GASIT", nod]
            if adancime_acum == nr_pasi:
                return ["MAI_INCEARCA", float('inf')]
            mic = float('inf')
            for vecin, cost_muchie in graf[nod]:
                if vecin in drum:
                    continue 
                cost_nou = g + cost_muchie
                date = go(vecin, cost_nou, adancime_acum + 1, limita, drum + [vecin])
                assert len(date) == 2 
                if date[0] == "GASIT":
                    return date
                assert date[0] == "MAI_INCEARCA"
                if date[1] < mic:
                    mic = date[1]
            return ["MAI_INCEARCA", mic]

        def ida_star():
            global last_open
            limita = euristica(nod_start)
            while True:
                last_open = defaultdict(lambda: float('inf'))
                date = go(nod_start, 0, 0, limita, [nod_start])
                assert len(date) == 2
                if date[0] == "GASIT":
                    return date[1]
                assert date[0] == "MAI_INCEARCA"
                if date[1] == float('inf'):
                    return list(last_open.items())
                limita = date[1]

        return ida_star()
        

sol = solve(12, [1, 20], 2, "A*", [muchii_mici, muchii_medii, muchii_mari], [1, 2, 3])
print(sol)
