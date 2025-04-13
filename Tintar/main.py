from stare_tintar import stare_tintar
from Tintar.evaluare_stare_tintar import evaluare_stare_tintar

def main():
    stare_init = stare_tintar()
    evaluator = evaluare_stare_tintar()
    print("Stare initiala:", stare_init)
    print("Scor:", evaluator.evalueaza(stare_init))
    stari_noi = stare_init.generare_stari_urmatoare()
    for idx, s in enumerate(list(stari_noi)[:5]):
        print(f"Stare {idx}:", s, "Scor:", evaluator.evalueaza(s))

if __name__ == "__main__":
    main()