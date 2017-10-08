package de.bguenthe.finanzstatus.vermoegenmonthly;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

@Service
public class VermoegenMonthlyImpl implements VermoegenMonthlyService {

    @Autowired
    private VermoegenMonthlyRepository finanzstatusMonthlyRepository;

    @Override
    public List<VermoegenMonthly> getAll() {
        List<VermoegenMonthly> f = new ArrayList<VermoegenMonthly>();
        Iterator<VermoegenMonthly> iterator = finanzstatusMonthlyRepository.findAll().iterator();
        while (iterator.hasNext()) {
            f.add(iterator.next());
        }

        return f;
    }
}