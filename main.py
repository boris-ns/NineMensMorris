from Igra import Igra
from Covek import Covek
from Ai import Ai

if __name__ == "__main__":
    print("\n\n\t---===   MICE   ===---\n\n")

    igra = Igra()
    igrac1 = Covek('W', igra)
    igrac2 = Ai('B', igra)
    igra.set_igraci(igrac1, igrac2)
    igra.postavi_figure()

    '''
    igra._tabla[4] = 'B'
    igra._tabla[6] = 'B'
    igra._tabla[9] = 'B'
    igra._tabla[10] = 'B'
    igra._tabla[12] = 'B'
    igra._tabla[14] = 'B'
    igra._tabla[16] = 'B'
    igra._tabla[22] = 'B'
    
    igra._tabla[3] = 'W'
    igra._tabla[17] = 'W'
    igra._tabla[18] = 'W'
    igra._tabla[20] = 'W'
    igra._tabla[21] = 'W'
    igra._tabla[23] = 'W'
    
    igra.nacrtaj_tablu()
    igra.pomeraj_figure(igrac1, igrac2)
    '''