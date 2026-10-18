import numpy as np
from math import sqrt
import sympy as sym
import copy
import math

class tiesas_kludas():
    def __init__(self, merijumi: list = None, merierices_pamatkluda: float = None, beta: float = 0.95, simbols = None):
        self.merijumi = merijumi
        self.beta = beta
        self.merierices_pamatkluda = merierices_pamatkluda
        self.stjudenta_koef =  {0.70: {2: 1.96, 3: 1.39, 4: 1.25, 5: 1.19, 6: 1.16},
                                0.95: {2: 12.71,
                                       3: 4.30,
                                       4: 3.18,
                                       5: 2.78,
                                       6: 2.57,
                                       7: 2.45,
                                       8: 2.36,
                                       9: 2.31,
                                       10: 2.26,
                                       11: 2.23,
                                       12: 2.20,
                                       13: 2.18,
                                       14: 2.16,
                                       15: 2.15,
                                       16: 2.13,
                                       17: 2.12,
                                       "bezg": 1.96},
                                0.99: {}
                                }
        self.gadijuma_kluda = 0
        self.sistematiska_kluda = 0
        self.galiga_kluda = 0
        self.galeja_vertiba = 0
        self.simbols = simbols
        self.rezultats = {self.simbols: {"vertiba": None, "kluda": None}}
        self.formulas = {}
        self.formulas_ar_skaitliem = {}


    def atjaunot_kludas(self):
        self.gadijuma_kluda = 0
        self.sistematiska_kluda = 0
        self.galiga_kluda = 0
        self.rezultats = {self.simbols: {"vertiba": None, "kluda": None}}
        self.formulas = {}
        self.formulas_ar_skaitliem = {}
        
    def apr_kludas(self):
        self.atjaunot_kludas()
        self.sistematiska_kluda = self.apr_sist_kludu()
        self.gadijuma_kluda = self.apr_gad_kludu()
        self.galiga_kluda = self.dabut_galigo_kludu()
        self.rezultats[self.simbols]["vertiba"] = self.galeja_vertiba
        self.rezultats[self.simbols]["kluda"] = self.galiga_kluda
        self.rezultats[self.simbols]["formulas"] = self.formulas.copy()
        self.rezultats[self.simbols]["formulas_ar_skaitliem"] = self.formulas_ar_skaitliem.copy()
        return self.rezultats

    def apr_gad_kludu(self): # aprēķina gadījuma absolūto kļūdu
        merijumu_sk = len(self.merijumi)
        vid_arit = np.mean(self.merijumi)
        s = sym.latex(sym.Symbol(str(self.simbols)))
        self.formulas["videja_vertiba"] = rf"{s}_{{vid}}=\frac{{\sum_{{i=1}}^n {s}_i}}{{n}}"
        self.formulas_ar_skaitliem["videja_vertiba"] = rf"{s}_{{vid}}=\frac{{{' + '.join(map(str, self.merijumi))}}}{{{merijumu_sk}}}={vid_arit}"
        merijumu_kludas = []
        if merijumu_sk > 1: # ja vairāk par 1 mērījumu, tad rēķina gadījuma kļūdu
            for merijums in self.merijumi:
                kluda = merijums - vid_arit
                merijumu_kludas.append(kluda)

            kv_kludas = []
            for kluda in merijumu_kludas:
                kv_kludas.append(kluda**2)

            vid_kv_kluda = sqrt(sum(kv_kludas)/(merijumu_sk*(merijumu_sk-1)))
            gadijuma_kluda = vid_kv_kluda*self.stjudenta_koef[self.beta][merijumu_sk]
            self.galeja_vertiba = vid_arit
            self.formulas["gadijuma_kluda"] = rf"\Delta {s}_s=t_\beta(n)\sqrt{{\frac{{\sum_{{i=1}}^n({s}_i-{s}_{{vid}})^2}}{{n(n-1)}}}}"
            summa = " + ".join(rf"({x}-({vid_arit}))^2" for x in self.merijumi)
            self.formulas_ar_skaitliem["gadijuma_kluda"] = rf"\Delta {s}_s={self.stjudenta_koef[self.beta][merijumu_sk]}\sqrt{{\frac{{{summa}}}{{{merijumu_sk}({merijumu_sk}-1)}}}}={gadijuma_kluda}"
            return gadijuma_kluda
        else: # ja ir tikai viena vērtība, pieņem, ka gadījuma kļūda ir 0
            self.galeja_vertiba = self.merijumi[0]
            return 0
    
    def apr_sist_kludu(self): # aprēķina sistemātisko absolūto kļūdu
        sistematiska_kluda = (self.merierices_pamatkluda/3)*self.stjudenta_koef[self.beta]["bezg"]
        s = sym.latex(sym.Symbol(str(self.simbols)))
        self.formulas["sistematiska_kluda"] = rf"\Delta {s}_\delta=t_\beta(\infty)\frac{{\delta {s}}}{{3}}"
        self.formulas_ar_skaitliem["sistematiska_kluda"] = rf"\Delta {s}_\delta={self.stjudenta_koef[self.beta]['bezg']}\frac{{{self.merierices_pamatkluda}}}{{3}}={sistematiska_kluda}"
        return sistematiska_kluda
    
    def dabut_galigo_kludu(self): # izlemj, kas būs kā galīgā absolūtā kļūda
        s = sym.latex(sym.Symbol(str(self.simbols)))
        self.formulas["galiga_kluda"] = rf"\Delta {s}=\sqrt{{(\Delta {s}_s)^2+(\Delta {s}_\delta)^2}}"
        if self.gadijuma_kluda > 0 and self.sistematiska_kluda > 0: # turpina, ja abas kļūdas nav 0
            atskiriba = self.gadijuma_kluda/self.sistematiska_kluda
            galiga_kluda = None
            if atskiriba >= 3 or (1/atskiriba)>=3: # pārbauda vai kļūdas atšķirās vairāk par 3 reizēm
                if atskiriba >= 3:
                    galiga_kluda = self.gadijuma_kluda
                    self.formulas_ar_skaitliem["galiga_kluda"] = rf"\Delta {s}={galiga_kluda}"
                else:
                    galiga_kluda = self.sistematiska_kluda
                    self.formulas_ar_skaitliem["galiga_kluda"] = rf"\Delta {s}={galiga_kluda}"
            else: # ja atšķirās mazāk par 3 reizēm, saskaita kļūdas pēc kļūdu saskaitīšanas likuma
                galiga_kluda = sqrt(self.gadijuma_kluda**2 + self.sistematiska_kluda**2)
                self.formulas_ar_skaitliem["galiga_kluda"] = rf"\Delta {s}=\sqrt{{({self.gadijuma_kluda})^2+({self.sistematiska_kluda})^2}}={galiga_kluda}"
            return galiga_kluda
        else: # ja kāda no kļūdām ir 0, tad galīgo kļūdu pieņem, kā kļūdu summu
            self.formulas_ar_skaitliem["galiga_kluda"] = rf"\Delta {s}={self.gadijuma_kluda}+{self.sistematiska_kluda}={self.gadijuma_kluda+self.sistematiska_kluda}"
            return self.gadijuma_kluda+self.sistematiska_kluda


