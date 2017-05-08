class Heuristika:
    def __init__(self, game_instance):
        self._game_instance = game_instance
    
    # Vraca 1 ako sam ja napravio micu, -1 ako je protivnik, 0 ako nije napravljena mica u poslednjem potezu
    def _napravljena_mica(self, oznaka, poslednji_potez):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if i == poslednji_potez or j == poslednji_potez or k == poslednji_potez:
                if tabla[i] == tabla[j] == tabla[k] == oznaka:
                    return 10
        
        return 0

    # Razlika izmedju broja mojih i protivnikovih napravljenih mica
    def _broj_mica(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_mica = 0

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == oznaka:
                broj_mica += 1
                
        return broj_mica

    # Razlika izmedju protivnikovih i mojih blokiranih figurica
    def _broj_blokiranih_figura(self, oznaka):
        tabla = self._game_instance._tabla
        pozicije = []

        for i in range(len(tabla)):
            if tabla[i] == oznaka:
                pozicije.append(i)

        broj_blokiranih = self._nadji_broj_blokiranih(pozicije)
        return broj_blokiranih

    # Pomocna metoda koja nalazi broj blokiranih figura na tabli
    def _nadji_broj_blokiranih(self, pozicije):
        putanje = self._game_instance._moguce_putanje
        broj_blokiranih = 0

        for i in pozicije:
            blokirana = True
            for j in putanje[i]:
                if self._game_instance._tabla[j] == 'X':
                    blokirana = False
                    break
            
            if blokirana:
                broj_blokiranih += 1

        return broj_blokiranih

    # Razlika izmedju broja mojih i protivnikovih figura
    def _broj_figura(self, oznaka):
        tabla = self._game_instance._tabla
        broj_figura = 0

        for i in tabla:
            if i == oznaka:
                broj_figura += 1

        return broj_figura

    '''
    def _2_piece_conf(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_zauzetih = 0

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == self.oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == self.oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == self.oznaka and tabla[i] == 'X'):
                return 1

        return 0
    '''

    def _blokirao_mogucu_micu(self, oznaka1, oznaka2):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_blokiranih = 0

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == oznaka2 and tabla[k] == oznaka1) or (tabla[i] == tabla[k] == oznaka2 and tabla[j] == oznaka1) or (tabla[j] == tabla[k] == oznaka2 and tabla[i] == oznaka1):
                broj_blokiranih += 1

        return broj_blokiranih

    # 3 piece conf.
    # Razlika izmedju broja mojih i protivnikovih '2 piece configurations'
    def _zauzete_dve_pozicije(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_zauzetih = 0

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == oznaka and tabla[i] == 'X'):
                broj_zauzetih += 1

        return broj_zauzetih

    # Razlika izmedju mojih i protivnihkov '3 piece conf.' (u jednom potezu se moze napraviti vise mica)
    def _moguca_dupla_mica(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        moguce_mice = []

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == oznaka and tabla[i] == 'X'):
                moguce_mice.append((i, j, k))

        broj_mice = self._nadji_duple_mice(moguce_mice)
        return broj_mice

    # Razlika izmedju broja mojih i protivnikovih duplih mica (dupla mica-ako obe imaju jednu zajednicku figuru)
    def _dupla_mica(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        duple_mice = []

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == oznaka:
                duple_mice.append((i, j, k))

        duple_mice = self._nadji_duple_mice(duple_mice)                   
        return duple_mice

    # Pomocna funkcija za izracunavanje broja mica koje dele zajednicku figuru
    def _nadji_duple_mice(self, lista):
        broj_mica = 0

        if len(lista) > 1:
            for i in range(len(lista) - 1):
                for j in range(i + 1, len(lista)):
                    if lista[i][0] in lista[j] or lista[i][1] in lista[j] or lista[i][2] in lista[j]:
                        broj_mica += 1
        
        return broj_mica

    def _kraj_igre(self, oznaka1, oznaka2):
        if self._game_instance.proveri_kraj_igre():
            if self._game_instance._pobednik == oznaka1:
                return 50
            elif self._game_instance._pobednik == oznaka2:
                return -50

        return 0
    

    def heuristika_postavljanje(self, poslednji_potez, oznaka1, oznaka2):
        h = 0
        h -= self._broj_blokiranih_figura(oznaka1)
        h += 12 * (self._broj_mica(oznaka1) - self._broj_mica(oznaka2))
        h += 11 * self._blokirao_mogucu_micu(oznaka1, oznaka2) # - self._blokirao_mogucu_micu(oznaka2, oznaka1))
        h += 9 * self._moguca_dupla_mica(oznaka1)
        #h += 12 * self._napravljena_mica(oznaka1, poslednji_potez)
        #h += self._moguca_dupla_mica(oznaka1) - self._moguca_dupla_mica(oznaka2)
        #h += self._zauzete_dve_pozicije(oznaka1) - self._zauzete_dve_pozicije(oznaka1)

        return h

    def heuristika_pomeranje(self, poslednji_potez, oznaka1, oznaka2):
        h = 0

        h += self._broj_blokiranih_figura(oznaka2) - self._broj_blokiranih_figura(oznaka1)
        h += 12 * (self._broj_mica(oznaka1) - self._broj_mica(oznaka2))
        h += 11 * self._moguca_dupla_mica(oznaka1)
        h += 10 * self._blokirao_mogucu_micu(oznaka1, oznaka2)
        h += 2 * self._kraj_igre(oznaka1, oznaka2)

        return h