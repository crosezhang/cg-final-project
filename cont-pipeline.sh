#!/bin/bash

# krakenuniq --db minikraken --report-file $2 $1
phyloligo.py -d JSD -i $1 -o $2 -c 64 --method joblib
phyloselect.py -f $1 -i $2 -m hdbscan --noX -o $3 -p 10