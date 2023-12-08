#!/bin/bash

krakenuniq --db minikraken --report-file $2 $1 --output $2
# phyloligo.py -d JSD -i $1 -o $2 -c 64 --method joblib
# phyloselect.py -i $2 -m kmedoids --noX -o $3 -p 20