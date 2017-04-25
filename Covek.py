class Covek:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance

        self._broj_figura_postavjlanje = self.broj_figura

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
            
            if self._game_instance.postavi_igraca(self.oznaka, pozicija):
                self._broj_figura_postavjlanje -= 1
                return pozicija

            print("Ne mozete zauzeti polje ", pozicija)

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

    def pojedi_figuru(self):
        while True:
            try:
                pozicija = int(input("\n[{}] unesite polje da pojedete figuru: ".format(self.oznaka)))
            except ValueError:
                print("Uneli ste pogresnu vrednost!")
                continue

            if self._game_instance.ukloni_igraca(self.oznaka, pozicija):
                break

            print("Ne mozete ukloniti igraca na poziciji ", pozicija)