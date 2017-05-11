class Covek:
    """
    Klasa koja omogucuje interakciju aplikacije i korisnika
    """

    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self._game_instance = game_instance
        self.broj_figura = 9
        self._oznaka_protivnik = 'B' if oznaka == 'W' else 'W'
        self._broj_figura_postavjlanje = self.broj_figura

    # Postavlja figuru na tablu i vraca poziciju na kojoj je postavljen
    def postavi_figuru(self):
        while True:
            try:
                pozicija = int(input("\n[{}][{}] unesite poziciju: ".format(self.oznaka, self._broj_figura_postavjlanje)))
            except ValueError:
                print("Uneli ste pogresnu vrednost!")
                continue

            if pozicija == 50:  # Terminator programa
                import sys
                sys.exit()
            
            # TODO: IZMESTI OVO U GAME KLASU
            if self._game_instance.postavi_igraca(self.oznaka, pozicija):
                self._broj_figura_postavjlanje -= 1
                return pozicija

            print("Ne mozete zauzeti polje ", pozicija)

    # Pomera figuru sa stare na novu poziciju i vraca novu poziciju
    def pomeri_figuru(self):
        while True:
            try:
                stara_pozicija = int(input("\n[{}][{}] unesite poziciju figure koju zelite da pomerite: ".format(self.oznaka, self.broj_figura)))
                nova_pozicija = int(input("[{}] unesite novu poziciju: ".format(self.oznaka)))
            except ValueError:
                print("Uneli ste pogresnu vrednost!")
                continue
            
            if self._game_instance.pomeri_igraca(self.oznaka, stara_pozicija, nova_pozicija):
                return nova_pozicija

            print("Ne mozete pomeriti figuru na polje ", nova_pozicija)

    # Uklanja figuru sa table i vraca poziciju sa koje je figura uklonjena
    def pojedi_figuru(self):
        while True:
            if not self._game_instance.sve_u_mici(self._oznaka_protivnik):
                return -1

            try:
                pozicija = int(input("\n[{}] unesite polje da pojedete figuru: ".format(self.oznaka)))
            except ValueError:
                print("Uneli ste pogresnu vrednost!")
                continue

            if self._game_instance.ukloni_igraca(self.oznaka, pozicija):
                return pozicija

            print("Ne mozete ukloniti igraca na poziciji ", pozicija)