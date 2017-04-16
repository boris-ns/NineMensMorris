class Igra:
    def __init__(self):
        self._slobodno_polje = 'X'
        self._tabla = [self._slobodno_polje for i in range(24)]
        self._igrac1 = None
        self._igrac2 = None
        self._pobednik = None

    # Metoda trazi preostala slobodna mesta na tabli i vraca listu indeksima polja
    def nadji_slobodna_polja(self):
        slobodna_polja = []
        for i in self._tabla:
            if i == self._slobodno_polje:
                slobodna_polja.append(i)

        return slobodna_polja

    # Provera da li pozicija postoji i da li je slobodna
    def _proveri_poziciju(self, pozicija):
        if (not 0 <= pozicija < 24) or (self._tabla[pozicija] != self._slobodno_polje):
        #if not pozicija in self.nadji_slobodna_polja():
            return False
        
        return True

    # Zauzimanje polja na tabli
    def postavi_igraca(self, oznaka_igraca, pozicija):
        if not self._proveri_poziciju(pozicija):
            return False

        self._tabla[pozicija] = oznaka_igraca
        return True

    # Iscrtavanje table na ekran
    def nacrtaj_tablu(self):
        # TODO: Probaj da ubacis i koordinate u ispis matrice, da korisnik ne mora napamet da trazi poziciju

        tabla = [
            [self._tabla[0], '-','-','-','-','-', self._tabla[1], '-','-','-','-','-', self._tabla[2]],
            ['|', ' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ','|'],
            ['|', ' ', self._tabla[3], '-','-','-',self._tabla[4],'-''-''-',self._tabla[5],' ','|'],
            ['|', ' ','|',' ',' ',' ','|',' ',' ',' ','|',' ','|'],
            ['|',' ','|',' ', self._tabla[6],'-',self._tabla[7],'-', self._tabla[8],' ','|',' ','|'],
            ['|',' ','|',' ','|',' ',' ',' ','|',' ','|',' ','|'],
            [self._tabla[9],'-',self._tabla[10],'-', self._tabla[11],' ',' ',' ',self._tabla[12],'-',self._tabla[13],'-', self._tabla[14]],
            ['|',' ','|',' ','|',' ',' ',' ','|',' ','|',' ','|'],
            ['|',' ','|',' ', self._tabla[15],'-',self._tabla[16],'-', self._tabla[17],' ','|',' ','|'],
            ['|', ' ','|',' ',' ',' ','|',' ',' ',' ','|',' ','|'],
            ['|', ' ', self._tabla[18], '-','-','-',self._tabla[19],'-''-''-',self._tabla[20],' ','|'],
            ['|', ' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ','|'],
            [self._tabla[21], '-','-','-','-','-', self._tabla[22], '-','-','-','-','-', self._tabla[23]]
        ]

        for i in tabla:
            print("     ", end="")
            for j in i:
                print(j, end="")
            print()

    # Metoda za proveru da li je napravljena mica
    # TODO:
    def proveri_mica(self):
        pass

    # Provera da li je igra zavrsena. Igra je zavrsena ako je igrac ostao sa 2 figure
    # TODO: ili nema gde da se pomeri
    def proveri_kraj_igre(self):
        if self._igrac1.broj_figura == 2:
            self._pobednik = self._igrac2.oznaka
            return True
        if self._igrac2.broj_figura == 2:
            self._pobednik = self._igrac1.oznaka
            return True
        
        # TODO: Proveri ako nema gde da se pomeri

        return False

    # FAZA 1: Odavde pocinje igra. Postavljanje figura. Ova faza traje maksimalno 18 poteza.
    def postavi_figure(self, igrac1, igrac2):
        self._igrac1 = igrac1
        self._igrac2 = igrac2

        self.nacrtaj_tablu()

        for potez in range(18):
            if potez % 2 == 0: # Beli igrac je na potezu
                self._igrac1.postavi_figuru()
            else:              # Crni igrac je na potezu
                self._igrac2.postavi_figuru()

            self.nacrtaj_tablu()

        # TODO: poziv za FAZU 2

class Covek:
    def __init__(self, oznaka, game_instance):
        self.oznaka = oznaka
        self.broj_figura = 9
        self._game_instance = game_instance

    def postavi_figuru(self):
        while True:
            try:
                pozicija = int(input("\n[{}] unesite poziciju: ".format(self.oznaka)))
            except ValueError:
                print("Uneli ste pogresnu vrednost!")
                continue

            if pozicija == 50:  # Terminator programa
                import sys
                sys.exit()
            
            if self._game_instance.postavi_igraca(self.oznaka, pozicija):
                break

            print("Ne mozete zauzeti polje ", pozicija)

    def pomeri_figuru(self):
        pass

    def pojedi_figuru(self):
        pass

if __name__ == "__main__":
    print("\n\n---===   MICE   ===---\n\n")

    igra = Igra()
    igrac1 = Covek('W', igra)
    igrac2 = Covek('B', igra)

    igra.postavi_figure(igrac1, igrac2)