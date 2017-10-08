package de.bguenthe.finanzstatus.umsaetzemonthly;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "umsaetze_monthly")
public class UmsaetzeMonthly {
    @Id
    @Column(name = "id")
    private Long id; // The row number!

    @Column(name = "monat")
    private String monat;

    @Column(name = "einkuenfte")
    private String einkuenfte;

    @Column(name = "kosten")
    private String kosten;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getMonat() {
        return monat;
    }

    public void setMonat(String monat) {
        this.monat = monat;
    }

    public String getEinkuenfte() {
        return einkuenfte;
    }

    public void setEinkuenfte(String einkuenfte) {
        this.einkuenfte = einkuenfte;
    }

    public String getKosten() {
        return kosten;
    }

    public void setKosten(String kosten) {
        this.kosten = kosten;
    }
}
