import pygame
import sys
from stare_tintar import stare_tintar
from evaluare_stare_tintar import evaluare_stare_tintar
from min_max import min_max
from alpha_beta import alpha_beta
from bayesian_tintar import BayesianEvaluator, alege_mutare_bayesian

pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tintar")

NODE_COORDS = {
    1: (100, 100),
    2: (400, 100),
    3: (700, 100),
    4: (200, 200),
    5: (400, 200),
    6: (600, 200),
    7: (300, 300),
    8: (400, 300),
    9: (500, 300),
    10: (100, 400),
    11: (200, 400),
    12: (300, 400),
    13: (500, 400),
    14: (600, 400),
    15: (700, 400),
    16: (300, 500),
    17: (400, 500),
    18: (500, 500),
    19: (200, 600),
    20: (400, 600),
    21: (600, 600),
    22: (100, 700),
    23: (400, 700),
    24: (700, 700)
}

RADIUS = 15

def distance_sq(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def get_node_at_pos(pos):
    for node, coord in NODE_COORDS.items():
        if distance_sq(pos, coord) <= (RADIUS*2)**2:
            return node
    return None

def draw_board(stare):
    WIN.fill((255,255,255))
    for start in NODE_COORDS:
        for end in stare.pozitii_adjacente[start]:
            pygame.draw.line(WIN, (0,0,0), NODE_COORDS[start], NODE_COORDS[end], 2)
    for node, coord in NODE_COORDS.items():
        color = (0,0,0)
        if node in stare.piese_jucator1:
            color = (255,0,0)
        elif node in stare.piese_jucator2:
            color = (0,0,255)
        pygame.draw.circle(WIN, color, coord, RADIUS)
    pygame.display.update()

def valid_removal(stare, capturing_player):
    if capturing_player == 1:
        opponent = stare.piese_jucator2
    else:
        opponent = stare.piese_jucator1
    opponent_in_mills = stare.piese_in_mori(opponent)
    candidates = opponent - opponent_in_mills
    if candidates:
        return candidates
    return opponent

def game_loop():
    stare_curenta = stare_tintar()
    evaluator = evaluare_stare_tintar()
    bayes_eval = BayesianEvaluator()

    mode = "min_max"    
    user_turn = True
    selected_node = None
    capture_mode = False
    capturing_player = None
    clock = pygame.time.Clock()
    adancime = 4

    while True:
        clock.tick(30)
        draw_board(stare_curenta)

        if not stare_curenta.este_in_faza_de_plasare():
            if len(stare_curenta.piese_jucator1) < 3:
                print("Jucator 1 are mai putin de 3 piese. Jucator 2 castiga.")
                pygame.time.wait(2000)
                break
            if len(stare_curenta.piese_jucator2) < 3:
                print("Jucator 2 are mai putin de 3 piese. Jucator 1 castiga.")
                pygame.time.wait(2000)
                break

        if user_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if capture_mode:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        node = get_node_at_pos(pos)
                        if node and node in valid_removal(stare_curenta, capturing_player):
                            if capturing_player == 1:
                                stare_curenta.piese_jucator2.remove(node)
                            else:
                                stare_curenta.piese_jucator1.remove(node)
                            capture_mode = False
                            stare_curenta._schimba_jucatorul()
                            user_turn = False
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    node = get_node_at_pos(pos)
                    if not node:
                        continue
                    if stare_curenta.este_in_faza_de_plasare():
                        if node not in stare_curenta.pozitii_libere():
                            continue
                        if stare_curenta.jucator_curent == 1:
                            stare_curenta.piese_jucator1.add(node)
                            stare_curenta.piese_ramase_jucator1 -= 1
                        else:
                            stare_curenta.piese_jucator2.add(node)
                            stare_curenta.piese_ramase_jucator2 -= 1
                        if stare_curenta.a_format_moara(node, stare_curenta.piese_jucator1 if stare_curenta.jucator_curent == 1 else stare_curenta.piese_jucator2):
                            capture_mode = True
                            capturing_player = stare_curenta.jucator_curent
                            continue
                        stare_curenta._schimba_jucatorul()
                        user_turn = False
                    else:
                        if selected_node is None:
                            if stare_curenta.jucator_curent == 1 and node in stare_curenta.piese_jucator1:
                                selected_node = node
                        else:
                            if node not in stare_curenta.piese_jucator1 and node not in stare_curenta.piese_jucator2 and node in stare_curenta.pozitii_adjacente[selected_node]:
                                if stare_curenta.jucator_curent == 1:
                                    stare_curenta.piese_jucator1.remove(selected_node)
                                    stare_curenta.piese_jucator1.add(node)
                                else:
                                    stare_curenta.piese_jucator2.remove(selected_node)
                                    stare_curenta.piese_jucator2.add(node)
                                if stare_curenta.a_format_moara(node, stare_curenta.piese_jucator1 if stare_curenta.jucator_curent == 1 else stare_curenta.piese_jucator2):
                                    capture_mode = True
                                    capturing_player = stare_curenta.jucator_curent
                                    selected_node = None
                                    continue
                                stare_curenta._schimba_jucatorul()
                                user_turn = False
                            selected_node = None
        else:
            if mode == "bayes":
                new_stare = alege_mutare_bayesian(stare_curenta, bayes_eval)
            elif mode == "alpha_beta":
                valoare, new_stare = alpha_beta(stare_curenta, adancime, evaluator, stare_curenta.jucator_curent, -float("inf"), float("inf"))
            elif mode == "min_max":
                valoare, new_stare = min_max(stare_curenta, adancime, evaluator, stare_curenta.jucator_curent)
            else:
                new_stare = None
            if new_stare is None:
                print("Jucatorul", stare_curenta.jucator_curent, "nu mai poate muta.")
                pygame.time.wait(2000)
                break
            stare_curenta = new_stare
            user_turn = True

def main():
    game_loop()

if __name__ == "__main__":
    main()
