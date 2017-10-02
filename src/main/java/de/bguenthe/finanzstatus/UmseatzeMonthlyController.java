package de.bguenthe.finanzstatus;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
public class UmseatzeMonthlyController {
    @Autowired
    private UmsaetzeMonthlyService umsaetzeMonthlyService;

    @RequestMapping(value = "/umsaetzemonthly/all")
    public List<UmsaetzeMonthly> getAll() {
        List<UmsaetzeMonthly> um = umsaetzeMonthlyService.getAll();

        return um;
    }
}