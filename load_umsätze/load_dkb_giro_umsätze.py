import glob
import locale
import os
import shutil
from datetime import date

locale.setlocale(locale.LC_ALL, '')

import psycopg2


class Load:
    def __init__(self):
        self.con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus',
                                    password='%dudelsack48%')
        self.cur = self.con.cursor()

        self.institut = "DKB"
        self.typ = 'Girokonto'

    def load_data(self):
        # Alle PB_* Dateien lesen, komplett önnen und in das Schema
        for file in glob.glob("input/10533*"):
            fin = open(file)
            umsätze = fin.readlines()

            datum_und_kontostand = []
            for zeile in umsätze[3:5]:
                datum_und_kontostand.append(zeile.split(";"))

            datum = datum_und_kontostand[0][1][1:-1]
            kontostand = float(locale.atof((datum_und_kontostand[1][1][1:-1]).replace(" EUR", "")))

            try:
                self.cur.execute(
                    "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND datum=%s ",
                    (self.institut, self.typ, kontostand, datum))
                rows = self.cur.fetchall()
                # dublikate überlesen
                if len(rows) != 0:
                    print("Kontodaten für %s, %s sind Up to date" % (self.institut, self.typ))
                else:
                    self.cur.execute(
                        "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                        (self.institut, self.typ, datum, kontostand))
                    print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (datum, kontostand))
            except Exception as e:
                print(str(e))
                raise(e)
            fin.close()

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
                    self.cur.execute(
                        "SELECT * FROM umsaetze WHERE institut=%s AND typ=%s AND wertstellungstag=%s AND umsatzart=%s AND buchungsdetails=%s AND betrag=%s",
                        (self.institut, self.typ, wertstellungstag, umsatzart, buchungsdetails, betrag))
                    rows = self.cur.fetchall()
                    # dublikate überlesen
                    if len(rows) != 0:
                        print("Umsätze: Institur %s, Wertstellungstag %s überlesen (Duplikat)" % (self.institut, wertstellungstag))
                    else:
                        self.cur.execute(
                            "INSERT INTO umsaetze (institut, typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfaenger, betrag, saldo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (self.institut, self.typ, wertstellungstag, umsatzart, buchungsdetails, auftraggeber, empfänger, betrag, saldo))
                        print("Umsätze: Institur %s, Wertstellungstag %s eingefügt" % (self.institut, wertstellungstag))
                except Exception as e:
                    print(str(e))
                    raise(e)
            shutil.move(file, "input/processed/" + file.split("\\")[1] + "_" + str(date.today()))
        self.con.commit()


if __name__ == "__main__":
    loadDKBGiro = Load()
    loadDKBGiro.load_data()
