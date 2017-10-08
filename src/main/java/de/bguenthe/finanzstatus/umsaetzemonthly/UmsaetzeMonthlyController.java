package de.bguenthe.finanzstatus.umsaetzemonthly;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@RestController
public class UmsaetzeMonthlyController {
    @Autowired
    private UmsaetzeMonthlyService umsaetzeMonthlyService;

    @RequestMapping(value = "/umsaetzemonthly/all")
    public List<UmsaetzeMonthly> getAll() {
        List<UmsaetzeMonthly> um = umsaetzeMonthlyService.getAll();

        return um;
    }

    @ExceptionHandler
    void handleIllegalArgumentException(
            IllegalArgumentException e, HttpServletResponse response) throws IOException {

        response.sendError(HttpStatus.BAD_REQUEST.value());

    }
}