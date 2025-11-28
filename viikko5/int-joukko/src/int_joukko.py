KAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    # tämä metodi on ainoa tapa luoda listoja
    def _luo_lista(self, koko):
        return [0] * koko

    def __init__(self, kapasiteetti:int =KAPASITEETTI, kasvatuskoko:int =OLETUSKASVATUS):
        if kapasiteetti <= 0 or kasvatuskoko <= 0:
            raise ValueError("Kapasiteetin ja kasvatuskoon oltava suurempia kuin 0")
        self.kapasiteetti = kapasiteetti
        self.kasvatuskoko = kasvatuskoko

        self.ljono = self._luo_lista(self.kapasiteetti)
        self.alkioiden_lkm = 0


    def kuuluu(self, n):
        for i in range(0, self.alkioiden_lkm):
            if self.ljono[i] == n:
                return True
        return False

    def lisaa(self, n):
        if self.kuuluu(n):
            return False

            # ei mahdu enempää, luodaan uusi säilytyspaikka luvuille
        if self.alkioiden_lkm >= len(self.ljono):
            uusi_lista = self._luo_lista(len(self.ljono) + self.kasvatuskoko)
            self.kopioi_lista(self.ljono, uusi_lista)
            self.ljono = uusi_lista

        self.ljono[self.alkioiden_lkm] = n
        self.alkioiden_lkm += 1
        return True


    def poista(self, n):
        poistettava_indeksi = -1
        for i in range(0, self.alkioiden_lkm):
            if self.ljono[i] == n:
                poistettava_indeksi = i
                break

        if poistettava_indeksi == -1:
            return False

        self.alkioiden_lkm -= 1
        for j in range(poistettava_indeksi, self.alkioiden_lkm):
            self.ljono[j] = self.ljono[j + 1]

        return True


    def kopioi_lista(self, a, b):
        j = min(len(a), len(b))
        for i in range(j):
            b[i] = a[i]

    def mahtavuus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        int_list = self._luo_lista(self.alkioiden_lkm)

        for i in range(0, self.alkioiden_lkm):
            int_list[i] = self.ljono[i]

        return int_list

    def __str__(self):
        if self.alkioiden_lkm == 0:
            return "{}"
        elif self.alkioiden_lkm == 1:
            return "{" + str(self.ljono[0]) + "}"
        else:
            tuotos = "{"
            for i in range(0, self.alkioiden_lkm - 1):
                tuotos = tuotos + str(self.ljono[i])
                tuotos = tuotos + ", "
            tuotos = tuotos + str(self.ljono[self.alkioiden_lkm - 1])
            tuotos = tuotos + "}"
            return tuotos


    @staticmethod
    def yhdiste(a, b):
        x = IntJoukko()

        for i in a.to_int_list():
            x.lisaa(i)

        for i in b.to_int_list():
            x.lisaa(i)

        return x

    @staticmethod
    def leikkaus(a, b):
        y = IntJoukko()
        for i in a.to_int_list():
            if b.kuuluu(i):
                y.lisaa(i)
        return y

    @staticmethod
    def erotus(a, b):
        z = IntJoukko()
        for i in a.to_int_list():
            z.lisaa(i)
        for i in b.to_int_list():
            z.poista(i)

        return z

