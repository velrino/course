FROM node:22-alpine

ENV NODE_ENV=production \
    PORT=8080 \
    DATA_DIR=/data

WORKDIR /app

RUN addgroup -S -g 10001 lab && \
    adduser -S -D -H -u 10001 -G lab lab && \
    mkdir -p /data && \
    chown -R lab:lab /app /data

COPY --chown=lab:lab app/ ./app/

USER 10001:10001
EXPOSE 8080
VOLUME ["/data"]

HEALTHCHECK --interval=5s --timeout=2s --start-period=3s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:8080/health/ready').then(r=>{if(!r.ok)process.exit(1)}).catch(()=>process.exit(1))"]

CMD ["node", "app/server.mjs"]
