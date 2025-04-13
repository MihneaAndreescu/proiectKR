import random
import time
from concurrent.futures import ProcessPoolExecutor
from stare_tintar import stare_tintar
from evaluare_stare_tintar import evaluare_stare_tintar
from min_max import min_max, terminal
from alpha_beta import alpha_beta

def simuleaza_partida(algoritm, adancime, evaluator1, evaluator2, draw_if_longer_than):
    stare_curenta = stare_tintar()
    if random.choice([True, False]):
        mapping_evaluator = {1: evaluator1, 2: evaluator2}
    else:
        mapping_evaluator = {1: evaluator2, 2: evaluator1}
    stare_curenta.jucator_curent = random.choice([1, 2])
    numar_mutari = 0
    while True:
        if numar_mutari >= draw_if_longer_than:
            return (0, 1, 0)
        if terminal(stare_curenta):
            break
        evaluator_curent = mapping_evaluator[stare_curenta.jucator_curent]
        if algoritm == "alpha_beta":
            valoare, stare_noua = alpha_beta(
                stare_curenta, adancime, evaluator_curent,
                stare_curenta.jucator_curent, -float("inf"), float("inf")
            )
        else:
            valoare, stare_noua = min_max(
                stare_curenta, adancime, evaluator_curent,
                stare_curenta.jucator_curent
            )
        if stare_noua is None:
            break
        stare_curenta = stare_noua
        numar_mutari += 1
    if len(stare_curenta.piese_jucator1) < 3:
        castigator = mapping_evaluator[2]
    elif len(stare_curenta.piese_jucator2) < 3:
        castigator = mapping_evaluator[1]
    else:
        return (0, 1, 0)
    if castigator is evaluator1:
        return (1, 0, 0)
    else:
        return (0, 0, 1)

def evaluare_stare_tintar_with_params(params):
    evaluator = evaluare_stare_tintar()
    evaluator._coef_piese = params.get("coef_piese", evaluator._coef_piese)
    evaluator._coef_mobility = params.get("coef_mobility", evaluator._coef_mobility)
    evaluator._coef_mori = params.get("coef_mori", evaluator._coef_mori)
    evaluator._coef_mills_potential = params.get("coef_mills_potential", evaluator._coef_mills_potential)
    return evaluator

def compara_evaluatori(param_set1, param_set2, num_partide=100, adancime=3, draw_if_longer_than=50, algoritm="alpha_beta"):
    evaluator1 = evaluare_stare_tintar_with_params(param_set1)
    evaluator2 = evaluare_stare_tintar_with_params(param_set2)
    total1, total_draw, total2 = 0, 0, 0
    for _ in range(num_partide):
        rezultat = simuleaza_partida(algoritm, adancime, evaluator1, evaluator2, draw_if_longer_than)
        total1 += rezultat[0]
        total_draw += rezultat[1]
        total2 += rezultat[2]
    return total1, total_draw, total2

def meci(param1, param2, num_partide=60, adancime=3, draw_if_longer_than=50, algoritm="alpha_beta"):
    res = compara_evaluatori(param1, param2, num_partide, adancime, draw_if_longer_than, algoritm)
    if res[0] > res[2]:
        return param1
    elif res[0] < res[2]:
        return param2
    else:
        return random.choice([param1, param2])

def turneu(lista_param, num_threads=1):
    current = lista_param
    while len(current) > 1:
        next_round = []
        with ProcessPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(meci, current[i], current[i+1])
                       for i in range(0, len(current), 2)]
            for future in futures:
                next_round.append(future.result())
        current = next_round
    return current[0]

if __name__ == "__main__":
    k = 6
    n = 2 ** k
    lista_param = []
    for i in range(n):
        params = {
            "coef_piese": random.uniform(0, 1),
            "coef_mobility": random.uniform(0, 1),
            "coef_mori": random.uniform(0, 1),
            "coef_mills_potential": random.uniform(0, 1)
        }
        lista_param.append(params)
    start = time.time()
    campion = turneu(lista_param, num_threads=8)
    end = time.time()
    print("Campionul:", campion)
    print("Timpul de evaluare:", end - start, "secunde")
