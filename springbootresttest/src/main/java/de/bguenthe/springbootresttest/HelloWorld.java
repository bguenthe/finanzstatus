package de.bguenthe.springbootresttest;

public class HelloWorld {

    private String message;

    public HelloWorld(String message){
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

}