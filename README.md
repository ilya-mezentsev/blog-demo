# blog-demo
Blog API demo

# Deploy
* Clone repo:
```bash
$ git clone https://github.com/ilya-mezentsev/blog-demo.git && cd blog-demo
```

* Build containers:
```bash
$ make containers-build
```

* Run DB and permission service containers:
```bash
$ make containers-run
```

* Prepare tests data:
```bash
$ make init-test-data
```

* Run API container:
```bash
$ make containers-hl-run
```

* Run high load tests:
  * Master - ```$ make start-load-test-master```
  * Worker (can be started [multiple times](http://docs.locust.io/en/stable/running-locust-distributed.html)) - ```$ make start-load-test-worker```

* Watch containers stats:
```bash
$ docker stats
```

* Prometheus exported metrics is available here - localhost:9090; examples:
  * avg(request_processing_seconds_sum{app_name='blog-demo-api'} / request_processing_seconds_count{app_name='blog-demo-api'})
  * max(request_processing_seconds_sum{app_name='blog-demo-api'} / request_processing_seconds_count{app_name='blog-demo-api'})
  * avg(rate(request_processing_seconds_sum{app_name="blog-demo-api", endpoint!~"/alert|/metrics"}[10s])) / avg(rate(request_processing_seconds_count{app_name="blog-demo-api", endpoint!~"/alert|/metrics"}[10s]))
