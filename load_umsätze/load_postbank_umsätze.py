import glob
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

import psycopg2

con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus', password='%dudelsack48%')
cur = con.cursor()

institut = "Postbank"
typ = 'Girokonto'

def get_curent_date():
    return datetime.today().strftime('%Y.%m.%d')

# Alle PB_* Dateien lesen, komplett önnen und in das Schema
for file in glob.glob("PB_*"):
    fin = open(file)
    umsätze = fin.readlines()

    kontostand_array = []
    for zeile in umsätze[5:6]:
        kontostand_array.append(zeile.split(";"))

    kontostand = float(locale.atof(kontostand_array[0][1][:-3]))
    datum = get_curent_date()

    try:
        cur.execute(
            "SELECT * FROM finanzstatus WHERE institut=%s AND typ=%s AND kontostand=%s AND datum=%s ",
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

    for zeile in umsätze[9:]:
        # zu utf8 wandeln
        #zeile.encode('utf-8')
        zeilenliste = zeile.split(";")

        wertstellungstag = zeilenliste[1][1:-1]
        umsatzart = zeilenliste[2][1:-1]
        buchungsdetails = zeilenliste[3][1:-1]
        auftraggeber = zeilenliste[4][1:-1]
        empfänger = zeilenliste[5][1:-1]
        betrag = float(locale.atof(zeilenliste[6][1:-2]))
        saldo = float(locale.atof(zeilenliste[7][1:-4]))

        try:
            cur.execute(
                "SELECT * FROM umsaetze WHERE institut=%s AND typ =%s AND wertstellungstag=%s AND umsatzart=%s AND buchungsdetails=%s AND auftraggeber=%s AND empfaenger=%s AND betrag=%s AND saldo=%s",
                (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger, betrag, saldo))
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