class netiesas_kludas():
    def __init__(self, vienadojums: sym, syms: list, vertibas_un_kludas):
        self.vienadojums = vienadojums
        self.syms = syms
        self.vertibas_un_kludas = vertibas_un_kludas
        self.delta_syms = []
        for symbol in syms:
            self.delta_syms.append(sym.symbols(f"Delta_{symbol}"))
        pass
    def parciala_atvasinasana(self): # parciāli atvasina vienādojumu
        parcialie_atvasinajumi = {}
        for symbol in self.syms:
            parcialie_atvasinajumi[f"diff_{symbol}"] = sym.diff(self.vienadojums, symbol)
        return parcialie_atvasinajumi
    
    def kludu_saskaitisana(self): # saskaita parciālos atvasinājumu un kļūdu reizinājumu kvadrātus un izvelkt kvadrātsakni
        kvadratu_summa = 0
        parcialie_atvasinajumi = self.parciala_atvasinasana()
        for symbol, delta_symbol in zip(self.syms, self.delta_syms):
            kvadratu_summa += (parcialie_atvasinajumi[f"diff_{symbol}"]*delta_symbol)**2
        rezultats = sym.sqrt(kvadratu_summa)
        return rezultats

    def iegut_rezultatu(self): # ieliek skaitļus vienādojumā
        vertibas = {}
        kvadratu_summa = self.kludu_saskaitisana()
        for symbol, delta_symbol in zip(self.syms, self.delta_syms):
            vertibas[symbol] = self.vertibas_un_kludas[str(symbol)]["vertiba"]
            vertibas[delta_symbol] = self.vertibas_un_kludas[str(symbol)]["kluda"]
        rezultats = kvadratu_summa.subs(vertibas)
        vienadojuma_rezultats = self.vienadojums.subs(vertibas)
        
        symbol_names = {symbol: str(value) for symbol, value in vertibas.items()}
        kluda_f_sk = sym.latex(kvadratu_summa, symbol_names=symbol_names)
        vien_sk = sym.latex(self.vienadojums, symbol_names=symbol_names)

        return {"vertiba": vienadojuma_rezultats,
                "kluda": rezultats, 
                "formulas": {"Kludai": str(sym.latex(kvadratu_summa)).replace("Delta_", "Delta "), "vienadojums": sym.latex(self.vienadojums)},
                "formulas_ar_skaitliem": {"Kludai": kluda_f_sk, "vienadojums": vien_sk}}
    
    
