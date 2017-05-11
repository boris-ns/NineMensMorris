class Heuristika:
    def __init__(self, game_instance):
        self._game_instance = game_instance
    
    # Vraca 1 ako sam ja napravio micu, -1 ako je protivnik, 0 ako nije napravljena mica u poslednjem potezu
    def _napravljena_mica(self, poslednji_potez):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if i == poslednji_potez or j == poslednji_potez or k == poslednji_potez:
                if tabla[i] == tabla[j] == tabla[k] == self.oznaka:
                    return 10
                elif tabla[i] == tabla[j] == tabla[k] == self._oznaka_protivnik:
                    return -10
        
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
                if self._game_instance._tabla[j] == 'X':
                    blokirana = False
                    break
            
            if blokirana:
                broj_blokiranih += 1

        return broj_blokiranih

    # Razlika izmedju broja mojih i protivnikovih figura
    def _broj_figura(self):
        tabla = self._game_instance._tabla
        broj_figura_ja = 0
        broj_figura_protivnik = 0

        for i in tabla:
            if i == self.oznaka:
                broj_figura_ja += 1
            elif i == self._oznaka_protivnik:
                broj_figura_protivnik += 1

        return broj_figura_ja - broj_figura_protivnik
        #return broj_figura_protivnik - broj_figura_ja

    def _mesto_za_micu(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        broj_zauzetih_ja = 0
        broj_zauzetih_protivnik = 0

        for i, j, k in mice:
            if (tabla[i] == tabla[j] == self.oznaka and tabla[k] == 'X') or (tabla[i] == tabla[k] == self.oznaka and tabla[j] == 'X') or (tabla[j] == tabla[k] == self.oznaka and tabla[i] == 'X'):
                return 5
            elif (tabla[i] == tabla[j] == self._oznaka_protivnik and tabla[k] == 'X') or (tabla[i] == tabla[k] == self._oznaka_protivnik and tabla[j] == 'X') or (tabla[j] == tabla[k] == self._oznaka_protivnik and tabla[i] == 'X'):
                return -5

        return 0

    # 3 piece conf.
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
                return 50
            elif self._game_instance._pobednik == self._oznaka_protivnik:
                return -50

        return 0