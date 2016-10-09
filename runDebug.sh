#!/bin/bash

mkdir -p /tmp/remakemathoid

docker run --rm \
    --name wtl-dev-remakemathoid \
    -v $(pwd):/latex2svg \
    -v /tmp/remakemathoid:/tmp \
    -p 10044:10044 \
    wikitolearn/remakemathoid