def aprekinat_tiesas_kludas(visi_merijumi: list):
    kludu_rekinatajs = tiesas_kludas() # izveido kludu rekinataja objektu
    kludas = {}
    for merijuma_kategorija in visi_merijumi: # iziet cauri visam kategorijām
        i = 0
        kludu_rekinatajs.merierices_pamatkluda = merijuma_kategorija["merierices pamatkluda"]
        kludu_rekinatajs.simbols = merijuma_kategorija["simbols"]
        
        for merijumi in merijuma_kategorija["merijumi"]:  # iziet cauri visiem mērījumiem kategorijā
            i+=1
            kludu_rekinatajs.merijumi = merijumi
            rezultats = kludu_rekinatajs.apr_kludas()[merijuma_kategorija["simbols"]]
            try:
                kludas[f"Nr.{i}"][merijuma_kategorija["simbols"]] = rezultats
            except:
                kludas[f"Nr.{i}"] = {merijuma_kategorija["simbols"]: rezultats}
            kludas[f"Nr.{i}"][merijuma_kategorija["simbols"]].update({"Mērvienība": merijuma_kategorija["Mērvienība"]}) 
    return kludas


def uzlikt_pakapi_tiesam_kludam(kludas: dict, kludu_simboli_ar_pakapem: dict):
    for key in kludas.keys():
        for simbols in kludu_simboli_ar_pakapem.keys():
            kludas[key][simbols]["vertiba"] = kludas[key][simbols]["vertiba"]*10**(kludu_simboli_ar_pakapem[simbols])
            kludas[key][simbols]["kluda"] = kludas[key][simbols]["kluda"]*10**(kludu_simboli_ar_pakapem[simbols])
    return kludas


def aprekinat_netiesas_kludas(kludas: dict, vienadojums: sym, simbols, syms, mervieniba: str = ""):
    rezultats = {}

    for nr, dati in kludas.items():
        try:
            netiesa_kluda = netiesas_kludas(syms=syms, vienadojums=vienadojums, vertibas_un_kludas=dati)
            rez = netiesa_kluda.iegut_rezultatu()

            rezultats[nr] = {simbols: rez}
            rezultats[nr][simbols].update({"Mērvienība": mervieniba})

        except Exception as e:
            print(f"{simbols} {nr} Failed: {e}")

    return rezultats

