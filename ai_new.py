from heuristika import Heuristika 

class Ai:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'
        self._he = Heuristika(game_instance)
        self._postavljenje_figure = 9
        self.DEPTH = 3
    

    # Funkcija koja izracunava heuristiku. Bice linearna f-ja
    def _izracunaj_heuristiku(self):
        return self._broj_mica() + self._broj_blokiranih_figura() + self._broj_figura() + self._zauzete_dve_pozicije() + self._moguca_dupla_mica() + self._dupla_mica() + self._kraj_igre()

    def _heuristika_postavljanje(self, potez):
        rezultat  = 18 * self._napravljena_mica(potez)
        rezultat += 26 * self._broj_mica()
        rezultat += self._broj_blokiranih_figura()
        rezultat += 6 * self._broj_figura()
        rezultat += 12 * self._mesto_za_micu()
        rezultat += 7 * self._zauzete_dve_pozicije()

        return rezultat  

    def __nadji_oznaku_protivnika(self, oznaka):
        if oznaka == self.oznaka:
            return self._oznaka_protivnik
        else:
            return self.oznaka

    # FAZA 1: Minimax za postavljanje figura
    def _minimax_postavi(self, depth, alpha, beta, oznaka):
        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        poz_pojedi = None

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(oznaka, i)

            if depth == 0:
                heuristika = self._he.heuristika_postavljanje(i, self.oznaka, self._oznaka_protivnik)         
                self._game_instance.oslobodi_polje(i)                  
                return heuristika
            else: 
                vrednost = self._minimax_postavi(depth - 1, alpha, beta, self.__nadji_oznaku_protivnika(oznaka))
                self._game_instance.oslobodi_polje(i)

                if oznaka == self.oznaka:
                    if vrednost > alpha:
                        alpha = vrednost
                    if alpha >= beta:
                        return beta
                else:
                    if vrednost < beta:
                        beta = vrednost
                    if beta <= alpha: 
                        return alpha    

        if oznaka == self.oznaka:
            return alpha
        else:
            return beta

    def postavi_figuru(self):
        a = -10000
        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        potezi = []

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(self.oznaka, i)   

            vrednost = self._minimax_postavi(self.DEPTH, -10000, 10000, self._oznaka_protivnik)
            self._game_instance.oslobodi_polje(i)
            
            if vrednost > a:
                a = vrednost
                potezi = [i]
            elif vrednost == a:
                potezi.append(i)
            
        import random
        pozicija = random.choice(potezi)

        print("\n[AI] Zauzeo sam ", pozicija)
        self._postavljenje_figure -= 1
        return pozicija

    def _proveri_blokiran(self, pozicija):
        putanje = self._game_instance._moguce_putanje

        for i in putanje[pozicija]:
            if self._game_instance._tabla[i] == 'X':
                return False

        return True
    
    def _nadji_moguca_polja(self, stara_pozicija):
        putanje = self._game_instance._moguce_putanje
        moguce_putanje = []

        for i in putanje[stara_pozicija]:
            if self._game_instance._tabla[i] == 'X':
                moguce_putanje.append(i)

        return moguce_putanje

    # FAZA 2: Minimax za pomeranje figura
    def _minimax_pomeri(self, depth, alpha, beta, oznaka):
        zauzeta_polja = self._game_instance.nadji_zauzeta_polja(oznaka)

        for i in zauzeta_polja:
            if self._proveri_blokiran(i): # Ako je igrac blokiran nastavi na obradu sledeceg
                continue
            
            moguca_polja = self._nadji_moguca_polja(i)

            for j in moguca_polja:
                self._game_instance.oslobodi_polje(i)
                self._game_instance.postavi_igraca(oznaka, j)

                if depth == 0:
                    heuristika = self._he.heuristika_pomeranje(j, self.oznaka, self._oznaka_protivnik)
                    self._game_instance.oslobodi_polje(j)
                    self._game_instance.postavi_igraca(oznaka, i)
                    return heuristika
                else:
                    vrednost = self._minimax_pomeri(depth - 1, alpha, beta, self.__nadji_oznaku_protivnika(oznaka))
                    self._game_instance.oslobodi_polje(j)
                    self._game_instance.postavi_igraca(oznaka, i)                  

                    if oznaka == self.oznaka:
                        if vrednost > alpha:
                            alpha = vrednost
                        if alpha >= beta:
                            return beta
                    else:
                        if vrednost < beta:
                            beta = vrednost
                        if beta <= alpha:
                            return alpha

        if oznaka == self.oznaka:
            return alpha
        else:
            return beta

    def pomeri_figuru(self):
        a = -10000
        zauzeta_polja = self._game_instance.nadji_zauzeta_polja(self.oznaka)
        potez = None
        stara_pozicija = None

        for i in zauzeta_polja:
            if self._proveri_blokiran(i):
                continue

            moguca_polja = self._nadji_moguca_polja(i)

            for j in moguca_polja:
                self._game_instance.oslobodi_polje(i)
                self._game_instance.postavi_igraca(self.oznaka, j)  

                vrednost = self._minimax_pomeri(self.DEPTH, -10000, 10000, self._oznaka_protivnik)

                self._game_instance.oslobodi_polje(j)
                self._game_instance.postavi_igraca(self.oznaka, i)

                if vrednost > a:
                    a = vrednost
                    potez = j
                    stara_pozicija = i
                #elif vrednost == a:
                    #potezi.append(i)
                    #stara_pozicija = i
                
        print("\n[AI] Pomerio sam figuru sa " + str(stara_pozicija) + " na " + str(potez))
        self._game_instance.pomeri_igraca(self.oznaka, stara_pozicija, potez)
        return potez

    # Metoda za proveru da li je napravljena mica za prosledjenog igraca
    def proveri_micu(self, oznaka_igraca, poslednja_pozicija):
        for i, j, k in self._game_instance._moguce_mice:
            if i == poslednja_pozicija or j == poslednja_pozicija or k == poslednja_pozicija:
                if self._game_instance._tabla[i] == self._game_instance._tabla[j] == self._game_instance._tabla[k] and self._game_instance._tabla[i] == oznaka_igraca:
                    return True

        return False

    # Nalazi poziciju 2 figure u redu, i vraca poz. jednu od njih da bi ih pojeo, sprecavanje moguce mice
    def _moguca_mica_pojedi(self):
        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla
        import random
        for i, j, k in mice:
            if tabla[i] == tabla[j] == self._oznaka_protivnik and tabla[k] == 'X' and not self.proveri_micu(self._oznaka_protivnik, i) and not self.proveri_micu(self._oznaka_protivnik, j):   
                return random.choice([i, j])
            elif tabla[i] == tabla[k] == self._oznaka_protivnik and tabla[j] == 'X' and not self.proveri_micu(self._oznaka_protivnik, i) and not self.proveri_micu(self._oznaka_protivnik, k):
                return random.choice([i,k])
            elif tabla[j] == tabla[k] == self._oznaka_protivnik and tabla[i] == 'X' and not self.proveri_micu(self._oznaka_protivnik, j) and not self.proveri_micu(self._oznaka_protivnik, k):
                return random.choice([j,k])

        return None

    def _nadji_random_poziciju_pojedi(self):
        from random import randint
        tabla = self._game_instance._tabla
        protivnik_pozicije = []
        
        for i in range(0, len(tabla)):
            if tabla[i] == self._oznaka_protivnik and not self.proveri_micu(self._oznaka_protivnik, i):
                protivnik_pozicije.append(i)

        return protivnik_pozicije[randint(0, len(protivnik_pozicije) - 1)]

    def _nadji_pozicije_protivnika(self, oznaka_protivnik):
        tabla = self._game_instance._tabla
        protivnik_pozicije = []

        for i in range(0, len(tabla)):
            if tabla[i] == oznaka_protivnik and not self.proveri_micu(oznaka_protivnik, i):
                protivnik_pozicije.append(i)

        return protivnik_pozicije

    def _pojedi_figuru(self, oznaka_protivnik):
        protivnik_pozicije = self._nadji_pozicije_protivnika(oznaka_protivnik)
        max_ocena = None
        pozicija = None

        for i in protivnik_pozicije:
            self._game_instance.oslobodi_polje(i)
            
            ocena = self._he.heuristika_pojedi(self.oznaka, self._oznaka_protivnik)
            if max_ocena == None or ocena > max_ocena:
                max_ocena = ocena
                pozicija = i
            
            self._game_instance.postavi_igraca(self._oznaka_protivnik, i)
            
        return pozicija

    def pojedi_figuru(self):
        pozicija = self._pojedi_figuru(self._oznaka_protivnik)
        print("\n[AI] Pojeo sam figuru sa pozicije " + str(pozicija))

        if pozicija == None:
            return -1

        return pozicija
    '''
    def pojedi_figuru(self):
        moguca_mica = self._moguca_mica_pojedi()
        random_pozicija = self._nadji_random_poziciju_pojedi()

        if moguca_mica != None:
            print("\n[AI] Pojeo sam figuru sa pozicije " + str(moguca_mica))
            return moguca_mica
        else:
            print("\n[AI] Pojeo sam figuru sa pozicije " + str(random_pozicija))
            return random_pozicija
    '''