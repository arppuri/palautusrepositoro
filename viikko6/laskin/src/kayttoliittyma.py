from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4

class Summa:
    def __init__(self, sovelluslogiikka, hae_arvo):
        self._sovelluslogiikka = sovelluslogiikka
        self._hae_arvo = hae_arvo
        self._edellinen = 0
        #self._edelliset = []

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        #self._edelliset.append(self._sovelluslogiikka.arvo())
        arvo = int(self._hae_arvo())
        self._sovelluslogiikka.plus(arvo)

    def kumoa(self):
        #self._viimeisin = self._edelliset.pop()
        self._sovelluslogiikka.aseta_arvo(self._edellinen)

class Erotus:
    def __init__(self, sovelluslogiikka, hae_arvo):
        self._sovelluslogiikka = sovelluslogiikka
        self._arvo_getter = hae_arvo
        self._edellinen = 0
        #self._edelliset = []

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        arvo = int(self._arvo_getter())
        self._sovelluslogiikka.miinus(arvo)
        #self._edelliset = []
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen)

class Nollaus:
    def __init__(self, sovelluslogiikka, hae_arvo):
        self._sovelluslogiikka = sovelluslogiikka
        self._arvo_getter = hae_arvo
        self._edellinen = 0
        #self._edelliset = []

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen)


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self._edellinen_komento = None
        self._edelliset_komennot = []

        self._komennot = {
            Komento.SUMMA: Summa(sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: Nollaus(sovelluslogiikka, self._lue_syote)
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        return self._syote_kentta.get()

    def _suorita_komento(self, komento):
        if komento in self._komennot:
            komento_olio = self._komennot[komento]
            komento_olio.suorita()
            self._edellinen_komento = komento_olio
            self._edelliset_komennot.append(komento_olio)
        else:
            self._kumoa()
        self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())

    def _kumoa(self):
        if self._edellinen_komento:
            self._edellinen_komento.kumoa()

            self._arvo_var.set(self._sovelluslogiikka.arvo())

            if not self._edellinen_komento:
                self._nollaus_painike["state"] = constants.DISABLED
            else:
                self._nollaus_painike["state"] = constants.NORMAL


        if self._edelliset_komennot:
            viimeisin_komento = self._edelliset_komennot.pop()
            viimeisin_komento.kumoa()

            self._arvo_var.set(self._sovelluslogiikka.arvo())

            if not self._edelliset_komennot:
                self._nollaus_painike["state"] = constants.DISABLED
            else:
                self._nollaus_painike["state"] = constants.NORMAL