def replace_greek(text: str) -> str:
    replacements = {
        "alpha": "α",
        "beta": "β",
        "gamma": "γ",
        "delta_": "Δ",
        "epsilon": "ε",
        "zeta": "ζ",
        "eta": "η",
        "theta": "θ",
        "iota": "ι",
        "kappa": "κ",
        "lambda": "λ",
        "mu": "μ",
        "nu": "ν",
        "xi": "ξ",
        "omicron": "ο",
        "pi": "π",
        "rho": "ρ",
        "sigma": "σ",
        "tau": "τ",
        "upsilon": "υ",
        "phi": "φ",
        "chi": "χ",
        "psi": "ψ",
        "omega": "ω",
    }

    for name, symbol in replacements.items():
        text = text.replace(name, symbol)
    return text



import copy
import math


def round_pair(value, error, sig=3):
    try:
        value = float(value)
        error = float(error)
    except (TypeError, ValueError):
        return str(value), str(error)

    if not math.isfinite(error):
        return str(value), str(error)

    if error == 0:
        return str(value), "0"

    exponent = math.floor(math.log10(abs(error)))
    decimals = sig - exponent - 1

    if decimals > 0:
        error_rounded = f"{error:.{decimals}f}"
        value_rounded = f"{value:.{decimals}f}"
    else:
        error_rounded = f"{round(error, decimals):.0f}"
        value_rounded = f"{round(value, decimals):.0f}"

    return value_rounded, error_rounded


def round_results(results, sig=3):
    rounded = copy.deepcopy(results)

    for category in rounded:
        for nr, lielumi in category.items():
            for simbols, dati in lielumi.items():

                if "vertiba" not in dati or "kluda" not in dati:
                    continue

                dati["vertiba"], dati["kluda"] = round_pair(
                    dati["vertiba"],
                    dati["kluda"],
                    sig
                )

    return rounded


### Mērījumu noformēšanas piemērs ###

""" 
laika_merijumi = [
    [1.444,	1.403,	1.387,	1.398,	1.406],
    [1.2,	1.186,	1.192,	1.195,	1.186],
    [0.506,	0.503,	0.505,	0.502,	0.502],
    [0.429,	0.429,	0.43,	0.428,	0.426],
    [0.245,	0.242,	0.244,	0.247,	0.242],
    [0.209,	0.211,	0.212,	0.207,	0.239]]

h_merijumi = [[81],[81],[221],[221],[321],[321]]

H_merijumi = [[380.5],[380.5],[240.5],[240.5],[140.5],[140.5]]

visi_merijumi = [{"merierices pamatkluda": 0.001, "merijumi": laika_merijumi, "simbols": "t"},
                  {"merierices pamatkluda": 0.05, "merijumi": h_merijumi, "simbols": "h"},
                    {"merierices pamatkluda": 0.05, "merijumi": H_merijumi, "simbols": "H"}]
"""

### Kad mērījumi ir sarakstīti, var veikt tiešo kļūdu aprēķinu ###

"""
tieso_merijumu_kludas = aprekinat_tiesas_kludas(visi_merijumi)
"""

### Kad tiešās kļūdas ir aprēķinātas, var veikt netiešo kļūdu aprēķinu ###

"""
t, h, H = sym.symbols("t h H")    # izveido simbolus priekš vienādojuma
symbols = [t, h, H]
a = (H**2)/(2*h*t**2)             # uzraksta vienādojumu izmantojot iepriekš izveidotos simbolus
netieso_merijumu_kludas = aprekinat_netiesas_kludas(kludas=tieso_merijumu_kludas_aprekiniem, vienadojums=a, simbols="a", syms=symbols)
"""

### Nepieciešamības gadījumā var pielikt pakāpi nepieciešamām vērtībām ar noteiktiem simboliem, pēc tiešo kļūdu aprēķina ###

"""
i = {"h": -3, "H": -3}
tieso_merijumu_kludas_aprekiniem = uzlikt_pakapi_tiesam_kludam(kludas=tieso_merijumu_kludas, kludu_simboli_ar_pakapem=i)
"""

