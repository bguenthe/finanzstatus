/* vorbereitenb neuer monat */
insert into finanzstatus (institut, kontostand, datum, typ)
  select institut, kontostand, to_date(to_char(now(),'DDMMYYYY'),'DDMMYYYY'), typ FROM
    (select institut, kontostand, max(datum), typ
     FROM finanzstatus
     GROUP BY 1,2,4) a;

insert into finanzstatus (institut, kontostand, datum, typ)
  select institut, kontostand, to_date('01102017','DDMMYYYY'), typ FROM
    (select institut, kontostand, max(datum), typ
     FROM finanzstatus
     GROUP BY 1,2,4) a;

select
  sum(case when betrag > 0 THEN betrag END) "Einkuenfte",
  sum(case when betrag < 0 THEN betrag END) * -1 "Kosten"
from umsaetze;

select
  to_char(wertstellungstag, 'YYYY_MM'),
  sum(case when betrag > 0 THEN betrag END) "Einkuenfte",
  sum(case when betrag < 0 THEN betrag END) * -1 "Kosten"
from umsaetze
GROUP BY to_char(wertstellungstag, 'YYYY_MM')
order by to_char(wertstellungstag, 'YYYY_MM');


select wertstellungstag,
  sum(case when betrag > 0 THEN betrag END) "Einkuenfte",
  sum(case when betrag < 0 THEN betrag END) * -1 "Kosten"
from umsaetze where institut = 'DKB'
GROUP BY wertstellungstag
ORDER BY wertstellungstag;

/* VIEWS */
create or REPLACE view umsatz_uebersicht as
  (select to_char(wertstellungstag, 'YYYYMM') "monat",
        case
        when lower(buchungsdetails) like '%edeka%'
      or lower(buchungsdetails) like '%e-center%'
      or lower(buchungsdetails) like '%lidl%'
      or lower(buchungsdetails) like '%aldi%'
      or lower(buchungsdetails) like '%hayungas%'
      or lower(buchungsdetails) like '%famila%'
      or lower(buchungsdetails) like '%real%'
      or lower(buchungsdetails) like '%rewe%'
    then 'LBM'
    when lower(buchungsdetails) like '%haspa%' and umsaetze.betrag < 0
      or lower(buchungsdetails) like '%voba%' and umsaetze.betrag < 0or lower(buchungsdetails) like '%commerzbank%' and umsaetze.betrag < 0
      or lower(buchungsdetails) like '%commerzbank%' and umsaetze.betrag < 0
    then 'Geld abheben'
    when lower(buchungsdetails) like '%verwendungszweck bezuege%'
    then 'Gehalt'
    when lower(buchungsdetails) like '%spotify%'
    then 'Spotify'
    when lower(buchungsdetails) like '%smar tmobil.de%'
    then 'Handy'
    when lower(buchungsdetails) like '%amazon%'
    then 'Amazon'
    when lower(umsatzart) like '%zinsen/entgelt%'
    then 'Kontoführung'
    when lower(buchungsdetails) like '%aypal%' and not lower(buchungsdetails) like '%spotify%'
    then 'paypal'
  else buchungsdetails END "Posten",
  sum(case when betrag > 0 THEN betrag END) "Einkuenfte",
  sum(case when betrag < 0 THEN betrag * -1 END) "Kosten"
from umsaetze
GROUP BY 1, 2
ORDER BY 1,2);

select * from umsatz_uebersicht;

/* Monatsauswertung Umsäetze */
create OR REPLACE VIEW umsaetze_monthly as
select
  row_number() over() as id,
  to_char(wertstellungstag, 'YYYYMM') "monat",
  sum(case when betrag > 0 THEN betrag END) "einkuenfte",
  sum(case when betrag < 0 THEN betrag END) * -1 "kosten"
from umsaetze
GROUP BY to_char(wertstellungstag, 'YYYYMM')
order by to_char(wertstellungstag, 'YYYYMM');

SELECT * from umsaetze_monthly;

create or replace VIEW finanzstatus_monthly as (
  WITH summary AS (
      SELECT p.id,
        p.kontostand,
        to_char(p.datum, 'YYYYMM') datum,
        ROW_NUMBER() OVER(PARTITION BY p.institut, p.typ, to_char(p.datum, 'YYYYMM')
          ORDER BY p.timestampinserted DESC) AS rk
      FROM  finanzstatus p)
  SELECT s.datum, sum(s.kontostand)
  FROM summary s
  WHERE s.rk = 1
  GROUP BY s.datum
  ORDER BY s.datum);

select * from finanzstatus_monthly;