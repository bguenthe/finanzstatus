FROM openjdk:8u151-jre-alpine

COPY finanzstatus-0.0.1-SNAPSHOT.jar /

CMD java -jar finanzstatus-0.0.1-SNAPSHOT.jar