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

select * from finanzstatus order by datum;

select * from umsaetze order by wertstellungstag;
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


select institut, wertstellungstag,
  sum(case when betrag > 0 THEN betrag END) "Einkuenfte",
  sum(case when betrag < 0 THEN betrag END) * -1 "Kosten"
from umsaetze
GROUP BY institut, wertstellungstag
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
    when buchungsdetails like '%ABSCHLAG Gas%'
    then 'Gas'
    when buchungsdetails like '%HAMBURG ENERGIE%'
    then 'Strom'
    when buchungsdetails like '%WILHELM.TEL%'
    then 'WILHELM.TEL'
    when buchungsdetails like '%LS0310000899393%'
    then 'Stadtwerke Abwasser'
    when buchungsdetails like '%004182867288%'
    then '1&1'
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
  row_number() over() as id, -- für SPRING
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
        p.kontostand as kontostand,
        to_char(p.datum, 'YYYYMM') as monat,
        ROW_NUMBER() OVER(PARTITION BY p.institut, p.typ, to_char(p.datum, 'YYYYMM')
          ORDER BY p.timestampinserted DESC) AS rk
      FROM  finanzstatus p)
  SELECT
    row_number() over() as id,
    s.monat,
    sum(s.kontostand) as vermoegen
  FROM summary s
  WHERE s.rk = 1
  GROUP BY s.monat
  ORDER BY s.monat);

drop VIEW finanzstatus_monthly;

select * from finanzstatus order by datum desc;

select buchungsdetails, auftraggeber, empfaenger, betrag from umsaetze where to_char(wertstellungstag,'YYYYMM') = '201804' order by wertstellungstag;

select * from finanzstatus_monthly
order by monat desc;

select * from umsaetze order by wertstellungstag desc;