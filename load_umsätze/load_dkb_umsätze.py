import glob
import locale

locale.setlocale(locale.LC_ALL, '')

import psycopg2

con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus', password='%dudelsack48%')
cur = con.cursor()

institut = "DKB"
typ = 'Keditkarte'

# Alle PB_* Dateien lesen, komplett önnen und in das Schema
for file in glob.glob("4748*"):
    fin = open(file)
    umsätze = fin.readlines()

    datum_und_kontostand = []
    for zeile in umsätze[4:6]:
        datum_und_kontostand.append(zeile.split(";"))

    kontostand = float(datum_und_kontostand[0][1][1:-5])
    datum = datum_und_kontostand[1][1][1:-1]

    try:
        cur.execute(
            "SELECT * FROM finanzstatus WHERE institut=%s AND typ = %s AND kontostand=%s AND datum=%s ",
            (institut, typ, kontostand, datum))
        rows = cur.fetchall()
        # dublikate überlesen
        if len(rows) != 0:
            continue

        cur.execute(
            "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
            (institut, typ, datum, kontostand))
    except Exception as e:
        print(str(e))


    for zeile in umsätze[8:]:
        # zu utf8 wandeln
        zeile.encode('utf-8')
        zeilenliste = zeile.split(";")
        wertstellungstag = zeilenliste[1][1:-1]
        umsatzart = "Kreditkarte"
        buchungsdetails = zeilenliste[3][1:-1]
        auftraggeber = None
        empfänger = None
        betrag = float(locale.atof(zeilenliste[4][1:-1]))
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
                "INSERT INTO umsaetze (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfaenger, betrag, saldo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger, betrag, saldo))
        except Exception as e:
            print(str(e))

con.commit()
