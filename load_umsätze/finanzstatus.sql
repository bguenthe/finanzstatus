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

select wertstellungstag,
  buchungsdetails,
  case when betrag > 0 THEN betrag END "Einkuenfte",
  case when betrag < 0 THEN betrag * -1 END "Kosten"
from umsaetze where institut = 'DKB'
ORDER BY wertstellungstag;

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