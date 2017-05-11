class Igra:
    """
    Glavna klasa koja upravlja igrom
    """

    _moguce_putanje = {
        0 : (1, 9),
        1 : (0, 2, 4),
        2 : (1, 14),
        3 : (4, 10),
        4 : (1, 3, 5, 7),
        5 : (4, 13),
        6 : (7, 11),
        7 : (4, 6, 8),
        8 : (7, 12),
        9 : (0, 10, 21),
        10: (3, 9, 11, 18),
        11: (6, 10, 15),
        12: (8, 13, 17),
        13: (5, 12, 14, 20),
        14: (2, 13, 23),
        15: (11, 16),
        16: (15, 17, 19),
        17: (12, 16),
        18: (10, 19),
        19: (16, 18, 20, 22),
        20: (13, 19),
        21: (9, 22),
        22: (19, 21, 23),
        23: (14, 22)
    }

    _moguce_mice = ((0,1,2),(3,4,5),(6,7,8),(9,10,11),(12,13,14),(15,16,17),(18,19,20),(21,22,23),
                       (0,9,21),(3,10,18),(6,11,15),(1,4,7),(16,19,22),(8,12,17),(5,13,20),(2,14,23))

    def __init__(self):
        self._slobodno_polje = 'X'
        self._tabla = [self._slobodno_polje for i in range(24)]
        self._igrac1 = None
        self._igrac2 = None
        self._pobednik = None

    # Metoda trazi preostala slobodna mesta na tabli i vraca listu indeksima polja
    def nadji_slobodna_polja(self):
        slobodna_polja = []
        for i in range(len(self._tabla)):
            if self._tabla[i] == self._slobodno_polje:
                slobodna_polja.append(i)

        return slobodna_polja

    # Metoda trazi zauzeta polja za prosledjenog igraca i vraca listu indeksa tih polja
    def nadji_zauzeta_polja(self, oznaka):
        polja = []
        for i in range(len(self._tabla)):
            if self._tabla[i] == oznaka:
                polja.append(i)

        return polja

    # Provera da li pozicija postoji
    def _proveri_poziciju(self, pozicija):
        if not 0 <= pozicija < 24:
            return False
        
        return True

    # Metoda za proveru da li je napravljena mica za prosledjenog igraca
    def proveri_micu(self, oznaka_igraca, poslednja_pozicija):
        for i, j, k in self._moguce_mice:
            if i == poslednja_pozicija or j == poslednja_pozicija or k == poslednja_pozicija:
                if self._tabla[i] == self._tabla[j] == self._tabla[k] and self._tabla[i] == oznaka_igraca:
                    return True

        return False

    def sve_u_mici(self, oznaka):
        for i in range(len(self._tabla)):
            if self._tabla[i] == oznaka:
                for j, k, l in self._moguce_mice:
                    if not self._tabla[j] == self._tabla[k] == self._tabla[l] == oznaka:
                        return True
        
        return False

    '''
    # Provera da li je neki od igaca ostao sa 3 figure. Tada je moguce skakanje za tog igraca.
    # Ovo je i uslov za Fazu 3
    def _proveri_mogucnost_skakanja(self):
        if self._igrac1.broj_figura == 3 or self._igrac2.broj_figura == 3:
            return True

        return False
    '''

    # Proveravanje da li figura sme da se krece po odredjenoj putanji
    def _proveri_putanju_pomeranja(self, stara_poz, nova_poz):
        if nova_poz in self._moguce_putanje[stara_poz]:
            return True

        return False

    # Proverava da li su sve figure igraca cija je oznaka prosledjena blokirane
    def _proveri_blokiran(self, oznaka):
        pozicije = []

        for i in range(len(self._tabla)):
            if self._tabla[i] == oznaka:
                pozicije.append(i)

        blokiran = True
        for i in pozicije:
            blokiran = self._proveri_blokirana_pozicija(i)
            if not blokiran:
                break

        return blokiran

    # Proverava da li je odredjena pozicija koja se prosledi blokirana, tj. igrac ne moze vise da pomera tu figuru
    def _proveri_blokirana_pozicija(self, pozicija):
        putanje = self._moguce_putanje

        for i in putanje[pozicija]:
            if self._tabla[i] == 'X':
                return False

        return True

    # Provera da li je igra zavrsena. Igra je zavrsena ako je igrac ostao sa 2 figure
    def proveri_kraj_igre(self):
        if self._igrac1.broj_figura == 2 or self._proveri_blokiran(self._igrac1.oznaka):
            self._pobednik = self._igrac2.oznaka
            return True
        if self._igrac2.broj_figura == 2 or self._proveri_blokiran(self._igrac1.oznaka):
            self._pobednik = self._igrac1.oznaka
            return True
        
        return False

    # Zauzimanje polja na tabli
    def postavi_igraca(self, oznaka_igraca, pozicija):
        if (not self._proveri_poziciju(pozicija)) or (self._tabla[pozicija] != self._slobodno_polje):
            return False

        self._tabla[pozicija] = oznaka_igraca
        return True

    # Pomocna metoda za minimax
    def oslobodi_polje(self, pozicija):
        self._tabla[pozicija] = self._slobodno_polje

    # Pomeranje igraca
    def pomeri_igraca(self, oznaka_igraca, stara_pozicija, nova_pozicija):
        uslov_pozicija = not self._proveri_poziciju(stara_pozicija) or not self._proveri_poziciju(nova_pozicija)
        try: # TODO: nadji malo bolji nacin za roveru ako se unese neki bezveze indeks jer ovako dolazi do exceptiona
            # a ruzno izgleda da se svi ovi uslovi stave u 1 if
            uslov_polje = self._tabla[stara_pozicija] != oznaka_igraca or self._tabla[nova_pozicija] != self._slobodno_polje
        except IndexError:
            uslov_polje = False

        if uslov_pozicija or uslov_polje or not self._proveri_putanju_pomeranja(stara_pozicija, nova_pozicija):
             return False

        self._tabla[stara_pozicija] = self._slobodno_polje
        self._tabla[nova_pozicija] = oznaka_igraca
        return True

    # Uklanjanje figure sa table. oznaka_igraca je od igraca koji jede
    def ukloni_igraca(self, oznaka_igraca, pozicija):
        if not self._proveri_poziciju(pozicija) or self._tabla[pozicija] == oznaka_igraca or self._tabla[pozicija] == self._slobodno_polje:
            return False

        if oznaka_igraca == self._igrac1.oznaka:
            if self.proveri_micu(self._igrac2.oznaka, pozicija):
                return False

            self._igrac2.broj_figura -= 1
        else:
            if self.proveri_micu(self._igrac1.oznaka, pozicija):
                return False
                
            self._igrac1.broj_figura -= 1

        self._tabla[pozicija] = self._slobodno_polje
        return True

    def set_igraci(self, igrac1, igrac2):
        self._igrac1 = igrac1
        self._igrac2 = igrac2

    # Iscrtavanje table na ekran
    def nacrtaj_tablu(self):
        tabla = [
            [self._tabla[0]+'00', '------------', self._tabla[1]+'01', '------------', self._tabla[2]+'02'],
            [' |              |              |'],
            [' |              |              |'],
            [' |   ', self._tabla[3]+'03', '-------', self._tabla[4]+'04', '-------', self._tabla[5]+'05', '   |'],
            [' |    |         |         |    |'],
            [' |    |         |         |    |'],
            [' |    |   ', self._tabla[6]+'06', '--', self._tabla[7]+'07', '--', self._tabla[8]+'08', '   |    |'],
            [' |    |    |         |    |    |'],
            [' |    |    |         |    |    |'],
            [self._tabla[9]+'09', '--', self._tabla[10]+'10', '--', self._tabla[11]+'11', '       ', self._tabla[12]+'12', '--', self._tabla[13]+'13', '--', self._tabla[14]+'14'],
            [' |    |    |         |    |    |'],
            [' |    |    |         |    |    |'],
            [' |    |   ', self._tabla[15]+'15', '--', self._tabla[16]+'16', '--', self._tabla[17]+'17', '   |    |'],
            [' |    |         |         |    |'],
            [' |    |         |         |    |'],
            [' |   ', self._tabla[18]+'18', '-------', self._tabla[19]+'19', '-------', self._tabla[20]+'20', '   |'],
            [' |              |              |'],
            [' |              |              |'],
            [self._tabla[21]+'21', '------------', self._tabla[22]+'22', '------------', self._tabla[23]+'23']
        ]

        for i in tabla:
            print("     ", end="")
            for j in i:
                print(j, end="")
            print()
    
    # Metode koje se pozivaju ukoliko je sastavljena mica za belog igraca
    def _potez_beli(self, pozicija):
        if self.proveri_micu(self._igrac1.oznaka, pozicija):
            self.nacrtaj_tablu()
            poz_pojedi = self._igrac1.pojedi_figuru()
            if poz_pojedi == -1:
                return
            self.ukloni_igraca(self._igrac1.oznaka, poz_pojedi)

    # Metode koje se pozivaju ukoliko je sastavljena mica za crnog igraca
    def _potez_crni(self, pozicija):
        if self.proveri_micu(self._igrac2.oznaka, pozicija):
            self.nacrtaj_tablu()
            poz_pojedi = self._igrac2.pojedi_figuru()
            if poz_pojedi == -1:
                return
            self.ukloni_igraca(self._igrac2.oznaka, poz_pojedi)

    # FAZA 1: Odavde pocinje igra. Postavljanje figura. Ova faza traje maksimalno 18 poteza.
    def postavi_figure(self):
        self.nacrtaj_tablu()

        for potez in range(18):
            if potez % 2 == 0: # Beli igrac je na potezu
                beli_pozicija = self._igrac1.postavi_figuru()
                self.postavi_igraca(self._igrac1.oznaka, beli_pozicija)
                self._potez_beli(beli_pozicija)
            else:              # Crni igrac je na potezu
                crni_pozicija = self._igrac2.postavi_figuru()
                self.postavi_igraca(self._igrac2.oznaka, crni_pozicija)
                self._potez_crni(crni_pozicija)

            self.nacrtaj_tablu()

        self.pomeraj_figure() # Pozivanje Faze 2

    # FAZA 2: Pomeranje figura
    def pomeraj_figure(self):
        potez = 0
        while not self.proveri_kraj_igre():
            if potez % 2 == 0: # Beli igrac je na potezu
                pozicija = self._igrac1.pomeri_figuru()
                self._potez_beli(pozicija)
            else:              # Crni igrac je na potezu
                pozicija = self._igrac2.pomeri_figuru()
                self._potez_crni(pozicija)

            self.nacrtaj_tablu()
            potez += 1

        self._kraj()

    # Ispisivanje pobednika
    def _kraj(self):
        print("\nPobednik je: ", self._pobednik)