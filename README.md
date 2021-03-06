# bandcd
Bandcamp.com automation tools written in Python and Selenium

Main features:

1. release_meta.py - Scraps and persists releases meta-information  
2. freeband.py - Detects 'Name your Price' (free) Bandcamp albums
3. bandown.py - Downloads free albums. Requires Selenium driver

### Running locally against a [remote] Mongo DB
>       export MONGO_URL="<MONGO_URL>"
>       python release_meta.py --tag jazz
>       python freeband.py
>       python bandown.py

### Running in Docker container against a [remote] Mongo DB
>       docker build -t finder -f docker/release_mining/Dockerfile .
>       docker build -t enricher -f docker/enrichment_tracklist/Dockerfile .
>       docker run --env MONGO_URL="<MONGO_URL>" finder:latest --use_saved_tags True
>       docker run --env MONGO_URL="<MONGO_URL>" enricher:latest

Note: in docker/k8s the feature --scrap-download-size currently works unstable due to Selenium timeouts. 

### Running in a Kubernetes cluster against a [remote] Mongo DB
>       eval $(minikube docker-env)
>       kubectl apply -f deployment-finder.yaml
>       kubectl apply -f deployment-enricher.yaml
>       kubectl set env --all MONGO_URL="<MONGO_URL>"

#### Scaling in Kubernetes
>       kubectl scale --replicas=10 -f deployment-enricher.yaml


### Other files/scripts

1. tracklist.py - generates album track list
2. config.py - command line config options listed here
2. album.py - data model for Bandcamp album
