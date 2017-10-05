import glob
import locale

locale.setlocale(locale.LC_ALL, '')

import psycopg2

con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus', password='%dudelsack48%')
cur = con.cursor()

institut = "DKB"
typ = 'Girokonto'

# Alle PB_* Dateien lesen, komplett önnen und in das Schema
for file in glob.glob("10533*"):
    fin = open(file)
    umsätze = fin.readlines()

    datum_und_kontostand = []
    for zeile in umsätze[3:5]:
        datum_und_kontostand.append(zeile.split(";"))

    datum = datum_und_kontostand[0][1][1:-1]
    kontostand = float(locale.atof(datum_und_kontostand[1][1][1:-1]))

    try:
        cur.execute(
            "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND datum=%s ",
            (institut, typ, kontostand, datum))
        rows = cur.fetchall()
        # dublikate überlesen
        if len(rows) == 0:
            cur.execute(
                "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%S, %S, %S, %S)",
                (institut, typ, datum, kontostand))
    except Exception as e:
        print(str(e))

    for zeile in umsätze[7:]:
        # zu utf8 wandeln
        zeile.encode('utf-8')
        zeilenliste = zeile.split(";")
        wertstellungstag = zeilenliste[1][1:-1]
        umsatzart = zeilenliste[2][1:-1]
        if umsatzart == "Abschluss":
            continue
        auftraggeber = zeilenliste[3][1:-1]
        buchungsdetails = zeilenliste[4][1:-1]
        empfänger = None
        betrag = float(locale.atof(zeilenliste[7][1:-1]))
        saldo = None

        try:
            cur.execute(
                "SELECT * FROM umsaetze WHERE institut=%s AND typ=%s AND wertstellungstag=%s AND umsatzart=%s AND buchungsdetails=%s AND betrag=%s",
                (institut, typ, wertstellungstag, umsatzart, buchungsdetails, betrag))
            rows = cur.fetchall()
            # dublikate überlesen
            if len(rows) != 0:
                continue

            cur.execute(
                "INSERT INTO umsaetze (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfaenger, betrag, saldo) VALUES (%S, %S, %S, %S, %S, %S, %S, %S, %S)",
                (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger, betrag, saldo))
        except Exception as e:
            print(str(e))

con.commit()
