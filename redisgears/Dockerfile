FROM redislabs/redisgears

COPY entrypoint.sh /entrypoint.sh
COPY gears_init.py /gears_init.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]