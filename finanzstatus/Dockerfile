FROM  resin/rpi-raspbian:stretch

# install Python 3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-psycopg2 \
    python3-bottle \
    --no-install-recommends

COPY finanzstatus.py /

CMD python3 /finanzstatus.py