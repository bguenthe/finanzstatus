package de.bguenthe.finanzstatus.vermoegenmonthly;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "finanzstatus_monthly")
public class VermoegenMonthly {
    @Id
    @Column(name = "id")
    private Long id;

    @Column(name = "monat")
    private String monat;

    @Column(name = "vermoegen")
    private String vermoegen;


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

    public String getVermoegen() {
        return vermoegen;
    }

    public void setVermoegen(String kosten) {
        this.vermoegen = vermoegen;
    }
}
