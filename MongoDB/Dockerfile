FROM mongo:8.0

COPY ./conf/mongod.conf /etc/mongod.conf
COPY ./tools/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && \
    mkdir -p /data/db /data/configdb && \
    chown -R mongodb:mongodb /data/db /data/configdb

EXPOSE 27017
ENTRYPOINT ["/entrypoint.sh"]