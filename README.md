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

* Run high load tests (required [artillery](https://artillery.io/) to be installed):
```bash
$ make start-load-test
```

* Watch containers stats:
```bash
$ docker stats
```

* Prometheus exported metrics is available here - localhost:9090; examples:
  * avg(request_processing_seconds_sum{app_name='blog-demo-api'} / request_processing_seconds_count{app_name='blog-demo-api'})
  * max(request_processing_seconds_sum{app_name='blog-demo-api'} / request_processing_seconds_count{app_name='blog-demo-api'})
  * avg(rate(request_processing_seconds_sum{app_name='blog-demo-api'}[5m])) / avg(rate(request_processing_seconds_count{app_name='blog-demo-api'}[5m]))
