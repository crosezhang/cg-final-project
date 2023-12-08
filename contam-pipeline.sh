#!/bin/bash
for f in $1/*.fasta
do 
    FILENAME=$(echo $f  | cut -d "/" -f 3 | cut -d "." -f 1)
    KRAKEN_FILE=$2"/"$FILENAME"_kraken.txt"
    PHYLOLIGO_FILE=$3"/"$FILENAME"_phyloligo.txt"
    OUTPUT_FILE=$4"/"$FILENAME".out"
    printf "\n"
    echo "Running KrakenUniq"
    krakenuniq --db minikraken --report-file $KRAKEN_FILE $f --output $KRAKEN_FILE
    printf "\n"
    echo "Running PhylOligo"
    phyloligo.py -d JSD -i $f -o $PHYLOLIGO_FILE -c 64 --method joblib
    printf "\n"
    echo "Running Analysis Python Script"
    python3 CGProcess.py $f $KRAKEN_FILE $PHYLOLIGO_FILE $OUTPUT_FILE
done