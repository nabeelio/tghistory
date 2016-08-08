#!/bin/sh

env/bin/pelican \
  -s pelicanconf.py \
  -o output/ \
  --ignore-cache \
  --relative-urls

cp -R static/* output/
