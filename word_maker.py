from kludu_rekinatajs import replace_greek
import sympy as sym
from spire.doc import *
from spire.doc.common import *


def to_latex(formula):
    if isinstance(formula, str):
        return formula

    if isinstance(formula, sym.Basic):
        return sym.latex(formula)

    return str(formula)
def sqrt_to_power(latex):
    latex = str(latex)
    result = ""
    i = 0

    while i < len(latex):
        if latex.startswith(r"\sqrt{", i):
            start = i + len(r"\sqrt{")
            depth = 1
            j = start

            while j < len(latex) and depth > 0:
                if latex[j] == "{":
                    depth += 1
                elif latex[j] == "}":
                    depth -= 1

                j += 1

            if depth == 0:
                inside = latex[start:j - 1]

                # Convert nested square roots too
                inside = sqrt_to_power(inside)

                result += rf"\left({inside}\right)^{{\frac{{1}}{{2}}}}"
                i = j
                continue

        result += latex[i]
        i += 1

    return result

def add_text(section, text):
    paragraph = section.AddParagraph()
    paragraph.AppendText(str(text))
    return paragraph


def add_heading(section, text, level=1):
    paragraph = section.AddParagraph()
    paragraph.AppendText(str(text))

    if level == 1:
        paragraph.ApplyStyle(BuiltinStyle.Heading1)

    elif level == 2:
        paragraph.ApplyStyle(BuiltinStyle.Heading2)

    elif level == 3:
        paragraph.ApplyStyle(BuiltinStyle.Heading3)

    return paragraph


def add_equation(doc, section, formula):
    latex = to_latex(formula)
    latex = sqrt_to_power(latex)
    
    office_math = OfficeMath(doc)
    office_math.FromLatexMathCode(latex)

    paragraph = section.AddParagraph()
    paragraph.Items.Add(office_math)

    return paragraph


def get_unit(dati):
    mervieniba = dati.get("Mērvienība", "")

    if mervieniba == "":
        return ""

    return rf"\mathrm{{{mervieniba}}}"


def generate(results, nosauk, aprekinu_nr=None):
    doc = Document()
    section = doc.AddSection()

    if aprekinu_nr is None:
        aprekinu_nr = [1]

    aprekinu_nr = [f"Nr.{nr}" if isinstance(nr, int) else nr for nr in aprekinu_nr]

    sekcijas = [
        "Aprēķinu formulas",
        "Aprēķinu piemēri",
        "Rezultāti",
        "Rezultātu analīze",
        "Secinājumi",
        "Pielikumi"
    ]

    ### aprekinu formulas
    add_heading(section, sekcijas[0], 1)

    used_formulas = set()

    for nr in aprekinu_nr:
        for category in results:
            if nr not in category:
                continue

            for simbols in category[nr].keys():
                add_heading(section, replace_greek(str(simbols)), 2)

                for formula in category[nr][simbols]["formulas"].keys():

                    formula_bez_sk = category[nr][simbols]["formulas"][formula]
                    latex = to_latex(formula_bez_sk)

                    key = (simbols, formula, latex)

                    if key in used_formulas:
                        continue

                    used_formulas.add(key)

                    add_text(section, f"{replace_greek(str(simbols))} lieluma '{formula}' formula:")

                    s = sym.latex(sym.Symbol(str(simbols)))

                    if formula == "Kludai":
                        add_equation(doc, section, rf"\Delta {s}={latex}")

                    elif formula == "vienadojums":
                        add_equation(doc, section, rf"{s}={latex}")

                    else:
                        add_equation(doc, section, latex)


    ### aprekini
    add_heading(section, sekcijas[1], 1)

    for nr in aprekinu_nr:
        add_heading(section, nr, 2)

        for category in results:
            if nr not in category:
                continue

            for simbols in category[nr].keys():

                dati = category[nr][simbols]
                mervieniba = get_unit(dati)

                add_heading(section, f"{replace_greek(str(simbols))} aprēķins", 3)

                for formula in dati["formulas_ar_skaitliem"].keys():

                    formula_ar_sk = dati["formulas_ar_skaitliem"][formula]
                    latex = to_latex(formula_ar_sk)

                    add_text(section, f"{replace_greek(str(simbols))} lieluma '{formula}' aprēķins:")

                    s = sym.latex(sym.Symbol(str(simbols)))

                    if formula == "Kludai":
                        add_equation(doc, section, rf"\Delta {s}={latex}={dati['kluda']} \quad [{mervieniba}]")

                    elif formula == "vienadojums":
                        add_equation(doc, section, rf"{s}={latex}={dati['vertiba']} \quad [{mervieniba}]")

                    else:
                        add_equation(doc, section, rf"{latex} \quad [{mervieniba}]")


    ### rezultati
    add_heading(section, sekcijas[2], 1)
    grupeti_rezultati = {}

    for category in results:
        for nr, lielumi in category.items():

            if nr not in grupeti_rezultati:
                grupeti_rezultati[nr] = {}

            grupeti_rezultati[nr].update(lielumi)


    for nr, lielumi in grupeti_rezultati.items():

        add_heading(section, nr, 2)

        for simbols, dati in lielumi.items():

            if "vertiba" not in dati or "kluda" not in dati:
                continue

            add_text(section, replace_greek(str(simbols)))

            s = sym.latex(sym.Symbol(str(simbols)))
            mervieniba = get_unit(dati)

            add_equation(doc, section, rf"{s}=({(dati['vertiba'])}\pm {(dati['kluda'])}) \; [{mervieniba}]")


    add_heading(section, sekcijas[3], 1)
    add_text(section, "")

    add_heading(section, sekcijas[4], 1)
    add_text(section, "")

    add_heading(section, sekcijas[5], 1)
    add_text(section, "")

    doc.SaveToFile(nosauk, FileFormat.Docx2019)
    doc.Close()