class Ai:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'

        self._postavljenje_figure = 9

    # Vraca 1 ako sam ja napravio micu, -1 ako je protivnik, 0 ako nije napravljena mica u poslednjem potezu
    def _napravljena_mica(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == self.oznaka:
                return 1
            elif tabla[i] == tabla[j] == tabla[k] == self._oznaka_protivnik:
                return -1
        
        return 0

    # Razlika izmedju broja mojih i protivnikovih napravljenih mica
    def _broj_mica(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_mica_ja = 0
        broj_mica_protivnik = 0

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == self.oznaka:
                broj_mica_ja += 1
            elif tabla[i] == tabla[j] == tabla[k] == self._oznaka_protivnik:
                broj_mica_protivnik += 1

        return broj_mica_ja - broj_mica_protivnik

    # Razlika izmedju protivnikovih i mojih blokiranih figurica
    def _broj_blokiranih_figura(self):
        tabla = self._game_instance._tabla
        
        pozicije_ja = []
        pozicije_protivnik = []

        for i in range(len(tabla)):
            if tabla[i] == self.oznaka:
                pozicije_ja.append(i)
            elif tabla[i] == self._oznaka_protivnik:
                pozicije_protivnik.append(i)

        broj_blokiranih_ja = self.__nadji_broj_blokiranih(pozicije_ja)
        broj_blokiranih_protivnih = self.__nadji_broj_blokiranih(pozicije_protivnik)
        return broj_blokiranih_ja - broj_blokiranih_protivnih

    # Pomocna metoda koja nalazi broj blokiranih figura na tabli
    def __nadji_broj_blokiranih(self, pozicije):
        putanje = self._game_instance._moguce_putanje
        broj_blokiranih = 0

        for i in pozicije:
            blokirana = True
            for j in putanje[i]:
                if j == 'X':
                    blokirana = False
                    break
            
            if blokirana:
                broj_blokiranih += 1

        return broj_blokiranih

    # Razlika izmedju broja mojih i protivnikovih figura
    def _broj_figura(self):
        # TODO: promeni da self.brojfigura, ali za to mora da se namesti da i u minimax vrati ono sta je oduzeo
        tabla = self._game_instance._tabla
        broj_figura_ja = 0
        broj_figura_protivnik = 0

        for i in tabla:
            if i == self.oznaka:
                broj_figura_ja += 1
            elif i == self._oznaka_protivnik:
                broj_figura_protivnik += 1

        #return broj_figura_ja - broj_figura_protivnik
        return broj_figura_protivnik - broj_figura_ja

    # Razlika izmedju broja mojih i protivnikovih '2 piece configurations'
    def _zauzete_dve_pozicije(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_zauzetih_ja = 0
        broj_zauzetih_protivnik = 0

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == self.oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == self.oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == self.oznaka and tabla[i] == 'X'):
                broj_zauzetih_ja += 1
            elif (tabla[i] == tabla[j] == self._oznaka_protivnik and tabla[k] == 'X') or (tabla[i] == tabla[k] == self._oznaka_protivnik and tabla[j] == 'X') or (tabla[j] == tabla[k] == self._oznaka_protivnik and tabla[i] == 'X'):
                broj_zauzetih_protivnik += 1

        return broj_zauzetih_ja - broj_zauzetih_protivnik

    # Razlika izmedju mojih i protivnihkov '3 piece conf.' (u jednom potezu se moze napraviti vise mica)
    def _moguca_dupla_mica(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        moguce_mice_ja = []
        moguce_mice_protivnik = []

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == self.oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == self.oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == self.oznaka and tabla[i] == 'X'):
                moguce_mice_ja.append((i, j, k))
            elif (tabla[i] == tabla[j] == self._oznaka_protivnik and tabla[k] == 'X') or (tabla[i] == tabla[k] == self._oznaka_protivnik and tabla[j] == 'X') or (tabla[j] == tabla[k] == self._oznaka_protivnik and tabla[i] == 'X'):
                moguce_mice_protivnik.append((i, j, k))

        broj_mice_ja = self.__nadji_duple_mice(moguce_mice_ja)
        broj_mice_protivnik = self.__nadji_duple_mice(moguce_mice_protivnik)
        return broj_mice_ja - broj_mice_protivnik

    # Razlika izmedju broja mojih i protivnikovih duplih mica (dupla mica-ako obe imaju jednu zajednicku figuru)
    def _dupla_mica(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        mice_ja = []
        mice_protivnik = []

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == self.oznaka:
                mice_ja.append((i, j, k))
            elif tabla[i] == tabla[j] == tabla[k] == self._oznaka_protivnik:
                mice_protivnik.append((i, j, k))

        broj_mice_ja = self.__nadji_duple_mice(mice_ja)
        broj_mice_protivnik = self.__nadji_duple_mice(mice_protivnik)                      
        return broj_mice_ja - broj_mice_protivnik

    # Pomocna funkcija za izracunavanje broja mica koje dele zajednicku figuru
    def __nadji_duple_mice(self, lista):
        broj_mica = 0

        if len(lista) > 1:
            for i in range(len(lista) - 1):
                for j in range(i + 1, len(lista)):
                    if lista[i][0] in lista[j] or lista[i][1] in lista[j] or lista[i][2] in lista[j]:
                        broj_mica += 1
        
        return broj_mica

    # Vraca 1 ako je pobeda, vraca -1 ako je izgubljeno, u suprotnom vraca 0
    def _kraj_igre(self):
        if self._game_instance.proveri_kraj_igre():
            if self._game_instance._pobednik == self.oznaka:
                return 1
            elif self._game_instance._pobednik == self._oznaka_protivnik:
                return -1

        return 0

    # Funkcija koja izracunava heuristiku. Bice linearna f-ja
    def _izracunaj_heuristiku(self):
        return self._napravljena_mica() + self._broj_mica() + self._broj_blokiranih_figura() + self._broj_figura() + self._zauzete_dve_pozicije() + self._moguca_dupla_mica() + self._dupla_mica() + self._kraj_igre()

    def __nadji_oznaku_protivnika(self, oznaka):
        if oznaka == self.oznaka:
            return self._oznaka_protivnik
        else:
            return self.oznaka

    # Glavni algoritam
    def _minimax(self, depth, alpha, beta, oznaka):
        slobodna_polja = self._game_instance.nadji_slobodna_polja()

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(oznaka, i)
            #depth = 2

            if depth == 0:
                #depth += 1
                heuristika = self._izracunaj_heuristiku()
                self._game_instance.oslobodi_polje(i)                  
                return heuristika
            else:
                #depth -= 1
                vrednost = self._minimax(depth - 1, alpha, beta, self.__nadji_oznaku_protivnika(oznaka))
                self._game_instance.oslobodi_polje(i)                  

                if oznaka == self.oznaka:
                    if vrednost > alpha:
                        alpha = vrednost
                    if alpha >= beta:
                        #self._game_instance.oslobodi_polje(i)
                        #depth -= 1
                        return beta
                else:
                    if vrednost < beta:
                        beta = vrednost
                    if beta <= alpha: 
                        #self._game_instance.oslobodi_polje(i)   
                        #depth -= 1
                        return alpha    

        if oznaka == self.oznaka:
            return alpha
        else:
            return beta

    def postavi_figuru(self):
        a = -10000
        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        potezi = []
        depth = 2

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(self.oznaka, i)

            #if self._postavljenje_figure < depth:
                #depth = self._postavljenje_figure       

            vrednost = self._minimax(depth, -10000, 10000, self._oznaka_protivnik)
            self._game_instance.oslobodi_polje(i)

            #potezi.append(vrednost)
            
            if vrednost > a:
                a = vrednost
                potezi = [i]
            elif vrednost == a:
                potezi.append(i)
            
        import random
        pozicija = random.choice(potezi)
        #pozicija = potezi.index(max(potezi))
        print("\n[AI] Zauzeo sam ", pozicija)
        self._postavljenje_figure -= 1
        return pozicija