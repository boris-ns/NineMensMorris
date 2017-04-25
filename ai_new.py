class Ai:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'

    def postavi_figuru(self):
        return self._minimax(3)

    
    # Vraca vrednost za minimax ukoliko je igrac napravio micu
    def _napravljena_mica(self):
        MINIMAX_VREDNOST = 3

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == tabla[j] == tabla[k] == oznaka:
                return MINIMAX_VREDNOST

        return None

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

        return None

    # Vraca vrednost za minimax ukoliko je protivnik zauzeo jednu poziciju u redu
    def _zauzeta_jedna_poz_protivnik(self, oznaka=self._oznaka_protivnik):
        MINIMAX_VREDNOST = -1

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == oznaka and tabla[j] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[j] == oznaka and tabla[i] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[k] == oznaka and tabla[j] == tabla[i] == 'X':
                return MINIMAX_VREDNOST

        return None

    # Vraca vrednost za minimax ukoliko sam zauzeo jednu poziciju u redu
    def _zauzeta_jedna_poz_igrac(self, oznaka=self.oznaka):
        MINIMAX_VREDNOST = 1

        mice = self._game_instance._moguce_mice
        tabla = self._game_instance._tabla

        for i, j, k in mice:
            if tabla[i] == oznaka and tabla[j] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[j] == oznaka and tabla[i] == tabla[k] == 'X':
                return MINIMAX_VREDNOST
            elif tabla[k] == oznaka and tabla[j] == tabla[i] == 'X':
                return MINIMAX_VREDNOST

        return None

    def _nadji_max(self):
        lista = []
        lista.append(self._zauzete_dve_pozicije(self.oznaka))
        lista.append(self._zauzeta_jedna_poz_protivnik())
        lista.append(self._zauzeta_jedna_poz_igrac())
        lista.append(self._napravljena_mica())

        return max(lista)
   

    def _maxi(self, depth):
        if depth == 0:
            return

        slobodna_polja = self._game_instance.nadji_slobodna_polja()
        max_vrednost = None
        najbolja_pozicija = None

        for i in range slobodna_polja:
            self._game_instance.postavi_igraca(self.oznaka, i)

            # TODO vidi kako si u tic tac toe realizovao

            self._game_instance.oslobodi_polje(i)

        depth -= 1

    def _mini(self, depth):
        if depth == 0:
            return

        slobodna_polja = self._game_instance.nadji_slobodna_polja()

        for i in range slobodna_polja:
            self._game_instance.postavi_igraca(self._oznaka_protivnik, i)

            # TODO

            self._game_instance.oslobodi_polje(i)

        depth -= 1
