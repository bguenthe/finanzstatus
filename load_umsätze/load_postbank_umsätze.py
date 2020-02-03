import glob
import locale
from datetime import datetime

import psycopg2


class Load:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        self.con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus',
                                    password='%dudelsack48%')
        self.cur = self.con.cursor()

        self.institut = "Postbank"
        self.typ = 'Girokonto'

    def get_curent_date(self):
        return datetime.today().strftime('%Y.%m.%d')

    def load_data(self):
        # Alle PB_* Dateien lesen, komplett önnen und in das Schema
        for file in glob.glob("input/Umsatzauskunft_*"):
            fin = open(file)
            umsätze = fin.readlines()

            kontostand_array = []
            for zeile in umsätze[5:6]:
                kontostand_array.append(zeile.split(";"))

            kontostand = float(locale.atof(kontostand_array[0][1][:-3]))
            datum = self.get_curent_date()

            try:
                self.cur.execute(
                    "SELECT * FROM finanzstatus WHERE institut=%s AND typ=%s AND kontostand=%s AND datum=%s ",
                    (self.institut, self.typ, kontostand, datum))
                rows = self.cur.fetchall()
                # Datei schon verarbeitet skipping...
                if len(rows) != 0:
                    print("Kontodaten für %s, %s sind Up to date" % (self.institut, self.typ))
                    continue

                self.cur.execute(
                    "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                    (self.institut, self.typ, datum, kontostand))
                print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (datum, kontostand))
            except Exception as e:
                print(str(e))
                raise (e)
            num = 0
            for num, zeile in enumerate(umsätze[0:]):
                if zeile.find("gebuchte Umsätze;") != -1:
                    startup = num + 2
                    break

            for zeile in umsätze[startup:]:
                # zeile.encode('utf-8')
                zeilenliste = zeile.split(";")

                wertstellungstag = zeilenliste[1]
                umsatzart = zeilenliste[2]
                buchungsdetails = zeilenliste[3]
                auftraggeber = zeilenliste[4]
                empfänger = zeilenliste[5]
                try:
                    betrag = float(locale.atof(zeilenliste[6][1:-2]))
                except Exception as e:
                    f = 1
                try:
                    saldo = float(locale.atof(zeilenliste[7][1:-4]))
                except Exception as e:
                    f = 1

                try:
                    self.cur.execute(
                        "SELECT * FROM umsaetze WHERE institut=%s AND typ =%s AND wertstellungstag=%s AND umsatzart=%s AND buchungsdetails=%s AND auftraggeber=%s AND empfaenger=%s AND betrag=%s AND saldo=%s",
                        (self.institut, self.typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger,
                         betrag, saldo))
                    rows = self.cur.fetchall()
                    # Einzeldaten schon verarbeitet skipping...
                    if len(rows) != 0:
                        continue

                    self.cur.execute(
                        "INSERT INTO umsaetze (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfaenger, betrag, saldo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (self.institut, self.typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger,
                         betrag, saldo))
                    print("Umsätze: Institur %s, Wertstellungstag %s eingefügt" % (self.institut, wertstellungstag))
                except Exception as e:
                    print(str(e))
                    raise (e)

        self.con.commit()
