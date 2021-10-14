FROM prom/prometheus

ADD prometheus.yaml /etc/prometheus/prometheus.yml
ADD rules.yaml /etc/prometheus/rules.yaml

EXPOSE 9090
