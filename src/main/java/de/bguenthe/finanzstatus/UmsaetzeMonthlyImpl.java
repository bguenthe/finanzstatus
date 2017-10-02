package de.bguenthe.finanzstatus;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

@Service
public class UmsaetzeMonthlyImpl implements UmsaetzeMonthlyService {

    @Autowired
    private UmsaetzeMonthlyRepository finanzstatusMonthlyRepository;

    @Override
    public List<UmsaetzeMonthly> getAll() {
        List<UmsaetzeMonthly> f = new ArrayList<UmsaetzeMonthly>();
        Iterator<UmsaetzeMonthly> iterator = finanzstatusMonthlyRepository.findAll().iterator();
        while (iterator.hasNext()) {
            f.add(iterator.next());
        }

        return f;
    }
}