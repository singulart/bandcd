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
>       docker build -t band1 -f Dockerfile .
>       docker run --env MONGO_URL="<MONGO_URL>" band1:latest --use_saved_tags True

### Running in a Kubernetes cluster against a [remote] Mongo DB
>       kubectl apply -f deployment.yaml
>       kubectl set env --all MONGO_URL="<MONGO_URL>"

#### Scaling in Kubernetes
>       kubectl scale --replicas=10 -f deployment.yaml


### Other files/scripts

1. tracklist.py - generates album track list
2. config.py - command line config options listed here
2. album.py - data model for Bandcamp album
