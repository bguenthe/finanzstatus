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

select * from umsatz_uebersicht;

select * from umsaetze where lower(buchungsdetails) like '%abruf%' ORDER BY 2;

select * from umsaetze where institut = 'DKB' order by wertstellungstag desc;

select 'Postbank', count(*) from umsaetze where institut = 'Postbank'
UNION
select 'DKB', count(*) from umsaetze where institut = 'DKB';

delete from umsaetze;

delete from finanzstatus;

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