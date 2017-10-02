package de.bguenthe.springbootresttest;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;

@RestController
public class HelloWorldController {

    @RequestMapping("/sayHello")
    public ArrayList<String> sayHello() {
        ArrayList<String> bikes = new ArrayList<String>();
        bikes.add("CBR250R");
        bikes.add("Ninja250R");

        return bikes;
    }
}