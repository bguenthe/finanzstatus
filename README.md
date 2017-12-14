Dockerfile unter `/home/pirate/finanzstaus` anlegen mit Inhalt

`FROM openjdk:8u151-jre-alpine`
 
`COPY finanzstatus-0.0.1-SNAPSHOT.jar /`
 
`CMD java -jar finanzstatus-0.0.1-SNAPSHOT.jar`


Bauen
`docker build -t  finanzstaus .`

Starten
`docker run --name finanzstaus -d -p 8080:8080 finanzstaus`
