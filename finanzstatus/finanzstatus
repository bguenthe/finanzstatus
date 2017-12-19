'''
Created on 18.12.2017

@author: claube
'''

import json

import psycopg2
from bottle import route, run, abort

con = psycopg2.connect(host="192.168.178.35", database='finanzstatus', user='finanzstatus', password='%dudelsack48%')
cur = con.cursor()


@route("/vermoegenmonthly/all", method='GET')
def get_vermoegenmonthly():
    li = []
    try:
        cur.execute("SELECT id, monat, vermoegen FROM finanzstatus_monthly")
        rows = cur.fetchall()
        i = 0
        for row in rows:
            data = {'id': row[0], 'monat': row[1], 'vermoegen': str(row[2])}
            li = li + [data]
        ret = json.dumps(li)
        return ret
    except Exception as e:
        abort(404, str(e))


@route("/umsaetzemonthly/all", method='GET')
def get_umseatzemonthly():
    li = []
    try:
        cur.execute("SELECT id, monat, einkuenfte, kosten FROM umsaetze_monthly")
        rows = cur.fetchall()
        i = 0
        for row in rows:
            data = {'id': row[0], 'monat': row[1], 'einkuenfte': str(row[2]), 'kosten': str(row[3])}
            li = li + [data]
        ret = json.dumps(li)
        return ret
    except Exception as e:
        abort(404, str(e))


run(host='0.0.0.0', port=8080)
