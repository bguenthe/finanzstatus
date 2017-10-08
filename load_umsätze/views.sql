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
               or lower(buchungsdetails) like '%voba%' and umsaetze.betrag < 0
               or lower(buchungsdetails) like '%commerzbank%' and umsaetze.betrag < 0
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

create OR REPLACE VIEW umsaetze_monthly as
  select
    row_number() over() as id,
    to_char(wertstellungstag, 'YYYYMM') "monat",
    sum(case when betrag > 0 THEN betrag END) "einkuenfte",
    sum(case when betrag < 0 THEN betrag END) * -1 "kosten"
  from umsaetze
  GROUP BY to_char(wertstellungstag, 'YYYYMM')
  order by to_char(wertstellungstag, 'YYYYMM');

create OR REPLACE VIEW finanzstatus_monthly as
  select
    row_number() over() as id,
    to_char(datum, 'YYYYMM') "monat",
    sum(kontostand)
  from finanzstatus
    WHERE datum in (select max(datum)
                    from finanzstatus
    )
  GROUP BY to_char(datum, 'YYYYMM')
  order by to_char(datum, 'YYYYMM');

create or replace VIEW finanzstatus_monthly as (
select row_number() over() as id, monat, vermoegen from (
WITH maxdate (institut, typ, maxtimestamp) AS
(SELECT
   institut,
   typ,
   max(timestampinserted)
 FROM finanzstatus
 GROUP BY 1, 2)
SELECT to_char(datum, 'YYYYMM') "monat",
  sum(kontostand) as vermoegen
FROM finanzstatus
  JOIN maxdate ON finanzstatus.timestampinserted = maxdate.maxtimestamp AND finanzstatus.institut = maxdate.institut AND
                  finanzstatus.typ = maxdate.typ
GROUP BY 1
ORDER BY 1) a);

select * from finanzstatus_monthly;


select
  row_number() over() as id,
  to_char(datum, 'YYYYMM') "monat",
  sum(kontostand)
from finanzstatus
WHERE datum in (select max(datum)
                from finanzstatus
);

select sum(s) from (
select institut, typ, max(to_char(datum, 'YYYYMM')), sum(kontostand) as s
    from finanzstatus
GROUP BY 1, 2) a;


select institut, typ, max(datum)
from finanzstatus
GROUP BY 1, 2

select * from  finanzstatus_monthly;