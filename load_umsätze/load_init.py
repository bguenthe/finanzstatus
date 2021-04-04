import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

import psycopg2


class Load:
    def __init__(self):
        self.con = psycopg2.connect(host='192.168.178.35', database='finanzstatus', user='finanzstatus',
                                    password='%dudelsack48%')
        self.cur = self.con.cursor()
        self.datum = self.get_curent_date()

        self.Postbank_institut = "Postbank"
        self.Postbank_sparcard_typ = 'SparCard direkt'
        self.Postbank_sparcard_kontostand = float(14.48)

        self.Postbank_sparcard_plus_typ = 'SparCard 3000 plus'
        self.Postbank_sparcard_plus_kontostand = float(2.01)

        self.Postbank_dax_typ = 'DAX Sparbuch'
        self.Postbank_dax_kontostand = float(60.36)

        self.Postbank_depot_typ = 'Depot&Anlagekonto'
        self.Postbank_depot_kontostand = float(1314.51)

    def get_curent_date(self):
        return datetime.today().strftime('%Y.%m.%d')

    def load_data(self):
        strdatum = datetime.today().strftime('%Y%m')
        try:
            self.cur.execute(
                "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND to_char(datum,'YYYYMM')=%s ",
                (self.Postbank_institut, self.Postbank_sparcard_plus_typ, self.Postbank_sparcard_plus_kontostand,
                 strdatum))
            rows = self.cur.fetchall()
            # dublikate überlesen
            if len(rows) == 0:
                self.cur.execute(
                    "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                    (self.Postbank_institut, self.Postbank_sparcard_plus_typ, self.datum,
                     self.Postbank_sparcard_plus_kontostand))
                print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (
                self.datum, self.Postbank_sparcard_plus_kontostand))
            else:
                print(
                    "Kontodaten für %s, %s sind Up to date" % (self.Postbank_institut, self.Postbank_sparcard_plus_typ))
        except Exception as e:
            print(str(e))

        try:
            self.cur.execute(
                "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND to_char(datum,'YYYYMM')=%s ",
                (self.Postbank_institut, self.Postbank_sparcard_typ, self.Postbank_sparcard_kontostand, strdatum))
            rows = self.cur.fetchall()
            # dublikate überlesen
            if len(rows) == 0:
                self.cur.execute(
                    "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                    (self.Postbank_institut, self.Postbank_sparcard_typ, self.datum, self.Postbank_sparcard_kontostand))
                print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (
                self.datum, self.Postbank_sparcard_plus_kontostand))
            else:
                print(
                    "Kontodaten für %s, %s sind Up to date" % (self.Postbank_institut, self.Postbank_sparcard_plus_typ))
        except Exception as e:
            print(str(e))

        try:
            self.cur.execute(
                "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND to_char(datum,'YYYYMM')=%s ",
                (self.Postbank_institut, self.Postbank_dax_typ, self.Postbank_dax_kontostand, strdatum))
            rows = self.cur.fetchall()
            # dublikate überlesen
            if len(rows) == 0:
                self.cur.execute(
                    "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                    (self.Postbank_institut, self.Postbank_dax_typ, self.datum, self.Postbank_dax_kontostand))
                print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (self.datum, self.Postbank_dax_kontostand))
            else:
                print("Kontodaten für %s, %s sind Up to date" % (self.Postbank_institut, self.Postbank_dax_typ))
        except Exception as e:
            print(str(e))

        try:
            self.cur.execute(
                "SELECT * FROM finanzstatus WHERE institut=%s AND typ =%s AND kontostand=%s AND to_char(datum,'YYYYMM')=%s ",
                (self.Postbank_institut, self.Postbank_depot_typ, self.Postbank_depot_kontostand, strdatum))
            rows = self.cur.fetchall()
            # dublikate überlesen
            if len(rows) == 0:
                self.cur.execute(
                    "INSERT INTO finanzstatus (institut, typ, datum, kontostand) VALUES (%s, %s, %s, %s)",
                    (self.Postbank_institut, self.Postbank_depot_typ, self.datum, self.Postbank_depot_kontostand))
                print("Kontodaten Datum: %s, Kontostand %s eingefügt" % (self.datum, self.Postbank_depot_kontostand))
            else:
                print("Kontodaten für %s, %s sind Up to date" % (self.Postbank_institut, self.Postbank_depot_typ))
        except Exception as e:
            print(str(e))

        self.con.commit()
