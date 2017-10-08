package de.bguenthe.finanzstatus.vermoegenmonthly;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@RestController
public class VermoegenMonthlyController {
    @Autowired
    private VermoegenMonthlyService vermoegenMonthlyService;

    @RequestMapping(value = "/vermoegenmonthly/all")
    public List<VermoegenMonthly> getAll() {
        List<VermoegenMonthly> vermoegenMonthlies = vermoegenMonthlyService.getAll();

        return vermoegenMonthlies;
    }

    @ExceptionHandler
    void handleIllegalArgumentException(
            IllegalArgumentException e, HttpServletResponse response) throws IOException {

        response.sendError(HttpStatus.BAD_REQUEST.value());

    }
}