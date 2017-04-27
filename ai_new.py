class Ai:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'

    def postavi_figuru(self):
        pozicija, vrednost = self._maxi(5, -4, 4)
        return pozicija

    
    # Vraca vrednost za minimax ukoliko je igrac napravio micu
    def _napravljena_mica(self):
        MINIMAX_VREDNOST = 3

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == self.oznaka:
                return MINIMAX_VREDNOST

        return 0

    # Vraca vrednost za minimax ukoliko igrac moze da napravi micu ili da je blokira
    def _zauzete_dve_pozicije(self, oznaka):
        MINIMAX_VREDNOST = 2

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == tabla[j] == oznaka and tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[i] == tabla[k] == oznaka and tabla[j] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[j] == tabla[k] == oznaka and tabla[i] == 'X':
                return MINIMAX_VREDNOST

        return 0

    # Vraca vrednost za minimax ukoliko je protivnik zauzeo jednu poziciju u redu
    def _zauzeta_jedna_poz_protivnik(self):
        MINIMAX_VREDNOST = -1

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == self._oznaka_protivnik and tabla[j] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[j] == self._oznaka_protivnik and tabla[i] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[k] == self._oznaka_protivnik and tabla[j] == tabla[i] == 'X':
                return MINIMAX_VREDNOST

        return 0

    # Vraca vrednost za minimax ukoliko sam zauzeo jednu poziciju u redu
    def _zauzeta_jedna_poz_igrac(self):
        MINIMAX_VREDNOST = 1

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == self.oznaka and tabla[j] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[j] == self.oznaka and tabla[i] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[k] == self.oznaka and tabla[j] == tabla[i] == 'X':
                return MINIMAX_VREDNOST

        return 0

    def _nadji_max(self):
        lista = []
        lista.append(self._zauzete_dve_pozicije(self.oznaka))
        lista.append(self._zauzeta_jedna_poz_protivnik())
        lista.append(self._zauzeta_jedna_poz_igrac())
        lista.append(self._napravljena_mica())

        print(lista)
        return max(lista)

    def _nadji_min(self):
        lista = []
        lista.append(self._zauzete_dve_pozicije(self.oznaka))
        lista.append(self._zauzeta_jedna_poz_protivnik())
        lista.append(self._zauzeta_jedna_poz_igrac())
        lista.append(self._napravljena_mica())

        print(lista)
        return min(lista)
   

    def _maxi(self, depth, alpha, beta):
        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        najbolja_pozicija = None

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(self.oznaka, i)

            vrednost = self._nadji_max()

            if depth == 0:
                self._game_instance.oslobodi_polje(i)
                break
            else:
                depth -= 1
                protivnik_poz, vrednost = self._mini(depth, alpha, beta)

            self._game_instance.oslobodi_polje(i)

            if vrednost > alpha:
                alpha = vrednost
                najbolja_pozicija = i
            if alpha >= beta:
                return najbolja_pozicija, beta

        return najbolja_pozicija, alpha

    def _mini(self, depth, alpha, beta):
        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        najbolja_pozicija = None

        for i in slobodna_polja:
            self._game_instance.postavi_igraca(self._oznaka_protivnik, i)

            vrednost = self._nadji_min()

            if depth == 0:
                self._game_instance.oslobodi_polje(i)
                break
            else:
                protivnik_poz, vrednost = self._maxi(depth - 1, alpha, beta)

            self._game_instance.oslobodi_polje(i)

            if vrednost < beta:
                beta = vrednost
                najbolja_pozicija = i
            if beta <= alpha:
                return najbolja_pozicija, alpha

        return najbolja_pozicija, beta