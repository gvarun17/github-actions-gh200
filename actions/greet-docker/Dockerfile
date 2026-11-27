FROM alpine:3.20
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Exec form so the runner passes `args` as "$1", "$2", ...
ENTRYPOINT ["/entrypoint.sh"]
