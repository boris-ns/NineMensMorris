class Ai:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'

    # Ukoliko postorji mogucnost da neki od igraca napravi micu
    def _moguca_mica(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == tabla[j] == oznaka and tabla[k] == 'X':
                return k
            elif tabla[i] == tabla[k] == oznaka and tabla[j] == 'X':
                return j
            elif tabla[j] == tabla[k] == oznaka and tabla[i] == 'X':
                return i

        return None

    # Ako je igrac zauzeo jednu lokaciju u mogucoj mici
    def _nadji_poziciju_blizu(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        import random
        for i, j, k in mice:
            if tabla[i] == oznaka and tabla[j] == tabla[k] == 'X':
                return random.choice([j,k])
            elif tabla[j] == oznaka and tabla[i] == tabla[k] == 'X':
                return random.choice([i,k])
            elif tabla[k] == oznaka and tabla[j] == tabla[i] == 'X':
                return random.choice([i,j])

        return None

    # Metoda za trazenje random pozicije, kada ni 1 od uslova iz metoda dole nije ispunjen
    def _nadji_random_poziciju(self):
        from random import randint
        slobodne_pozicije = self._game_instance.nadji_slobodna_polja()
        return slobodne_pozicije[randint(0, len(slobodne_pozicije) - 1)]

    # Ukoliko protivnik ima mogucnost da napravi micu, metoda _moguca_mica() iznad vraca poziciju sa kojom bi to blokirala
    def _moguca_protivnikova_mica(self):
        return self._moguca_mica(self._oznaka_protivnik)

    # Ukoliko ja imam mogucnost da napravim micu, metoda _moguca_mica() iznad vraca poziciju sa kojom bi to blokirala
    def _moguca_moja_mica(self):
        return self._moguca_mica(self.oznaka)

    # Vraca poziciju blizu protivnika da bi sprecio mogucu micu
    def _pozicija_blizu_protivnika(self):
        return self._nadji_poziciju_blizu(self._oznaka_protivnik)

    # Vraca poziciju blizu moje figure, tako da u sledecem potezu imam mogucnost da napravim micu
    def _pozicija_blizu_mene(self):
        return self._nadji_poziciju_blizu(self.oznaka)

    def _pojedi_figuru_moguca_mica(self):
        return self._moguca_mica_pojedi(self._oznaka_protivnik)

    # Nalazi poziciju 2 figure u redu, i vraca poz. jednu od njih da bi ih pojeo, sprecavanje moguce mice
    def _moguca_mica_pojedi(self, oznaka):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        import random
        for i, j, k in mice:
            if tabla[i] == tabla[j] == oznaka and tabla[k] == 'X':   
                return random.choice([i, j])
            elif tabla[i] == tabla[k] == oznaka and tabla[j] == 'X':
                return random.choice([i,k])
            elif tabla[j] == tabla[k] == oznaka and tabla[i] == 'X':
                return random.choice([j,k])

        return None

    def _nadji_random_poziciju_pojedi(self):
        from random import randint
        tabla = self._game_instance._tabla
        protivnik_pozicije = []
        
        for i in range(0, len(tabla)):
            if tabla[i] == self._oznaka_protivnik:
                protivnik_pozicije.append(i)

        return protivnik_pozicije[randint(0, len(protivnik_pozicije) - 1)]

    # Prema odredjenim prioritetima se gleda na koju poziciju ce AI staviti figuru
    def postavi_figuru(self, poslednja_pozicija):
        protivnik_mica = self._moguca_protivnikova_mica()
        moja_mica = self._moguca_moja_mica()
        protivnik_blizu = self._pozicija_blizu_protivnika()
        blizu_mene = self._pozicija_blizu_mene()
        random_pozicija = self._nadji_random_poziciju()

        if moja_mica != None:
            self._game_instance.postavi_igraca(self.oznaka, moja_mica)
            print("\n[{}][AI] Stavio sam figuru na polje {}".format(self.oznaka, moja_mica))
            return moja_mica
        elif protivnik_mica != None:
            self._game_instance.postavi_igraca(self.oznaka, protivnik_mica)
            print("\n[{}][AI] Stavio sam figuru na polje {}".format(self.oznaka, protivnik_mica))
            return protivnik_mica
        elif blizu_mene != None:
            self._game_instance.postavi_igraca(self.oznaka, blizu_mene)
            print("\n[{}][AI] Stavio sam figuru na polje {}".format(self.oznaka, blizu_mene))
            return blizu_mene
        elif protivnik_blizu != None:
            self._game_instance.postavi_igraca(self.oznaka, protivnik_blizu)
            print("\n[{}][AI] Stavio sam figuru na polje {}".format(self.oznaka, protivnik_blizu))
            return protivnik_blizu
        else:
            self._game_instance.postavi_igraca(self.oznaka, random_pozicija)
            print("\n[{}][AI] Stavio sam figuru na polje {}".format(self.oznaka, random_pozicija))
            return random_pozicija
            
    def pojedi_figuru(self):
        moguca_mica = self._pojedi_figuru_moguca_mica()
        random_pozicija = self._nadji_random_poziciju_pojedi()

        if moguca_mica != None:
            self._game_instance.ukloni_igraca(self.oznaka, moguca_mica)
            print("\n[{}][AI] Pojeo sam figuru sa polja {}".format(self.oznaka, moguca_mica))
        else:
            self._game_instance.ukloni_igraca(self.oznaka, random_pozicija)
            print("\n[{}][AI] Pojeo sam figuru sa polja {}".format(self.oznaka, random_pozicija))