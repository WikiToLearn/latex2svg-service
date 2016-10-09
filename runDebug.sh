#!/bin/bash

mkdir -p /tmp/remakemathoid

docker run --rm \
    -v $(pwd):/latex2svg \
    -v /tmp/remakemathoid:/tmp \
    -p 5000:5000 \
    wikitolearn/remakemathoid